import numpy as np
import json
import os

class MagicNumbers:
    def __init__(
        self,
        magicNumberFen: np.int64,
        magicNumbersW: list[np.int64],
        magicNumbersB: list[np.int64],
        fromRandom=False,
    ):
        if fromRandom:
            self.magicNumberFen = np.random.randint(-(2**30), 2**30)
            self.magicNumbersW = np.random.randint(-(2**30), 2**30, 7)
            self.magicNumbersB = np.random.randint(-(2**30), 2**30, 7)
        else:
            self.magicNumberFen = magicNumberFen
            self.magicNumbersW = magicNumbersW
            self.magicNumbersB = magicNumbersB


class GeneticAlgorithm:
    def __init__(self, population_size=100, mutation_rate=0.05):
        self.population_size = population_size
        self.mutation_rate = mutation_rate

    def initialize_population(self):
        return [
            MagicNumbers(None, None, None, fromRandom=True)
            for _ in range(self.population_size)
        ]

    def load_population(self):
        with open("last_gen", "r") as f:
            data = json.load(f)
            return [
                MagicNumbers(
                    item["magicNumberFen"], item["magicNumbersW"], item["magicNumbersB"]
                )
                for item in data
            ]

    def save_population(self, population):
        data = [
            {
                "magicNumberFen": p.magicNumberFen,
                "magicNumbersW": p.magicNumbersW.tolist(),
                "magicNumbersB": p.magicNumbersB.tolist(),
            }
            for p in population
        ]
        with open("last_gen", "w") as f:
            json.dump(data, f)

    def load_fitness(self):
        if os.path.exists("last_gen_result"):
            with open("last_gen_result", "r") as f:
                return json.load(f)
        return {}

    def select_parents(self, fitness):
        total_fitness = sum(fitness.values())
        selection_probs = [f / total_fitness for f in fitness.values()]
        return np.random.choice(self.population, 2, p=selection_probs)

    def crossover(self, parent1, parent2):
        if np.random.rand() > 0.5:
            return MagicNumbers(
                parent1.magicNumberFen, parent2.magicNumbersW, parent2.magicNumbersB
            )
        else:
            return MagicNumbers(
                parent2.magicNumberFen, parent1.magicNumbersW, parent1.magicNumbersB
            )

    def mutate(self, child):
        if np.random.rand() < self.mutation_rate:
            child.magicNumberFen = np.random.randint(-(2**30), 2**30)
        if np.random.rand() < self.mutation_rate:
            child.magicNumbersW[np.random.randint(0, 7)] = np.random.randint(
                -(2**30), 2**30
            )
        if np.random.rand() < self.mutation_rate:
            child.magicNumbersB[np.random.randint(0, 7)] = np.random.randint(
                -(2**30), 2**30
            )
        return child

    def evolve(self):
        if os.path.exists("last_gen"):
            self.population = self.load_population()
            fitness = self.load_fitness()
            new_population = []

            for _ in range(self.population_size):
                parent1, parent2 = self.select_parents(fitness)
                child = self.crossover(parent1, parent2)
                child = self.mutate(child)
                new_population.append(child)
                self.save_population(new_population)
        else:
            self.population = self.initialize_population()
            self.save_population(self.population)


# Usage
ga = GeneticAlgorithm()
ga.evolve()
