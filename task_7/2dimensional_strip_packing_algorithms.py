'''
Задание 7. 
Нужно реализовать Next Fit, First Fit, Best Fit, Split Fit и проверить их на разных наборах многоугольников: 
1. генерировать примерно одинаковые по соотношению стороны, например, 2:3 ± константа.
2. генерировать вытянутые по соотношению стороны, например, 1:2 ± константа.
'''

from copy import deepcopy
from random import randint
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle



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

def draw_line_segment(point_1, point_2):
	plt.plot([point_1[0], point_2[0]],[point_1[1], point_2[1]], c = 'black')

def calculate_average_rating(N: int, ratio: list):
	n_f = f_f = b_f = s_f = 0
	for i in range(N):
		n = 30
		container_width = randint(25, 40)
		boxes = [generate_box(ratio) for i in range(n)]

		n_f += calculate_rating(container_width, next_fit(container_width, boxes=deepcopy(boxes)))
		f_f += calculate_rating(container_width, first_fit(container_width, boxes=deepcopy(boxes)))
		b_f += calculate_rating(container_width, best_fit(container_width, boxes=deepcopy(boxes)))
		s_f += calculate_rating(container_width, split_fit(container_width, boxes=deepcopy(boxes)))

	return [round(i / N, 3) for i in [n_f, f_f, b_f, s_f]]

def calculate_rating(container_width: int, levels: list):
	height = 0
	boxes_area = 0
	if type(levels[0][0][0]) in [type(0.0), type(0)]:
		for level in levels:
			height += level[0][1]
			for box in level:
				boxes_area += box[0] * box[1]
	else:
		initial_levels, remaining_levels, inner_levels, inner_container_coordinates = levels

		levels = initial_levels + remaining_levels
		for level in levels:
			height += level[0][1]
			for box in level:
				boxes_area += box[0] * box[1]

		for level in inner_levels:
			for box in level:
				boxes_area += box[0] * box[1]

	return round(boxes_area / height / container_width, 3)

def draw_container(x: int, y: int, width: int):
	draw_line_segment([x, y], [x + width, y])
	draw_line_segment([x, y], [x, y + 150])
	draw_line_segment([x + width, y], [x + width, y + 150])

def generate_box(ratio: list):
	unit_size = randint(1, 5)	
	if randint(0, 1):
		return [round(unit_size * ratio[0], 1), round(unit_size * (ratio[1] + randint(0, 9) * 0.1), 1)]
	return [round(unit_size * (ratio[1] + randint(0, 9) * 0.1), 1), round(unit_size * ratio[0], 1)]

def packing_boxes(x: int, y: int, container_width: int, levels: list , plot, text='', show=False):
	draw_container(x, y, container_width)

	if type(levels[0][0][0]) in [type(0.0), type(0)]:
		height = y
		for level in levels:
			width = x
			for box in level:
				plot.add_patch(Rectangle([width, height], box[0], box[1], color=random_color()))
				width += box[0]

			height += level[0][1]
	else:
		initial_levels, remaining_levels, inner_levels, inner_container_coordinates = levels

		levels = initial_levels + remaining_levels
		height = y
		for level in levels:
			width = x
			for box in level:
				plot.add_patch(Rectangle([width, height], box[0], box[1], color=random_color()))
				width += box[0]

			height += level[0][1]

		height = y + inner_container_coordinates[1]
		for level in inner_levels:
			width = x + inner_container_coordinates[0]
			for box in level:
				plot.add_patch(Rectangle([width, height], box[0], box[1], color=random_color()))
				width += box[0]

			height += level[0][1]	

	plt.text(x, y - 10, text, fontsize=14)

	if show:
		plt.xlim([x, 150])
		plt.ylim([y, 150])

		plt.show()

def compare_packing(container_width: int,  results: list):
	fig, ax = plt.subplots()
	text = ['Next Fit', 'First Fit', 'Best Fit', 'Split Fit']

	x = 0
	y = 0 
	for i, result in enumerate(results):
		rating = calculate_rating(container_width, result)
		packing_boxes(x, y, container_width, result, ax, text=f'{text[i]}: {rating}')
		x += container_width + 10

	plt.xlim([-15, x + 5])
	plt.ylim([y - 15, 165])

	plt.show()



# 2-DIMENSIONAL STRIP PACKING ALGORITHMS

def next_fit(container_width: int, boxes: list) -> list:
	boxes = sorted(boxes, key=lambda box: -box[1])

	level = 0
	levels = [[]]
	remaining_width = container_width
	for box in boxes:
		if not levels[level]:
			levels[level].append(box)
			remaining_width -= box[0]
			continue

		if remaining_width < box[0]:
			levels.append([box])
			level += 1
			remaining_width = container_width - box[0]
			continue

		levels[level].append(box)
		remaining_width -= box[0]

	return levels

def first_fit(container_width: int, boxes: list) -> list:
	boxes = sorted(boxes, key=lambda box: -box[1])

	level = 0
	levels = [[]] 
	remaining_widths = [container_width]
	for box in boxes:
		if not levels[level]:
			levels[level].append(box)
			remaining_widths[level] -= box[0]
			continue

		not_added = True
		for i in range(len(levels)):
			if remaining_widths[i] < box[0]:
				continue

			levels[i].append(box)
			remaining_widths[i] -= box[0]
			not_added = False
			break

		if not_added:
			level += 1
			levels.append([box])
			remaining_widths.append(container_width - box[0])

	return levels

