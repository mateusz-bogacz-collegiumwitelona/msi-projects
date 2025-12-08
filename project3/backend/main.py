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

@app.post(
    "/run",
    tags=["Genetic Algorithm"],
    summary="Run genetic algorithm to find target string",
    responses={
        200: {
            "description": "Algorithm completed successfully",
            "content": {
                "application/json": {
                    "example": {
                        "success": True,
                        "final_solution": "string",
                        "fitness": 6,
                        "max_fitness": 6,
                        "generations_completed": 75,
                        "progress": [
                            {
                                "generation": 1,
                                "solution": "s$0gD3",
                                "fitness": 1,
                                "max_fitness": 6
                            },
                            {
                                "generation": 43,
                                "solution": "strWng",
                                "fitness": 5,
                                "max_fitness": 6
                            },
                            {
                                "generation": 75,
                                "solution": "string",
                                "fitness": 6,
                                "max_fitness": 6
                            }
                        ],
                        "message": "Find solution"
                    }
                }
            }
        },
        400: {
            "description": "Invalid character in target string",
            "content": {
                "application/json": {
                    "example": {"detail": "Invalid character 'ö' in target string."}
                }
            }
        },
        500: {
            "description": "Internal server error",
            "content": {
                "application/json": {
                    "example": {"detail": "An error occurred"}
                }
            }
        }
    }
)
async def run_genetic_algorithm(request: SetGARequest):
    """
    Run genetic algorithm to evolve a solution matching the target string.
    
    **Request body:**
    - `target`: String to find (supports ASCII + Polish characters)
    - `max_generations`: How many iterations to run
    - `parents_mating`: Number of best solutions to breed
    - `sol_per_pop`: Population size
    - `keep_parents`: Best solutions to preserve (elitism)
    - `mutation_percent_genes`: Mutation rate (0-100%)
    
    **Returns:**
    - `success`: Whether target was found
    - `final_solution`: Best solution found
    - `fitness`: Number of correct characters
    - `max_fitness`: Target length
    - `generations_completed`: Total generations executed
    - `progress`: List of best solutions per generation
    - `message`: Result message
    """
    try:
        # Validate characters
        for char in request.target:
            if char not in ga.GENES:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid character '{char}' in target string."
                )
        
        # Run algorithm
        result = ga.run_ga(
            target=request.target,
            max_generations=request.max_generations,
            parents_mating=request.parents_mating,
            sol_per_pop=request.sol_per_pop,
            keep_parents=request.keep_parents,
            mutation_percent_genes=request.mutation_percent_genes
        )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)