'''
Задание 5.
Решить диофантовое уравнение, используя генетический алгоритм.
''' 

import matplotlib.pyplot as plt
from random import randint
from time import sleep


# USEFUL FUNCTIONS

def read_powers(file_name: str) -> list:
	with open(file_name) as f:
		powers = list(map(int, f.readline().split(' ')))
		
		result = powers.pop(-1)

		u_pows = powers[::5]
		w_pows = powers[1::5]
		x_pows = powers[2::5]
		y_pows = powers[3::5]
		z_pows = powers[4::5]

		return [[u_pows, w_pows, x_pows, y_pows, z_pows], result]

def get_equation_form(powers: list, result: int) -> str:
	u_pows, w_pows, x_pows, y_pows, z_pows = powers
	equation = ''

	for i in range(len(u_pows)):
		term = ''
		if u_pows[i]:
			term += f'(u^{u_pows[i]})' if u_pows[i] > 1 else 'u'	
		if w_pows[i]:
			term += f'(w^{w_pows[i]})' if w_pows[i] > 1 else 'w'
		if x_pows[i]:
			term += f'(x^{x_pows[i]})' if x_pows[i] > 1 else 'x'
		if y_pows[i]:
			term += f'(y^{y_pows[i]})' if y_pows[i] > 1 else 'y'
		if z_pows[i]:
			term += f'(z^{z_pows[i]})' if z_pows[i] > 1 else 'z'
		equation += f' + {term}' if equation else term

	return f'{equation} = {result}'

def draw_line_segment(point_1: list, point_2: list, color: str):
	plt.plot([point_1[0], point_2[0]], [point_1[1], point_2[1]], color=color)

def plot(average_chromosomes: list, best_chromosomes: list, generations_scores: list):
	average_chromosomes_vertices = []
	best_chromosomes_vertices = []	
	for i in range(len(average_chromosomes)):
		average_chromosomes_vertices.append([i, average_chromosomes[i]])
		best_chromosomes_vertices.append([i, best_chromosomes[i]])

	for i in range(len(best_chromosomes_vertices) - 1):
		draw_line_segment(average_chromosomes_vertices[i], average_chromosomes_vertices[i + 1], 'red')
		draw_line_segment(best_chromosomes_vertices[i], best_chromosomes_vertices[i + 1], 'blue')
	
	for i, scores in enumerate(generations_scores):
		for score in scores:
			plt.scatter(i, score, color='green', s=12)

	plt.plot([0, len(best_chromosomes_vertices) - 1], [0, 0], color='black', linestyle='dashed')

	plt.show()


# GENETIC ALGORITHM

def function(variables: list, powers: list) -> int:
	u, w, x, y, z = variables
	u_pows, w_pows, x_pows, y_pows, z_pows = powers

	return sum([(u**u_pows[i]) * (w**w_pows[i]) * (x**x_pows[i]) * (y**y_pows[i]) * (z**z_pows[i]) for i in range(len(u_pows))])

def generation(population: int) -> list:
	return [[randint(-3, 3) for i in range(5)] for j in range(population)]

def fitness(result: int, powers: list, generation: list) -> list:
	fitness_scores = [abs(function(chromosome, powers) - result) for i, chromosome in enumerate(generation)]
	average_fitness = sum(fitness_scores) / len(fitness_scores)

	return [fitness_scores, average_fitness]

def selection(fitness_scores: list, average_fitness: float) -> list:
	survival_coefficient = sum([1 / score if score else 1 for score in fitness_scores])
	survival_probabilities = [1 / score / survival_coefficient if score else 1 for score in fitness_scores]

	return [survival_coefficient, survival_probabilities]

