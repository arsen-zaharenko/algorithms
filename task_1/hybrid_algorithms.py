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



# HYBRID QUICK-INSERTION SORT FOR TASK 1.3

def modifying_hybrid_quick_sort(array: list, left: int, right: int, k: int, counter: list):
	if len(array) == 1:
		#-------------#
		counter[0] += 2
		#-------------#
		return	
	if right - left + 1 < k:
		temp = array[left:right + 1]
		insertion_sort(temp)
		for i in range(left, right + 1):
			array[i] = temp[i - left]
		#-----------------------------------------------------#
		counter[0] += len(temp)**2 + (right - left + 2) * 5 + 2
		#-----------------------------------------------------#
	elif left < right:
		p = partition(array, left, right)
		modifying_hybrid_quick_sort(array, left, p - 1, k, counter)
		modifying_hybrid_quick_sort(array, p + 1, right, k, counter)
		#----------------------------------#
		counter[0] += (right - left + 2) * 9
		#----------------------------------#



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



# HYBRID MERGE-INSERTION SORT FOR TASK 1.3

def modifying_hybrid_merge_sort(array: list, k: int, counter: list):
	if len(array) > 1:
		mid = len(array) // 2

		L = array[:mid]
		R = array[mid:]
		#--------------------------#
		counter[0] += 9 + len(array)
		#--------------------------# 
		if len(L) < k:
			insertion_sort(L)
			#-------------------------#
			counter[0] += len(L)**2 + 2
			#-------------------------#
		else:
			modifying_hybrid_merge_sort(L, k, counter)
			#-------------#
			counter[0] += 1
			#-------------#

		if len(R) < k:
			insertion_sort(R)
			#-------------------------#
			counter[0] += len(R)**2 + 2
			#-------------------------#
		else:
			modifying_hybrid_merge_sort(R, k,counter)
			#-------------#
			counter[0] += 1
			#-------------#

		i = j = k = 0
		#-------------#
		counter[0] += 3
		#-------------#
		while i < len(L) and j < len(R):
			if L[i] < R[j]:
				array[k] = L[i]
				i += 1
				#-------------#
				counter[0] += 8
				#-------------#
			else:
				array[k] = R[j]
				j += 1
				#-------------#
				counter[0] += 5
				#-------------#
			k += 1
			#-------------#
			counter[0] += 7
			#-------------#	

		while i < len(L):
			array[k] = L[i]
			i += 1
			k += 1
			#-------------#
			counter[0] += 9
			#-------------#

		while j < len(R):
			array[k] = R[j]
			j += 1
			k += 1
			#-------------#
			counter[0] += 9
			#-------------#



# TASK 1.1 (сортировка оптимальна при k = 20)

def task_1_1(R: int, N: int, M: int):
	arrays = [[randint(0, M) for i in range(N)] for j in range(R)]
	time_sum = 0

	for array in arrays:
		start_time = time()
		hybrid_quick_sort(array, left = 0, right = len(array) - 1, k = 20)
		time_sum += time() - start_time
	
	print(f'Average time for hybrid Quick-Insertion sort: {time_sum / len(arrays):.{4}f}', end = '\n\n')



# TASK 1.2 (сортировка оптимальна при k = 20)

def task_1_2(R: int, N: int, M: int):
	arrays = [[randint(0, M) for i in range(N)] for j in range(R)]
	time_sum = 0

	for array in arrays:
		start_time = time()
		hybrid_merge_sort(array, k = 20)
		time_sum += time() - start_time
	
	print(f'Average Time for hybrid Merge-Insertion sort: {time_sum / len(arrays):.{4}f}', end = '\n\n')



'''
TASK 1.3 

"Цена" операций:
	1. арифметические операции -> 1
	2. логические операции -> 1
	3. операция присваивания -> 1
	4. операции сравнения -> 1
	4. вызов функции -> 1
	5. обращение к элементу по индексу -> 1  
	6. срез списка list[n:m], где n <= m -> m - n + 1
'''

def task_1_3(N: int, M: int):
	array = [randint(0, M) for i in range(N)]
	counter = [0]
	modifying_hybrid_quick_sort(array, left = 0, right = len(array) - 1, k = 20, counter = counter)
	print(f'Number of operation for hybrid Quick-Insertion sort: {counter[0]}', end = '\n\n')

	array = [randint(0, M) for i in range(N)]
	counter = [0]
	modifying_hybrid_merge_sort(array, k = 20, counter = counter)
	print(f'Number of operation for hybrid Merge-Insertion sort: {counter[0]}', end = '\n\n')



# Требуется отсортировать R массивов длины N со значениями из отрезка [0, M]. 

if __name__ == '__main__':
	task_1_1(R = 50, N = 100000, M = 500000)
	task_1_2(R = 50, N = 100000, M = 500000)
	task_1_3(N = 100000, M = 500000)
