'''
Задание 2.1.
Реализовать алгоритмы бинарного и интерполяционного поиска числа x в массиве длины N,
элементы которых - случайные целые числа в диапазоне от 0 до M.
Вывести число операций сравнения, выполненных алгоритмом для заданных N, M и x.

Задание 2.2.
Реализовать алгоритмы построения, обхода и балансировки дерева бинарного поиска (BST).
На вход алгоритма подается последовательность целых положительных чисел a_1,a_2,...,a_n.
Программа должна строить BST, добавляя узлы в порядке последовательности.
Реализовать обходы дерева по возрастанию узлов и по убыванию узлов.
Реализовать алгоритм нахождения k-го минимального ключа в дереве;
на его основе сбалансировать построенное дерево (ротациями вправо и влево n/2-минимальный элемент помещается в корень,
затем данная процедура рекурсивно повторяется для поддеревьев с корнями в дочерних узлах).

Задание 2.3.
Реализовать алгоритм хеширования методом умножения с разрешением коллизий цепочками переполнения,
линейного зондирования и двойным хешированием. 
В вычислительном эксперименте подобрать свою константу для метода умножения,
сравнить ее с константой Кнута по наибольшей длине цепочек коллизий (множества ключей с равным хеш-значением)
для P наборов из N случайных ключей от 1 до R, при длине хеш-таблицы M.
'''

from random import randint



# SEARCH ALGORITHMS

def binary_search(array: list, left: int, right: int, x: int, counter: list) -> int:
	if right >= left:
		mid = left + (right - left) // 2
		counter[0] += 1

		if array[mid] == x:
			return mid
		elif array[mid] > x:
			return binary_search(array, left, mid - 1, x, counter)
		else:
			return binary_search(array, mid + 1, right, x, counter)
	
	return -1



def interpolation_search(array: list, left: int, right: int, x: int, counter: list) -> int:
	if left <= right and array[left] <= x <= array[right]:
		inter = left + (right - left) * (x - array[left]) // (array[right] - array[left]) 
		counter[0] += 1

		if array[inter] == x:
			return inter
		elif array[inter] > x:
			return interpolation_search(array, left, inter - 1, x, counter)
		else:
			return interpolation_search(array, inter + 1, right, x, counter)
	
	return -1



# TASK 2.1

def task_2_1(x: int, N: int, M: int):
	array = [randint(0, M) for i in range(N)]
	array.sort()

	counter = [0]
	print(binary_search(array, left = 0, right = len(array) - 1, x = int(input()), counter = counter))
	print(f'Найдено за {counter[0]} итераций')



	counter = [0]
	print(interpolation_search(array, left = 0, right = len(array) - 1, x = int(input()), counter = counter))
	print(f'Найдено за {counter[0]} итераций')



# TASK 2.2

def task_2_2():
	pass



# TASK 2.3

def task_2_3():
	pass



# Выполнить: бинарный и интерполяционный поиск, алгоритмы для BST, алгоритм хеширования.

if __name__ == '__main__':
	x = randint(0, 10000000)
	task_2_1(x, N = 10000, M = 1000000)
	task_2_2()
	task_2_3()