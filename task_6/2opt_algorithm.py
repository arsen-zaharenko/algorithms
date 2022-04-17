'''
Задание 6.
Задан полный граф G(V,E) на N вершинах и весовая функция w: E -> R, w(ij) >= 0 для всех ребер.
Граф задан матрицей W, где W[i,j] - вес w(ij) ребра ij.
Реализовать алгоритм 2-замены для задачи коммивояжера для графа G.
'''

from random import randint, sample



# USEFUL FUNCTIONS

def generate_graph(N: int):
	graph = [[0] * int(N) for i in range(N)]

	for i, row in enumerate(graph):
		for j, element in enumerate(row):
			if i == j:
				break
			graph[i][j] = graph[j][i] = randint(0, N) 

	return graph

def cost(graph: list, route: list) -> int:
	return sum([graph[route[i]][route[i + 1]] for i in range(len(route) - 1)]) + graph[route[-1]][route[0]]



# 2-OPT ALGORITHM

def two_opt(graph: list, route: list, steps=False) -> list:
	best = route
	improved = True
	iterations = 0

	while improved:
		improved = False

		for i in range(1, len(route)):
			for j in range(i, len(route)):
				if j - i == 1:
					iterations += 1
					if steps:
						print(f'Iteration {iterations}: \n\tRoute: {" ".join(map(str, best))}\n\tCost: {cost(graph, best)}') 
					continue
		
				new_route = route[:]
				new_route[i:j] = route[j - 1: i - 1: -1] 
		
				if cost(graph, new_route) < cost(graph, best):
					best = new_route
					improved = True

				iterations += 1
				if steps:
					print(f'Iteration {iterations}: \n\tRoute: {" ".join(map(str, best))}\n\tCost: {cost(graph, best)}')

	return [best, cost(graph, best), iterations]



# TASK 6

def task_6():
	N = 5

	GRAPH = generate_graph(N)
	route = sample(range(N), N)

	print('Cost matrix:')
	for row in GRAPH:
		print(' '.join(map(str, row)))

	print(f'\nInitial route: {" ".join(map(str, route))}\nCost:{cost(GRAPH, route)}\n')
	
	best_route, best_cost, iterations = two_opt(GRAPH, route)

	print(f'The best route found in {iterations} iterations.\nRoute: {" ".join(map(str, best_route))}\nCost: {best_cost}')


		
if __name__ == '__main__':
	task_6()