'''
Задание 1.1. 
Реализовать один из гибридных алгоритмов,
сочетающий быструю сортировку и сортировку вставками следующим образом: в алгоритме быстрой сортировки,
участки массива длины меньшей некоторого параметра k сортировать сортировкой вставками,
не используя для них рекурсию быстрой сортировки.

Проделать вычислительный эксперимент.
Подобрать оптимальное k для сортировки R массивов длины N,
элементы которых - случайные целые числа в диапазоне от 0 до M.

Дать возможность пользователю задавать параметры R,N и M.

Задание 1.2. 
Реализовать один из гибридных алгоритмов, 
сочетающий сортировку слиянием и сортировку вставками следующим образом: в алгоритме сортировки слиянием,
участки массива длины меньшей некоторого параметра k сортировать сортировкой вставками,
не используя для них рекурсию сортировки слиянием.

Проделать вычислительный эксперимент.
Подобрать оптимальное k для сортировки R массивов длины N,
элементы которых - случайные целые числа в диапазоне от 0 до M.

Дать возможность пользователю задавать параметры R,N и M.

Задание 1.3. 
Подсчитать число элементарных операций в вашей реализации сортировки вставками.
'''

from random import randint
from time import time

def quick_sort(array: list):
	pass

def insertion_sort(array: list):
	for i in range(1, len(array)):
		key = array[i]

		j = i - 1
		while j >= 0 and key < array[j] :
			array[j + 1] = array[j]
			j -= 1
		array[j + 1] = key

def merge_sort(array: list):
	if len(array) > 1:
		mid = len(array) // 2

		L = array[:mid]
		R = array[mid:]

		merge_sort(L)
		merge_sort(R)

		i = j = k = 0

		while i < len(L) and j < len(R):
			if L[i] < R[j]:
				array[k] = L[i]
				i += 1
			else:
				array[k] = R[j]
				j += 1
			k += 1	

		while i < len(L):
			array[k] = L[i]
			i += 1
			k += 1

		while j < len(R):
			array[k] = R[j]
			j += 1
			k += 1

def hybrid_merge_sort(array: list, k: int):
	if len(array) > 1:
		mid = len(array) // 2

		L = array[:mid]
		R = array[mid:]

		insertion_sort(L) if len(L) < k else hybrid_merge_sort(L, k)
		insertion_sort(R) if len(R) < k else hybrid_merge_sort(R, k)

		i = j = k = 0

		while i < len(L) and j < len(R):
			if L[i] < R[j]:
				array[k] = L[i]
				i += 1
			else:
				array[k] = R[j]
				j += 1
			k += 1	

		while i < len(L):
			array[k] = L[i]
			i += 1
			k += 1

		while j < len(R):
			array[k] = R[j]
			j += 1
			k += 1

def task_1(R: int, N: int, M: int):
	arrays = [[randint(0, M) for i in range(N)] for j in range(R)]
	
	for array in arrays:
		hybrid_quick_sort(array, k)

def task_2(R: int, N: int, M: int):
	arrays = [[randint(0, M) for i in range(N)] for j in range(R)]
	
	for array in arrays:
		print(f'Origin: {array}')
		start_time = time()
		hybrid_merge_sort(array, k = 3)
		print(f'Sorted: {array}')
		print(f'Time: {time() - start_time}', end = '\n\n')



# Требуется отсортировать R массивов длины N со значениями из отрезка [0, M]. 

if __name__ == '__main__':
	task_2(R = 5, N = 20, M = 50)