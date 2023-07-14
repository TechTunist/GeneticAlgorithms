import os
import numpy as np
import pandas as pd
from population import Population
from simulation import Simulation
from genome import Genome
from creature import Creature

def run_experiment(population_size, mutation_rate, mutation_range, output_dir):

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Create subdirectories for fitness data and fittest creature data
    fitness_data_dir = os.path.join(output_dir, 'fitness_data')
    fittest_creature_dir = os.path.join(output_dir, 'fittest_creature')
    os.makedirs(fitness_data_dir, exist_ok=True)
    os.makedirs(fittest_creature_dir, exist_ok=True)

    # Set the parameters for the genetic algorithm
    gene_count = 6  # Set this to the number of genes you want to use
    num_iterations = 10  # Set this to the number of iterations you want to run

    # Initialize the population and simulation
    population = Population(population_size, gene_count)
    simulation = Simulation()

    # Run the genetic algorithm
    for i in range(num_iterations):
        # Evaluate the current population
        fitnesses, avg_speeds, path_straightnesses, creatures = simulation.eval_population(population, i)

        # Calculate path straightness and average speed
        path_straightnesses = [creature.get_path_straightness(creature.positions) for creature in creatures]
        avg_speeds = [creature.get_average_speed(creature.positions) for creature in creatures]

        # Print some statistics about the current generation
        print(f"Generation {i}:")
        print(f"  Max fitness: {max(fitnesses)}")
        print(f"  Min fitness: {min(fitnesses)}")
        print(f"  Avg fitness: {np.mean(fitnesses)}")

        fitness_df = pd.DataFrame({
            'max_distance': [max(fitnesses)],
            'min_distance': [min(fitnesses)],
            'avg_distance': [np.mean(fitnesses)],
            'avg_speed': [np.mean(avg_speeds)],  # Save average speeds
            'path_straightness': [np.mean(path_straightnesses)]  # Save path straightness values
        })
        
        # fitness_csv_filename = os.path.join(output_dir, f"generation_{i}_fitness.csv")
        # fitness_df.to_csv(fitness_csv_filename, index=False)

        # Save the fitness data to the fitness_data directory
        fitness_csv_filename = os.path.join(fitness_data_dir, f"generation_{i}_fitness.csv")
        fitness_df.to_csv(fitness_csv_filename, index=False)

        # Save the DNA of the creatures to CSV files
        for j, creature in enumerate(population.creatures):
            # csv_filename = os.path.join(output_dir, f"generation_{i}_creature_{j}.csv")
            # Genome.to_csv(creature.dna, csv_filename)
            fittest_creature = population.creatures[np.argmax(fitnesses)]
            csv_filename = os.path.join(output_dir, f"generation_{i}_fittest_creature.csv")
            Genome.to_csv(fittest_creature.dna, csv_filename)

        # Select parents and create the next generation
        fitness_map = population.get_fitness_map(fitnesses)
        offspring = []
        for _ in range(population_size // 2):
            parent1_index = population.select_parent(fitness_map)
            parent2_index = population.select_parent(fitness_map)
            parent1 = population.creatures[parent1_index]
            parent2 = population.creatures[parent2_index]

            # Perform crossover and mutation
            child_dna = Genome.crossover(parent1.dna, parent2.dna)
            child_dna = Genome.point_mutate(child_dna, mutation_rate, mutation_range)
            

            ##### testing this #####
            # child_dna = Genome.grow_mutate(child_dna, mutation_rate)
            ########################


            # Create the child and add it to the new generation
            child = Creature(gene_count=gene_count)
            child.update_dna(child_dna)
            offspring.append(child)

    # Replace the old generation with the new onejupyter no 
        population.creatures = offspring

# function to automate simulations based on param combinations dictionary
def run_experiments(param_combinations):
    for i, params in enumerate(param_combinations):
        print(f"Running experiment {i+1} of {len(param_combinations)} with parameters: {params}")
        # Create a directory name based on the parameter values
        dir_name = f"sphere_experiment_pop{params['population_size']}_mutrate{params['mutation_rate']}_mutrange{params['mutation_range']}"
        # Run the experiment with the given parameters
        run_experiment(
            population_size=params['population_size'], 
            mutation_rate=params['mutation_rate'], 
            mutation_range=params['mutation_range'], 
            output_dir=dir_name
        )

# Define a list of parameter combinations to test
param_combinations = [
    {"population_size": 100, "mutation_rate": 0.1, "mutation_range": 0.1},
    {"population_size": 100, "mutation_rate": 0.1, "mutation_range": 0.4},
    {"population_size": 100, "mutation_rate": 0.1, "mutation_range": 0.8},

    {"population_size": 100, "mutation_rate": 0.4, "mutation_range": 0.4},
    {"population_size": 100, "mutation_rate": 0.8, "mutation_range": 0.8},
    
    {"population_size": 100, "mutation_rate": 0.4, "mutation_range": 0.1},
    {"population_size": 100, "mutation_rate": 0.8, "mutation_range": 0.1},


    {"population_size": 300, "mutation_rate": 0.1, "mutation_range": 0.1},
    {"population_size": 300, "mutation_rate": 0.1, "mutation_range": 0.4},
    {"population_size": 300, "mutation_rate": 0.1, "mutation_range": 0.8},

    {"population_size": 300, "mutation_rate": 0.4, "mutation_range": 0.4},
    {"population_size": 300, "mutation_rate": 0.8, "mutation_range": 0.8},
    
    {"population_size": 300, "mutation_rate": 0.4, "mutation_range": 0.1},
    {"population_size": 300, "mutation_rate": 0.8, "mutation_range": 0.1},

    {"population_size": 600, "mutation_rate": 0.1, "mutation_range": 0.1},
    {"population_size": 600, "mutation_rate": 0.1, "mutation_range": 0.4},
    {"population_size": 600, "mutation_rate": 0.1, "mutation_range": 0.8},

    {"population_size": 600, "mutation_rate": 0.4, "mutation_range": 0.4},
    {"population_size": 600, "mutation_rate": 0.8, "mutation_range": 0.8},
    
    {"population_size": 600, "mutation_rate": 0.4, "mutation_range": 0.1},
    {"population_size": 600, "mutation_rate": 0.8, "mutation_range": 0.1},
    

    {"population_size": 800, "mutation_rate": 0.1, "mutation_range": 0.1},
    {"population_size": 800, "mutation_rate": 0.1, "mutation_range": 0.5},
    {"population_size": 800, "mutation_rate": 0.1, "mutation_range": 0.9},
    
    {"population_size": 800, "mutation_rate": 0.5, "mutation_range": 0.6},
    {"population_size": 800, "mutation_rate": 0.9, "mutation_range": 0.1},
    
    # Add more parameter combinations as needed...
]

# Run the experiments
run_experiments(param_combinations)