def best_fit(container_width: int, boxes: list) -> list:
	boxes = sorted(boxes, key=lambda box: -box[1])

	level = 0
	levels = [[]]
	remaining_widths = [container_width]
	for box in boxes:
		if not levels[level]:
			levels[level].append(box)
			remaining_widths[level] -= box[0]
			continue

		best_levels = sorted([[i, remaining_widths[i] - box[0]] for i in range(len(levels))], key=lambda remaining_width: remaining_width[1])
		
		best_level = None
		for i in best_levels:
			if i[1] >= 0:
				best_level = i
				break
			
		if not best_level:
			level += 1
			levels.append([box])
			remaining_widths.append(container_width - box[0])
		else:
			levels[best_level[0]].append(box)
			remaining_widths[best_level[0]] = best_level[1]

	return levels

def split_fit(container_width: int, boxes: list) -> list:
	greater_than_half = []
	remaining_boxes = []
	for box in boxes:
		if 2 * box[0] > container_width:
			greater_than_half.append(box)
		else:
			remaining_boxes.append(box)

	greater_than_half_and_less_than_two_third = []
	greater_than_two_third = []
	for box in greater_than_half:
		if 3 * box[0] > 2 * container_width:
			greater_than_two_third.append(box)
		else:
			greater_than_half_and_less_than_two_third.append(box)

	zero_levels = []
	if greater_than_two_third:
		zero_levels = [level for level in first_fit(container_width, greater_than_two_third) if level]
	
	first_levels = []
	if greater_than_half_and_less_than_two_third:
		first_levels = [level for level in first_fit(container_width, greater_than_half_and_less_than_two_third) if level]

	inner_container = None
	if first_levels:
		width = container_width - max([level[0][0] for level in first_levels])
		height = sum([level[0][1] for level in first_levels])
		inner_container = [width, height]

		remaining_boxes = sorted(remaining_boxes, key=lambda box: -box[1])

		level = 0
		inner_levels = [[]] 
		remaining_widths = [inner_container[0]]
		levels_heights = []
		remaining_height = inner_container[1]
		not_added_boxes = []
		for box in remaining_boxes:
			if box[1] > inner_container[1]:
				not_added_boxes.append(box)
				continue

			if not inner_levels[level]:
				if box[0] > remaining_widths[level]:
					not_added_boxes.append(box)
					continue
				inner_levels[level].append(box)
				remaining_widths[level] -= box[0]
				levels_heights.append(box[1])
				remaining_height -= box[1]
				continue

			not_added = True
			for i in range(len(inner_levels)):
				if remaining_widths[i] < box[0]:
					continue

				if levels_heights[i] < box[1]:
					continue

				inner_levels[i].append(box)
				remaining_widths[i] -= box[0]
				not_added = False
				break

			if not_added:
				if box[1] > remaining_height:
					not_added_boxes.append(box)
				elif box[0] > inner_container[0]:
					not_added_boxes.append(box)
				else:
					level += 1
					inner_levels.append([box])
					remaining_widths.append(inner_container[0] - box[0])
					levels_heights.append(box[1])
					remaining_height -= box[1]

	initial_levels = zero_levels + first_levels

	if not initial_levels or not first_levels:
		return first_fit(container_width, boxes)

	inner_container_coordinates = [max([level[0][0] for level in first_levels]), 0 if not zero_levels else sum([level[0][1] for level in zero_levels])]

	return [initial_levels, first_fit(container_width, remaining_boxes), inner_levels, inner_container_coordinates]



# TASK 7

def task_7():
	N = 30
 
	container_width = randint(25, 40)
	elongated_boxes = [generate_box([2, 4]) for i in range(N)]
	almost_equal_boxes = [generate_box([2, 3]) for i in range(N)]
	
	elongated_boxes_results = [
		next_fit(container_width, boxes=deepcopy(elongated_boxes)),
		first_fit(container_width, boxes=deepcopy(elongated_boxes)),
		best_fit(container_width, boxes=deepcopy(elongated_boxes)),
		split_fit(container_width, boxes=deepcopy(elongated_boxes))
	]

	almost_equal_boxes_results = [
		next_fit(container_width, boxes=deepcopy(almost_equal_boxes)),
		first_fit(container_width, boxes=deepcopy(almost_equal_boxes)),
		best_fit(container_width, boxes=deepcopy(almost_equal_boxes)),
		split_fit(container_width, boxes=deepcopy(almost_equal_boxes))
	]

	compare_packing(container_width, elongated_boxes_results)
	compare_packing(container_width, almost_equal_boxes_results)

	N = 1_000

	n_f, f_f, b_f, s_f = calculate_average_rating(N, [2, 4])
	print(f'Average ratings for boxes with ratio ~1:2\nNext Fit: {n_f}\nFirst Fit: {f_f}\nBest_Fit: {b_f}\nSplit Fit: {s_f}', end='\n\n')

	n_f, f_f, b_f, s_f = calculate_average_rating(N, [2, 3])
	print(f'Average ratings for boxes with ratio ~2:3\nNext Fit: {n_f}\nFirst Fit: {f_f}\nBest_Fit: {b_f}\nSplit Fit: {s_f}')
	


if __name__ == '__main__':
	task_7()