'''
Задание 6.1. 
Окрасить граф G с помощью "жадного" алгоритма.

Задание 6.2. 
Окрасить граф G с помощью алгоритма DSatur.
'''

from copy import deepcopy
from random import randint
from math import pi, sin, cos
import matplotlib.pyplot as plt



# USEFUL FUNCTIONS

def random_color():
	letters = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f'}
	color = '#'
	for i in range(6):
		if randint(0, 1000) < 375:
			color += letters[randint(0, 5)]
		else:
			color += str(randint(0, 9))

	return color

def generate_graph(N: int) -> list:
	graph = [[0] * int(N) for i in range(N)]

	for i, row in enumerate(graph):
		for j, element in enumerate(row):
			if i == j:
				graph[i][j] = 1
				break
			graph[i][j] = graph[j][i] = randint(0, 1) 

	return graph

def draw_line_segment(point_1, point_2):
	plt.plot([point_1[0], point_2[0]],[point_1[1], point_2[1]], c = 'gray')

def plot_graph(graph: list, vertices:list, colors = None):
	for i, row in enumerate(graph):
		for j, element in enumerate(row):
			if i == j:
				break
			if graph[i][j]:
				draw_line_segment(vertices[i], vertices[j])

	if colors:
		for color, coordinates in enumerate(colors):
			if coordinates:
				c = random_color()
				for vertex in coordinates:
					x, y = vertices[vertex]
					plt.scatter(x, y, s = 100, c = c)
					plt.text(x+.05, y+.05, color, fontsize=20)
	else:
		for x, y in vertices:
			plt.scatter(x, y, s = 100, c = '#000')

	plt.show()

def or_sum(a: list, b: list):
	return [1 if 1 in [a[i], b[i]] else 0 for i in range(len(a))]



# GREEDY ALGORITHM

def greedy(graph: list) -> list:
	colors = [[] for i in range(len(graph))]
	stop = [None] * len(graph)
	filled = [1] * len(graph)

	if graph == [filled] * len(graph):
		return [[i] for i in range(len(graph))]

	colors[0].append(0)
	i = color = 0
	while True:
		if graph == stop:
			return colors

		if graph[i] == filled:
			graph[i] = None
			
			j = i + 1
			while True:
				if j == len(graph):
					return colors
				
				if graph[j] in [filled, None]:
					graph[j] = None
					j += 1
					continue
				else:
					i = j
					color += 1
					colors[color].append(j)
					break

		index = graph[i].index(0)
		if graph[index]: 
			graph[i] = or_sum(graph[i], graph[index])
			colors[color].append(index)
			graph[index] = None
		else:
			graph[i][index] = 1



# DSATUR ALGORITHM

def dsatur(graph: list) -> list:
	pass

    

# TASK 6.1

def task_6_1():
	N = 30
	angle = 2 * pi / N	
	GRAPH = generate_graph(N)
	GRAPH_COPY = deepcopy(GRAPH)
	vertices_coordinates = [[cos(i * angle) * len(GRAPH), sin(i * angle) * len(GRAPH)] for i in range(len(GRAPH))]
	colors = greedy(GRAPH_COPY)

	plot_graph(GRAPH, vertices_coordinates)
	print('Colors:')
	for i, vertices in enumerate(colors):
		if vertices:
			print(f"{i}: {' '.join(map(str, vertices))}") 
	plot_graph(GRAPH, vertices_coordinates, colors = colors)
	


# TASK 6.2

def task_6_2():
	GRAPH = []

	dsatur(GRAPH)


if __name__ == '__main__':
	task_6_1()
	task_6_2()