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

def vertex_neighbours(graph: list, vertex: int) -> list:
	return [index for index in range(len(graph[vertex])) if graph[vertex][index]]

def get_amount_color(colored: list, vertices: list, color_number: int) -> int:
    color_counter = 0;  
    for vertex in vertices:
        if (colored[vertex] == color_number):
            color_counter += 1;
    
    return color_counter;



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
    degrees = list()
    saturation_degrees = [0] * len(graph)    
    colored = [0] * len(graph)
    uncolored_vertices = set(range(len(graph)))
    
    color_counter = index_maximum_degree = maximum_degree = 0
    for i, row in enumerate(graph):
        degrees.append((sum(row), i))
        
        if (degrees[i][0] > maximum_degree):
            (maximum_degree, vertex) = degrees[i]
            index_maximum_degree = i    

    neighbours = vertex_neighbours(graph, index_maximum_degree)
    for neighbour in neighbours:
        saturation_degrees[neighbour] += 1
    
    colored[index_maximum_degree] = color_counter
    uncolored_vertices.remove(index_maximum_degree)

    while uncolored_vertices:
        max_saturation_degree = -1
        for vertex in uncolored_vertices:
            if (saturation_degrees[vertex] > max_saturation_degree):
                max_saturation_degree = saturation_degrees[vertex]
        
        max_saturation_degrees = [vertex for vertex in uncolored_vertices if saturation_degrees[vertex] == max_saturation_degree]           

        coloring_index = max_saturation_degrees[0]
        if len(max_saturation_degrees) > 1: 
            maximum_degree = -1
            for i in max_saturation_degrees:
                (degree, vertex_index) = degrees[i]
                if (degree > maximum_degree):
                    coloring_index = vertex_index
                    maximum_degree = degree
        
        vertex_index_neighbours = vertex_neighbours(graph, coloring_index)
        for number_color in range(1, color_counter + 1, 1):
            if (get_amount_color(colored, vertex_index_neighbours, number_color) == 0):
                colored[coloring_index] = number_color
                break
                
        if not colored[coloring_index]:
            color_counter += 1
            colored[coloring_index] = color_counter
        
        uncolored_vertices.remove(coloring_index)
        
        for neighbour in vertex_index_neighbours:
            subneighbours = vertex_neighbours(graph, neighbour)
            
            if (get_amount_color(colored, subneighbours, colored[coloring_index]) == 1):
                saturation_degrees[neighbour] += 1;   

    colors = [[] for i in range(len(graph))]
    for vertex, i in enumerate(colored):
    	colors[i].append(vertex)

    return colors



# TASK 6.1

def task_6_1():
	N = 30
	angle = 2 * pi / N	
	GRAPH = generate_graph(N)
	GRAPH_COPY = deepcopy(GRAPH)
	vertices_coordinates = [[cos(i * angle) * len(GRAPH), sin(i * angle) * len(GRAPH)] for i in range(len(GRAPH))]
	colors = greedy(GRAPH_COPY)

	plot_graph(GRAPH, vertices_coordinates)
	print('Colors for Greedy Algorithm:')
	for i, vertices in enumerate(colors):
		if vertices:
			print(f"{i}: {' '.join(map(str, vertices))}") 
	plot_graph(GRAPH, vertices_coordinates, colors = colors)
	


# TASK 6.2

def task_6_2():
	N = 30
	angle = 2 * pi / N	
	GRAPH = generate_graph(N)
	vertices_coordinates = [[cos(i * angle) * len(GRAPH), sin(i * angle) * len(GRAPH)] for i in range(len(GRAPH))]
	colors = dsatur(GRAPH)

	plot_graph(GRAPH, vertices_coordinates)
	print('Colors for DSatur Algorithm:')
	for i, vertices in enumerate(colors):
		if vertices:
			print(f"{i}: {' '.join(map(str, vertices))}") 
	plot_graph(GRAPH, vertices_coordinates, colors = colors)



if __name__ == '__main__':
	task_6_1()
	task_6_2()
