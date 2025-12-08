import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from set_ga_request import SetGARequest
import ga 

app = FastAPI(
    title="Genetic Algorithm Password Cracker",
    description="An API that uses a genetic algorithm to guess a target password.",
    version="v0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/")
async def root(request: SetGARequest):
    try:
        for char in request.target:
            if char not in ga.GENES:
                raise HTTPException(status_code=400, detail=f"Invalid character '{char}' in target string.")
    
        result = ga.run_ga(
            target=request.target,
            max_generations=request.max_generations,
            parents_mating=request.parents_mating,
            sol_per_pop=request.sol_per_pop,
            keep_parents=request.keep_parents,
            mutation_percent_genes=request.mutation_percent_genes)
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)