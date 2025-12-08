from pydantic import BaseModel, Field

class SetGARequest(BaseModel):
    target: str = Field(..., min_length=1, description="Password to guess")
    max_generations: int = Field(1000, gt=0, description="Maximum number of generations")
    parents_mating: int = Field(10, gt=0, description="Number of parents for mating")
    sol_per_pop: int = Field(100, gt=0, description="Number of individuals in the population")
    keep_parents: int = Field(2, ge=0, description="Number of parents to keep")
    mutation_percent_genes: int = Field(10, ge=0, le=100, description="Percentage of genes to mutate")
    