def crossover(result: int, powers: list, generation: list, selection_results: list) -> list:
	survival_coefficient, survival_probabilities = selection_results
	good_chromosomes = []
	bad_chromosomes = []

	for chromosome, probability in zip(generation, survival_probabilities):
		good_chromosomes.append(chromosome) if probability > survival_coefficient else bad_chromosomes.append(chromosome)

	new_generation = []
	if len(good_chromosomes) == 1:
		new_generation = [good_chromosomes[0][:4] + [bad_chromosomes[i][randint(0, 4)]] for i in range(4)]
		new_generation += good_chromosomes
	elif 1 < len(good_chromosomes) < 5:
		for chromosome in good_chromosomes:
			new_generation += [chromosome[:4] + [bad_chromosomes[i][randint(0, 4)]] for i in range(len(bad_chromosomes))]
		new_generation += good_chromosomes
	else:
		best_chromosome = [generation[0], survival_probabilities[0]]
		for chromosome, probability in zip(generation[1:], survival_probabilities[1:]):
			if best_chromosome[1] < probability:
				best_chromosome = [chromosome, probability]
		best_chromosome = best_chromosome[0]
		
		new_generation = [best_chromosome[:3] + chromosome[3:] for chromosome in generation]

	fitness_scores, average_fitness = fitness(result, powers, new_generation)
	new_selection_results = selection(fitness_scores, average_fitness)

	return [new_generation, new_selection_results, fitness_scores, average_fitness]

def mutation(result: int, powers: list, generation: list, selection_results: list):
	survival_coefficient, survival_probabilities = selection_results
	best_chromosome = [generation[0], survival_probabilities[0]]
	for chromosome, probability in zip(generation[1:], survival_probabilities[1:]):
		if best_chromosome[1] < probability:
			best_chromosome = [chromosome, probability]
	best_chromosome = best_chromosome[0]

	for chromosome in generation:
		chromosome[randint(0, 4)] += randint(-3, 3)
	generation.pop(randint(0, len(generation) - 1))
	generation.append(best_chromosome)

	fitness_scores, average_fitness = fitness(result, powers, generation)

	if len(generation) != 5:
		survivors = [[chromosome, fitness] for chromosome, fitness in zip(generation, fitness_scores)]
		survivors = sorted(survivors, key=lambda survivor: survivor[1])[:5]
		generation = [survivor[0] for survivor in survivors]
		fitness_scores, average_fitness = fitness(result, powers, generation)
	
	new_selection_results = selection(fitness_scores, average_fitness)

	return [generation, new_selection_results, fitness_scores, average_fitness]

def genetic_algorithm(data: str, generations_limit: int, population: int):
	powers, result = read_powers(data)
	equation_form = get_equation_form(powers, result)

	average_chromosomes = []
	best_chromosomes = []
	generations_scores = []
	
	next_generation = initial_generation = generation(population)
	fitness_scores, average_fitness = fitness(result, powers, initial_generation)

	generations_count = 1
	bad_generation_count = 3
	while True:
		generations_count += 1
		if generations_count > generations_limit:
			generations_count = 1
			bad_generation_count = 3
			next_generation = initial_generation = generation(population)
			fitness_scores, average_fitness = fitness(result, powers, initial_generation)

			average_chromosomes = []
			best_chromosomes = []
			generations_scores = []
			continue

		selection_results = selection(fitness_scores, average_fitness)
		crossover_generation, crossover_selection_results, crossover_fitness_scores, crossover_average_fitness = crossover(result, powers, next_generation, selection_results)

		mutation_generation, mutation_selection_results, mutation_fitness_scores, mutation_average_fitness = mutation(result, powers, crossover_generation, crossover_selection_results)

		if 1 - average_fitness / mutation_average_fitness > 0.1:
			bad_generation_count -= 1

		if bad_generation_count:
			next_generation = mutation_generation
			fitness_scores, average_fitness = mutation_fitness_scores, mutation_average_fitness
			best_chromosomes.append(min(fitness_scores))
			average_chromosomes.append(average_fitness)
			generations_scores.append(fitness_scores)
		else:
			bad_generation_count = 3
			next_generation = generation(population)
			fitness_scores, average_fitness = fitness(result, powers, next_generation)
			best_chromosomes.append(None)
			average_chromosomes.append(None)
			generations_scores.append([])

		if 0 in fitness_scores:
			solution = next_generation[fitness_scores.index(0)] 
			print(f'Solution for {equation_form}:\n {solution}\nGenerations count: {generations_count}\n')
			plot(average_chromosomes, best_chromosomes, generations_scores)
			break



'''
START
Generate the initial population
Compute fitness
REPEAT
    Selection
    Crossover
    Mutation
    Compute fitness
UNTIL population has converged
STOP
'''

def task_5():
	genetic_algorithm('1.txt', 30, 5)
	#genetic_algorithm('2.txt', 30, 5)

if __name__ == '__main__':
	task_5()