import numpy as np
import json
import os


class MagicNumbers:
    def __init__(
        self,
        magicNumberFen: np.int64,
        magicNumbersW_T: list[np.int64],
        magicNumbersB_T: list[np.int64],
        magicNumbersW_B: list[np.int64],
        magicNumbersB_B: list[np.int64],
        fromRandom=False,
    ):
        if fromRandom:
            self.magicNumberFen = np.random.randint(-(2**30), 2**30)
            self.magicNumbersW_T = np.random.randint(-(2**30), 2**30, 7)
            self.magicNumbersB_T = np.random.randint(-(2**30), 2**30, 7)
            self.magicNumbersW_B = np.random.randint(-(2**30), 2**30, 7)
            self.magicNumbersB_B = np.random.randint(-(2**30), 2**30, 7)
        else:
            self.magicNumberFen = magicNumberFen
            self.magicNumbersW_T = magicNumbersW_T
            self.magicNumbersB_T = magicNumbersB_T
            self.magicNumbersW_B = magicNumbersW_B
            self.magicNumbersB_B = magicNumbersB_B


class GeneticAlgorithm:
    def __init__(self, population_size=100, mutation_rate=0.05):
        self.population_size = population_size
        self.mutation_rate = mutation_rate

    def initialize_population(self):
        return [
            MagicNumbers(None, None, None, None, None, fromRandom=True)
            for _ in range(self.population_size)
        ]

    def load_population(self):
        with open("last_gen", "r") as f:
            data = json.load(f)
            return [
                MagicNumbers(
                    item["magicNumberFen"],
                    item["magicNumbersW_T"],
                    item["magicNumbersB_T"],
                    item["magicNumbersW_B"],
                    item["magicNumbersB_B"],
                )
                for item in data
            ]

    def save_population(self, population):
        data = [
            {
                "magicNumberFen": p.magicNumberFen,
                "magicNumbersW_T": p.magicNumbersW_T.tolist(),
                "magicNumbersB_T": p.magicNumbersB_T.tolist(),
                "magicNumbersW_B": p.magicNumbersW_B.tolist(),
                "magicNumbersB_B": p.magicNumbersB_B.tolist(),
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
                parent1.magicNumberFen,
                parent2.magicNumbersW_T,
                parent2.magicNumbersB_T,
                parent2.magicNumbersW_B,
                parent2.magicNumbersB_B,
            )
        else:
            return MagicNumbers(
                parent2.magicNumberFen,
                parent1.magicNumbersW_T,
                parent1.magicNumbersB_T,
                parent1.magicNumbersW_B,
                parent1.magicNumbersB_B,
            )

    def mutate(self, child):
        if np.random.rand() < self.mutation_rate:
            child.magicNumberFen = np.random.randint(-(2**30), 2**30)
        if np.random.rand() < self.mutation_rate:
            child.magicNumbersW_T = np.random.randint(-(2**30), 2**30, 7)
        if np.random.rand() < self.mutation_rate:
            child.magicNumbersB_T = np.random.randint(-(2**30), 2**30, 7)
        if np.random.rand() < self.mutation_rate:
            child.magicNumbersW_B = np.random.randint(-(2**30), 2**30, 7)
        if np.random.rand() < self.mutation_rate:
            child.magicNumbersB_B = np.random.randint(-(2**30), 2**30, 7)
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
