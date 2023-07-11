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

    # Set the parameters for the genetic algorithm
    gene_count = 3  # Set this to the number of genes you want to use
    num_iterations = 10  # Set this to the number of iterations you want to run

    # Initialize the population and simulation
    population = Population(population_size, gene_count)
    simulation = Simulation()

#     # Run the genetic algorithm
#     for i in range(num_iterations):
#         # Evaluate the current population
#         fitnesses = simulation.eval_population(population, i)

#         # Print some statistics about the current generation
#         print(f"Generation {i}:")
#         print(f"  Max fitness: {max(fitnesses)}")
#         print(f"  Min fitness: {min(fitnesses)}")
#         print(f"  Avg fitness: {np.mean(fitnesses)}")

#         # Save the DNA of the creatures to CSV files
#         for j, creature in enumerate(population.creatures):
#             csv_filename = os.path.join(output_dir, f"generation_{i}_creature_{j}.csv")
#             Genome.to_csv(creature.dna, csv_filename)

#         # Select parents and create the next generation
#         parents = population.select_parents(fitnesses)
#         offspring = []
#         for parent1, parent2 in zip(parents[:-1:2], parents[1::2]):
#             # Perform crossover and mutation
#             child_dna = Genome.crossover(population[parent1].dna, population[parent2].dna)
#             child_dna = Genome.mutate(child_dna, mutation_rate, mutation_range)
#             # Create the child and add it to the new generation
#             child = population[parent1]  # Create a child based on one of the parents
#             child.update_dna(child_dna)  # Update the child's DNA
#             offspring.append(child)  # Add the child to the new generation
#         # Replace the old generation with the new one
#         population.creatures = offspring


# # run the code
# run_experiment(population_size=100, mutation_rate=0.1, mutation_range=0.5, output_dir="experiment1")


    # Run the genetic algorithm
    for i in range(num_iterations):
        # Evaluate the current population
        fitnesses = simulation.eval_population(population, i)

        # Print some statistics about the current generation
        print(f"Generation {i}:")
        print(f"  Max fitness: {max(fitnesses)}")
        print(f"  Min fitness: {min(fitnesses)}")
        print(f"  Avg fitness: {np.mean(fitnesses)}")

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

            # Create the child and add it to the new generation
            child = Creature(gene_count=gene_count)
            child.update_dna(child_dna)
            offspring.append(child)

        # Replace the old generation with the new one
        population.creatures = offspring


# run the code
run_experiment(population_size=100, mutation_rate=0.1, mutation_range=0.5, output_dir="experiment1")

