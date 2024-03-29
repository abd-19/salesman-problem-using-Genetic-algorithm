import random
import tkinter as tk
from itertools import permutations

class Genetic:
    def __init__(self, cities, population_size=50, elite_size=10, mutation_rate=0.01, generations= 1000):
        self.cities = cities
        self.population_size = population_size
        self.elite_size = elite_size
        self.mutation_rate = mutation_rate
        self.generations = generations

    def initial_population(self):
        return [random.sample(self.cities, len(self.cities)) for _ in range(self.population_size)]

    def fitness(self, route):
        total_distance = 0
        for i in range(len(route)):
            from_city = route[i]
            to_city = route[(i + 1) % len(route)]
            total_distance += self.distance(from_city, to_city)
        return 1 / total_distance

    def distance(self, city1, city2):
        return ((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2) ** 0.5

    def crossover(self, parent1, parent2):
        start = random.randint(0, len(parent1))
        end = random.randint(start, len(parent1))
        child = [None] * len(parent1)
        for i in range(start, end):
            child[i] = parent1[i]
        j = 0
        for i in range(len(parent2)):
            if parent2[i] not in child:
                while child[j] is not None:
                    j += 1
                child[j] = parent2[i]
        return child

    def mutate(self, route):
        for i in range(len(route)):
            if random.random() < self.mutation_rate:
                j = random.randint(0, len(route) - 1)
                route[i], route[j] = route[j], route[i]

    def evolve(self, population):
        elites = sorted(population, key=lambda x: self.fitness(x), reverse=True)[:self.elite_size]
        children = []
        for _ in range(self.population_size - self.elite_size):
            parent1, parent2 = random.choices(population, k=2)
            child = self.crossover(parent1, parent2)
            self.mutate(child)
            children.append(child)
        return elites + children

class APP:
    def __init__(self, master):
        self.master = master
        self.canvas = tk.Canvas(master, width=500, height=500)
        self.canvas.pack()
        self.cities = [(100, 100), (200, 200), (300, 300), (400, 400),(150, 100), (200, 150), (200, 300), (400, 300),(100, 400), (300, 100), (400, 200), (300, 400),(100, 200), (200, 400), (300, 200), (400, 100),(100,50),(50,100),(50,200),(50,300),(50,400),(50,340),]
        self.draw_cities()
        self.tsp_genetic = Genetic(self.cities)
        self.population = self.tsp_genetic.initial_population()
        self.current_generation = 0
        self.update()

    def draw_cities(self):
        for city in self.cities:
            self.canvas.create_oval(city[0] - 5, city[1] - 5, city[0] + 5, city[1] + 5, fill="red")
      
    def draw_route(self, route):
        self.canvas.delete("route")
        for i in range(len(route)):
            from_city = route[i]
            to_city = route[(i + 1) % len(route)]
            self.canvas.create_line(from_city[0], from_city[1], to_city[0], to_city[1], fill="blue", tags="route")

    def update(self):
        if self.current_generation < self.tsp_genetic.generations:
            self.population = self.tsp_genetic.evolve(self.population)
            best_route = max(self.population, key=lambda x: self.tsp_genetic.fitness(x))
            self.draw_route(best_route)
            self.current_generation += 1
            self.master.after(100, self.update)
            print("number of generations: ",self.current_generation)


root = tk.Tk()
app = APP(root)
root.mainloop()
