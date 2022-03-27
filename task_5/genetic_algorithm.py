'''
Задание 5.
Решить диофантовое уравнение, используя генетический алгоритм.
''' 

import matplotlib.pyplot as plt
from random import randint



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


# Trend Equation: y = b * x + a

def trend_coefficients(chromosomes: list):
	n_1 = len(chromosomes)
	m_1 = sum(range(len(chromosomes)))
	k_1 = sum(chromosomes)
	n_2 = m_1
	m_2 = sum([i*i for i in range(len(chromosomes))])
	k_2 = sum([chromosome*i for i, chromosome in enumerate(chromosomes)])

	b = (n_1*k_2 - n_2*k_1) / (n_1*m_2 - n_2*m_1)
	a = (k_1 - m_1*b) / n_1

	return [a, b]

def draw_line_segment(point_1: list, point_2: list, color: str):
	plt.plot([point_1[0], point_2[0]], [point_1[1], point_2[1]], color=color)

def plot(average_chromosomes: list, best_chromosomes: list):
	average_chromosomes_vertices = []
	best_chromosomes_vertices = []
	for i in range(len(average_chromosomes)):
		average_chromosomes_vertices.append([i, average_chromosomes[i]])
		best_chromosomes_vertices.append([i, best_chromosomes[i]])
		
	for i in range(len(best_chromosomes_vertices) - 1):
		draw_line_segment(average_chromosomes_vertices[i], average_chromosomes_vertices[i + 1], 'red')
		draw_line_segment(best_chromosomes_vertices[i], best_chromosomes_vertices[i + 1], 'blue')

	plt.plot([0, len(best_chromosomes_vertices) - 1], [0, 0], color='black', linestyle='dashed')

	a, b = trend_coefficients(average_chromosomes)
	plt.plot([0, len(average_chromosomes_vertices) - 1], [a, a + b * (len(average_chromosomes_vertices) - 1)], color='red', linestyle='dashed')
	a, b = trend_coefficients(best_chromosomes)
	plt.plot([0, len(best_chromosomes_vertices) - 1], [a, a + b * (len(best_chromosomes_vertices) - 1)], color='blue', linestyle='dashed')

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

	return fitness_scores

def fitness_average(fitness_scores: list, selection_results: list) -> int:
	survival_coefficient, survival_probabilities = selection_results
	average_fitness = sum([survival_probability * score for survival_probability, score in zip(survival_probabilities, fitness_scores)])

	return average_fitness

def selection(fitness_scores: list) -> list:
	survival_coefficient = sum([1 / score if score else 1 for score in fitness_scores])
	survival_probabilities = [1 / score / survival_coefficient if score else 1 for score in fitness_scores]

	return [survival_coefficient, survival_probabilities]

def crossover(result: int, powers: list, population: int, generation: list, selection_results: list) -> list:
	survival_coefficient, survival_probabilities = selection_results
	good_chromosomes = []
	bad_chromosomes = []

	for chromosome, probability in zip(generation, survival_probabilities):
		good_chromosomes.append(chromosome) if probability > survival_coefficient else bad_chromosomes.append(chromosome)

	best_chromosome = [generation[0], survival_probabilities[0]]
	for chromosome, probability in zip(generation[1:], survival_probabilities[1:]):
		if best_chromosome[1] < probability:
			best_chromosome = [chromosome, probability]
	best_chromosome = best_chromosome[0]

	new_generation = []
	if len(good_chromosomes) == 1:
		new_generation = [good_chromosomes[0][:4] + [bad_chromosomes[i][randint(0, 4)]] for i in range(4)]
		new_generation += good_chromosomes
	elif 1 < len(good_chromosomes) < population:
		for chromosome in good_chromosomes:
			new_generation += [chromosome[:4] + [bad_chromosomes[i][randint(0, 4)]] for i in range(len(bad_chromosomes))]
		new_generation += good_chromosomes
	else:
		new_generation = [best_chromosome[:3] + chromosome[3:] for chromosome in generation]

	new_generation.pop(randint(0, len(new_generation) - 1))
	new_generation.append(best_chromosome)

	fitness_scores = fitness(result, powers, new_generation)
	new_selection_results = selection(fitness_scores)
	average_fitness = fitness_average(fitness_scores, new_selection_results)

	return [new_generation, new_selection_results, fitness_scores, average_fitness]

def mutation(result: int, powers: list, population: int, generation: list, selection_results: list):
	survival_coefficient, survival_probabilities = selection_results
	best_chromosome = [generation[0], survival_probabilities[0]]
	for chromosome, probability in zip(generation[1:], survival_probabilities[1:]):
		if best_chromosome[1] < probability:
			best_chromosome = [chromosome, probability]
	best_chromosome = best_chromosome[0]

	for chromosome in generation:
		chromosome[randint(0, 4)] += randint(-1, 1)
	generation.pop(randint(0, len(generation) - 1))
	generation.append(best_chromosome)

	fitness_scores = fitness(result, powers, generation)
	new_selection_results = selection_results
	average_fitness = fitness_average(fitness_scores, selection_results)

	if len(generation) != population:
		survivors = [[chromosome, fitness] for chromosome, fitness in zip(generation, fitness_scores)]
		survivors = sorted(survivors, key=lambda survivor: survivor[1])[:population]
		generation = [survivor[0] for survivor in survivors]
		fitness_scores = fitness(result, powers, generation)
		new_selection_results = selection(fitness_scores)
		average_fitness = fitness_average(fitness_scores, new_selection_results)

	return [generation, new_selection_results, fitness_scores, average_fitness]

def genetic_algorithm(data: str, generations_limit: int, population: int):
	powers, result = read_powers(data)
	equation_form = get_equation_form(powers, result)
	
	next_generation = initial_generation = generation(population)
	fitness_scores = fitness(result, powers, initial_generation)
	selection_results = selection(fitness_scores)
	average_fitness = fitness_average(fitness_scores, selection_results)

	average_chromosomes = [average_fitness]
	best_chromosomes = [min(fitness_scores)]

	generations_count = 0
	while True:
		if generations_count > generations_limit:
			generations_count = 0
			
			next_generation = initial_generation = generation(population)
			fitness_scores = fitness(result, powers, initial_generation)
			selection_results = selection(fitness_scores)
			average_fitness = fitness_average(fitness_scores, selection_results)

			average_chromosomes = []
			best_chromosomes = []
			continue

		crossover_generation, crossover_selection_results, crossover_fitness_scores, crossover_average_fitness = crossover(result, powers, population, next_generation, selection_results)
		
		mutation_generation, mutation_selection_results, mutation_fitness_scores, mutation_average_fitness = mutation(result, powers, population, crossover_generation, crossover_selection_results)
		
		generations_count += 1
		selection_results = mutation_selection_results
		next_generation = mutation_generation
		fitness_scores, average_fitness = mutation_fitness_scores, mutation_average_fitness
		best_chromosomes.append(min(fitness_scores))
		average_chromosomes.append(average_fitness)

		if 0 in fitness_scores:
			solution = next_generation[fitness_scores.index(0)] 
			print(f'Solution for {equation_form}:\n {solution}\nGenerations count: {generations_count}\n')
			plot(average_chromosomes, best_chromosomes)
			break



# TASK 5

# START
# Generate the initial population
# Compute fitness
# REPEAT
#     Selection
#     Crossover
#     Mutation
#     Compute fitness
# UNTIL population has converged
# STOP

def task_5():
	genetic_algorithm('equation_1.txt', 20, 10)
	genetic_algorithm('equation_2.txt', 20, 10)



if __name__ == '__main__':
	task_5()