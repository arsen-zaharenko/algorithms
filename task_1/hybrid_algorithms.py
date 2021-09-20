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



# QUICK SORT

def partition(array: list, left: int, right: int) -> int:
	i = left - 1
	pivot = array[right]

	for j in range(left, right):
		if array[j] <= pivot:
			i += 1
			array[i], array[j] = array[j], array[i]
	array[i + 1], array[right] = array[right], array[i + 1]

	return i + 1

def quick_sort(array: list, left: int, right: int):
	if len(array) == 1:
		return	
	if left < right:
		p = partition(array, left, right)
		quick_sort(array, left, p - 1)
		quick_sort(array, p + 1, right)



# INSERTION SORT

def insertion_sort(array: list):
	for i in range(1, len(array)):
		key = array[i]

		j = i - 1
		while j >= 0 and key < array[j] :
			array[j + 1] = array[j]
			j -= 1
		array[j + 1] = key



# MERGE SORT

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



# HYBRID QUICK-INSERTION SORT

def hybrid_quick_sort(array: list, left: int, right: int, k: int):
	if len(array) == 1:
		return	
	if right - left + 1 < k:
		temp = array[left:right + 1]
		insertion_sort(temp)
		for i in range(left, right + 1):
			array[i] = temp[i - left]
	elif left < right:
		p = partition(array, left, right)
		hybrid_quick_sort(array, left, p - 1, k)
		hybrid_quick_sort(array, p + 1, right, k)



# HYBRID MERGE-INSERTION SORT

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



# TASK 1.1 (сортировка оптимальна при k из отрезка [7, 49])

def task_1_1(R: int, N: int, M: int):
	arrays = [[randint(0, M) for i in range(N)] for j in range(R)]
	
	for array in arrays:
		print(f'Origin: {array}')
		start_time = time()
		hybrid_quick_sort(array, left = 0, right = len(array) - 1, k = randint(7, 49))
		print(f'Sorted: {array}')
		print(f'Time: {time() - start_time}', end = '\n\n')



# TASK 1.2 (сортировка оптимальна при k из отрезка [2, 125])

def task_1_2(R: int, N: int, M: int):
	arrays = [[randint(0, M) for i in range(N)] for j in range(R)]
	
	for array in arrays:
		print(f'Origin: {array}')
		start_time = time()
		hybrid_merge_sort(array, k = randint(2, 125))
		print(f'Sorted: {array}')
		print(f'Time: {time() - start_time}', end = '\n\n')



# Требуется отсортировать R массивов длины N со значениями из отрезка [0, M]. 

if __name__ == '__main__':
	task_1_1(R = 5, N = 1000, M = 5000)
	task_1_2(R = 5, N = 1000, M = 5000)
