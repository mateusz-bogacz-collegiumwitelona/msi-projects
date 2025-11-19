import subprocess
import sys
import numpy as np
import uvicorn
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import torch
from torchvision import transforms
from PIL import Image, ImageOps
import io
import os
from model_def import MNISTNet

app = FastAPI(title="MNIST Classifier")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("Loading model...\n")
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = MNISTNet().to(device)

model_path = os.path.join("models", "MNISTNet.pth")
if not os.path.isfile(model_path):
    print("\n" + "="*50)
    print("Model not found - starting auto training...")
    print("Please wait 5-10 minutes until training is complete.")
    print("="*50 + "\n")

    training_path = os.path.join("training", "train_model.py")

    if not os.path.isfile(training_path):
        raise FileNotFoundError(f"Training file not found at '{training_path}'")

    print(f"Running training script: {training_path}\n")

    training_dir = os.path.dirname(os.path.abspath(training_path))
    result = subprocess.run(
        [sys.executable, os.path.basename(training_path)],
        cwd=training_dir,
        capture_output=True,
        text=True
    )

    # Wyświetl output z treningu
    if result.stdout:
        print(result.stdout)

    if result.returncode != 0:
        print("\nERROR during training:")
        if result.stderr:
            print(result.stderr)
        raise RuntimeError("Training script failed. Check the output above for errors.")

    print("\n" + "="*50)
    print("Training complete. Model saved.")
    print("="*50 + "\n")

if not os.path.isfile(model_path):
    raise FileNotFoundError(f"Model file not found at '{model_path}' after training")

model.load_state_dict(torch.load(model_path, map_location=device, weights_only=True))
model.eval()
print(f"Model loaded successfully (device: {device})\n")

transform = transforms.Compose([
    transforms.Resize((28, 28)),
    transforms.ToTensor(),
    transforms.Normalize((0.1307,), (0.3081,))
])

def preprocess_image(image_bytes):
    """
    Converts the image from the frontend to a format that the model understands
    """
    image = Image.open(io.BytesIO(image_bytes))

    if image.mode != 'L':
        image = image.convert('L')

    image = ImageOps.invert(image)

    image_tensor = transform(image)
    image_tensor = image_tensor.unsqueeze(0)
    return image_tensor

@app.get("/")
def root():
    return {
        "message": "Welcome to the MNIST Classifier",
        "endpoints": {
            "/predict": "POST - Send image for classification",
            "/health": "GET - Check API health status"
        }
    }

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "model_loaded": model is not None,
        "device": str(device)
    }

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        image = await file.read()
        image_tensor = preprocess_image(image).to(device)

        with torch.no_grad():
            output = model(image_tensor)
            print(f"Raw model output: {output[0].tolist()}")
            probabilities = torch.nn.functional.softmax(output, dim=1)

        probs = probabilities.cpu().numpy()[0]
        predicted_digit = int(np.argmax(probs))
        confidence = float(np.max(probs))

        return {
            "success": True,
            "predicted_digit": predicted_digit,
            "confidence": confidence,
            "probabilities": {
                str(i): float(prob) for i, prob in enumerate(probs)
            }
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)