import pygad
import numpy as np 

GENES = [chr(i) for i in range(32, 127)]  # ascii characters
POLISH_CHARS = ['ą', 'ć', 'ę', 'ł', 'ń', 'ó', 'ś', 'ź', 'ż', 
                'Ą', 'Ć', 'Ę', 'Ł', 'Ń', 'Ó', 'Ś', 'Ź', 'Ż'] # polish characters

GENES.extend(POLISH_CHARS)

def run_ga(target: str,max_generations: int = 1000, parents_mating: int = 10, sol_per_pop: int = 100,
    keep_parents: int = 2,mutation_percent_genes: int = 10):
    target_indices = [GENES.index(char) for char in target]
    progress_list = []
    
    def fitness_func(ga_instance, solution, solution_idx):
        fitness = sum(1 for i in range(len(solution)) if int(solution[i]) == target_indices[i])
        return fitness
    
    def on_generation(ga_instance):
        solution, fitness, _ = ga_instance.best_solution()
        decoded = ''.join(GENES[int(gene)] for gene in solution)
    
        progress_list.append({
                "generation": ga_instance.generations_completed,
                "solution": decoded,
                "fitness": int(fitness),
                "max_fitness": len(target)
            })
    
        if fitness == len(target):
            print(f"Gen {ga_instance.generations_completed}: '{decoded}' "
                f"(Fitness: {fitness}/{len(target)})")
            return 'stop'
    
    num_genes = len(target)
    gene_space = [range(len(GENES)) for _ in range(num_genes)]

    ga_instance = pygad.GA(
        num_generations=max_generations, #max generacji
        num_parents_mating=parents_mating, #liczba rodzicówe do krzyżowania
        fitness_func=fitness_func, #funkcja oceny
        sol_per_pop=sol_per_pop, #liczba osobników w populacji 
        num_genes=num_genes, #liczba genów w osobniku (długość hasła)
        gene_space=gene_space, #możliwe wartości genów
        parent_selection_type="tournament", #metoda selekcji rodziców
        keep_parents=keep_parents, #liczba rodziców do zachowania w następnej generacji
        crossover_type="single_point", #metoda krzyżowania
        mutation_type="random", #metoda mutacji
        mutation_percent_genes=mutation_percent_genes, #procent genów do mutacji
        on_generation=on_generation #funkcja wywoływana na koniec każdej generacji
    ) 

    print(f"Target: {target}")
    print(f"Length: {len(target)}")
    ga_instance.run()

    solution, fitness, _ = ga_instance.best_solution()
    decoded = ''.join(GENES[int(gene)] for gene in solution)

    print(f"final solution: '{decoded}'")
    print(f"Fitness: {int(fitness)}/{len(target)}")

    return {
        "success": bool(int(fitness) == len(target)),
        "final_solution": decoded,
        "fitness": int(fitness),
        "max_fitness": len(target),
        "generations_completed": ga_instance.generations_completed,
        "progress": progress_list,
        "message": "Find solution" if fitness == len(target) else "Not found within the generation limit"
    }
    
