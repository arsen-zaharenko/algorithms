'''
Задание 5.
Решить диофантовое уравнение, используя генетический алгоритм.
''' 

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

def function(variables: list, powers: list) -> int:
	u, w, x, y, z = variables
	u_pows, w_pows, x_pows, y_pows, z_pows = powers

	return sum([(u**u_pows[i]) * (w**w_pows[i]) * (x**x_pows[i]) * (y**y_pows[i]) * (z**z_pows[i]) for i in range(len(u_pows))])
	


# GENETIC ALGHORITHM

def generation():
	return [[randint(-3, 3) for i in range(5)] for j in range(5)]

def fitness(result: int, powers: list, generation: list) -> list:
	fitness_scores = [abs(function(chromosome, powers) - result) for i, chromosome in enumerate(generation)]
	average_fitness = sum(fitness_scores) / len(fitness_scores)

	return [fitness_scores, average_fitness]

def selection(fitness_scores: list, average_fitness: float) -> list:
	survival_coefficient = sum([1 / score for score in fitness_scores])
	survival_probabilities = [1 / score / survival_coefficient for score in fitness_scores]

	return [survival_coefficient, survival_probabilities]

def crossover(generation: list, selection_results: list) -> list:
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

	return new_generation

def mutation(generation: list):
	for chromosome in generation:
		chromosome[randint(0, 4)] += randint(-3, 3)

	return generation


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
	powers, result = read_powers('1.txt')
	equation_form = get_equation_form(powers, result)
	
	initial_generation = generation()
	fitness_scores, average_score = fitness(result, powers, initial_generation)

	previous_generation = next_generation = initial_generation
	generations_count = 1
	while True:
		generations_count += 1
		selection_results = selection(fitness_scores, average_score)
		next_generation = mutation(crossover(previous_generation, selection_results))
		previous_generation = next_generation
		fitness_scores, average_score = fitness(result, powers, next_generation)
		
		if 0 in fitness_scores:
			solution = next_generation[fitness_scores.index(0)] 
			print(f'Solution: {solution}\nGenerations count: {generations_count}')
			break

if __name__ == '__main__':
	task_5()
	powers, result = read_powers('1.txt')
	print(function([0, -18, -2, 0, -5], powers))