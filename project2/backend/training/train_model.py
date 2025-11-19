import os
import sys
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from model_def import MNISTNet

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f'Using device: {device}\n')

train_transform = transforms.Compose([
    transforms.RandomRotation(10),
    transforms.RandomAffine(0, translate=(0.1, 0.1)),
    transforms.ToTensor(),
    transforms.Normalize((0.1307,), (0.3081,))
])

test_transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.1307,), (0.3081,))
])

print("Loading MNIST dataset...\n")
train_dataset = datasets.MNIST(root='./data', train=True, download=True, transform=train_transform)
test_dataset = datasets.MNIST(root='./data', train=False, download=True, transform=test_transform)

train_loader = DataLoader(train_dataset, batch_size=128, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=128, shuffle=False)

print(f'MNIST trainset size: {len(train_dataset)}')
print(f'MNIST testset size: {len(test_dataset)}\n')

print("Creating model...\n")
model = MNISTNet().to(device)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)
scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=5, gamma=0.5)

print("Model summary...\n")
print(model)
print(f"\nParameters count: {sum(p.numel() for p in model.parameters())}\n")


def train_epoch(model, loader, criterion, optimizer, device):
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0

    for batch_idx, (data, target) in enumerate(loader):
        data, target = data.to(device), target.to(device)

        optimizer.zero_grad()
        output = model(data)
        loss = criterion(output, target)
        loss.backward()
        optimizer.step()

        running_loss += loss.item()
        _, predicted = torch.max(output.data, 1)
        total += target.size(0)
        correct += (predicted == target).sum().item()

        if batch_idx % 100 == 0:
            print(f"  Batch {batch_idx}/{len(loader)}, Loss: {loss.item():.4f}")

    avg_loss = running_loss / len(loader)
    accuracy = 100 * correct / total
    return avg_loss, accuracy


def test_epoch(model, loader, criterion, device):
    model.eval()
    running_loss = 0.0
    correct = 0
    total = 0

    with torch.no_grad():
        for data, target in loader:
            data, target = data.to(device), target.to(device)
            output = model(data)
            loss = criterion(output, target)

            running_loss += loss.item()
            _, predicted = torch.max(output.data, 1)
            total += target.size(0)
            correct += (predicted == target).sum().item()

    avg_loss = running_loss / len(loader)
    accuracy = 100 * correct / total
    return avg_loss, accuracy


print("Starting training...\n")
num_epochs = 15  

best_acc = 0.0
for epoch in range(num_epochs):
    print(f"\nEpoch {epoch + 1}/{num_epochs}")
    train_loss, train_acc = train_epoch(model, train_loader, criterion, optimizer, device)
    test_loss, test_acc = test_epoch(model, test_loader, criterion, device)

    scheduler.step()

    print(f"Train - Loss: {train_loss:.4f}, Accuracy: {train_acc:.2f}%")
    print(f"Test - Loss: {test_loss:.4f}, Accuracy: {test_acc:.2f}%")
    print(f"Learning rate: {optimizer.param_groups[0]['lr']:.6f}")

    if test_acc > best_acc:
        best_acc = test_acc

print("\n" + "=" * 50)
print("Finished!")
print(f"Best test accuracy: {best_acc:.2f}%")
print(f"Final test accuracy: {test_acc:.2f}%")
print("=" * 50 + "\n")

os.makedirs('../models', exist_ok=True)

model_path = '../models/MNISTNet.pth'
torch.save(model.state_dict(), model_path)
print(f"✓ Model saved to '{model_path}'")

torch.save({
    'model_state_dict': model.state_dict(),
    'model_class': MNISTNet,
    'best_accuracy': best_acc,
}, '../models/MNISTNetFull.pth')
print(f"Full model saved to '../models/MNISTNetFull.pth'")