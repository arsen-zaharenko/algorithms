'''
Задание 2.1.
Реализовать алгоритмы бинарного и интерполяционного поиска числа x в массиве длины N,
элементы которых - случайные целые числа в диапазоне от 0 до M.
Вывести число операций сравнения, выполненных алгоритмом для заданных N, M и x.

Задание 2.2.
Реализовать алгоритмы построения, обхода и балансировки дерева бинарного поиска (BST).
На вход алгоритма подается последовательность целых положительных чисел a_1, a_2, ..., a_n.
Программа должна строить BST, добавляя узлы в порядке последовательности.
Реализовать обходы дерева по возрастанию узлов и по убыванию узлов.
Реализовать алгоритм нахождения k-го минимального ключа в дереве;
на его основе сбалансировать построенное дерево (ротациями вправо и влево n/2-минимальный элемент помещается в корень,
затем данная процедура рекурсивно повторяется для поддеревьев с корнями в дочерних узлах).

Задание 2.3.
Реализовать алгоритм хеширования методом умножения с разрешением коллизий цепочками переполнения,
линейного зондирования и двойным хешированием. 
В вычислительном эксперименте подобрать свою константу для метода умножения,
сравнить ее с константой Кнута по наибольшей длине цепочек коллизий (множества элементов с равным хеш-значением)
для P наборов из N случайных элементов от 1 до R, при длине хеш-таблицы M.
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



# BST ALGORITHMS

class Node(object):
    def __init__(self, data: int):
        self.data = data
        self.left = None
        self.right = None
        self.height = 1



class BinarySearchTree(object):
    def insert(self, root: object, data: int) -> object:
        if not root:
            return Node(data)
        else:
            if root.data == data:
                return root
            elif root.data < data:
                root.right = self.insert(root.right, data)
            else:
                root.left = self.insert(root.left, data)
        return root

    def search(root: object, data: int) -> object:
        if root is None or root.data == data:
            return root
 
        if root.data < data:
            return self.search(root.right, data)
   
        return self.search(root.left, data)

    def height(self, root: object) -> int:
        if root is None:
            return 0
        hleft = self.height(root.left)
        hright = self.height(root.right)  
		
        if hleft > hright:
            return hleft + 1
		
        return hright + 1

    def is_balanced(self, root: object) -> bool:
        if root is None:
            return True
    
        lheight = self.height(root.left)
        rheight = self.height(root.right)
    
        if(abs(lheight - rheight) > 1):
            return False

        lcheck = self.is_balanced(root.left)
        rcheck = self.is_balanced(root.right)

        if lcheck == rcheck == True:
            return True

    def inorder_traversal(self, root: object):
        if root:
            self.inorder_traversal(root.left)
            print(root.data, end = ' ')
            self.inorder_traversal(root.right)

    def preorder_traversal(self, root: object):
        if root:
            print(root.data, end = ' ')
            self.preorder_traversal(root.left)
            self.preorder_traversal(root.right)

    def postorder_traversal(self, root: object):
        if root:
            self.postorder_traversal(root.left)
            self.postorder_traversal(root.right)
            print(root.data, end = ' ')

		

class AVL_Tree(object):
    def insert(self, root: object, data: int) -> object:
        if not root:
            return Node(data)
        elif data < root.data:
            root.left = self.insert(root.left, data)
        else:
            root.right = self.insert(root.right, data)
 
        root.height = 1 + max(self.height(root.left), self.height(root.right))
 
        balance = self.balance(root)
 
        if balance > 1 and data < root.left.data:
            return self.right_rotate(root)
 
        if balance < -1 and data > root.right.data:
            return self.left_rotate(root)
 
        if balance > 1 and data > root.left.data:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)
 
        if balance < -1 and data < root.right.data:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)
 
        return root
 
    def left_rotate(self, root: object) -> object:
        new_root = root.right
        left_subtree = new_root.left
 
        new_root.left = root
        root.right = left_subtree
 
        root.height = 1 + max(self.height(root.left), self.height(root.right))
        new_root.height = 1 + max(self.height(new_root.left), self.height(new_root.right))

        return new_root
 
    def right_rotate(self, root: object) -> object:
        new_root = root.left
        right_subtree = new_root.right
 
        new_root.right = root
        root.left = right_subtree
 
        root.height = 1 + max(self.height(root.left), self.height(root.right))
        new_root.height = 1 + max(self.height(new_root.left), self.height(new_root.right))
 
        return new_root
 
    def height(self, node: object) -> int:
        if not node:
            return 0
 
        return node.height
 
    def balance(self, node: object) -> int:
        if not node:
            return 0
 
        return self.height(node.left) - self.height(node.right)
 
    def preorder_traversal(self, root: object):
        if root:
            print(root.data, end = ' ')
            self.preorder_traversal(root.left)
            self.preorder_traversal(root.right)



# HASH ALGORITHMS

class HashTable(object):
	def __init__(self, size: int, CONST: float):
		self.size = size
		self.CONST = CONST
		self.dictionary = {}

	def hash(self, key: int) -> int: 
		key *= self.CONST
		return int(self.size * (key - int(key)))

	def double_hash(self, key:int) -> int:
		return self.hash(self.hash(key))

	def add_element(self, element: int):
		hash_of_element = self.hash(element)
		if hash_of_element not in self.dictionary.keys():
			self.dictionary[hash_of_element] = {element}
		else:
			self.dictionary[hash_of_element].add(element)

	def add_element_by_linear_probing(self, element: int, counter: list):
		hash_of_element = self.hash(element)
		if hash_of_element not in self.dictionary.keys():
			self.dictionary[hash_of_element] = {element}
		else:
			for key in range(hash_of_element + 1, self.size):
				counter[0] += 1
				if key not in self.dictionary.keys():
					self.dictionary[key] = {element}
					return
			for key in range(hash_of_element):
				counter[0] += 1
				if key not in self.dictionary.keys():
					self.dictionary[key] = {element}
					return

	def add_element_with_double_hashing(self, element: int):
		double_hash_of_element = self.double_hash(element)
		if double_hash_of_element not in self.dictionary.keys():
			self.dictionary[double_hash_of_element] = {element}
		else:
			self.dictionary[double_hash_of_element].add(element)

	def add_collisions(self, collisions: dict):
		for value in self.dictionary.values():
			if len(value) not in collisions.keys():
				collisions[len(value)] = 1
			else:
				collisions[len(value)] += 1 

	def print(self):
		for key in self.dictionary.keys():
			print(f'{key}: {self.dictionary[key]}')
	


def multiplication_method(P:int, N: int, R: int, M: int, CONST: float):
	KNUTH_CONST = 0.618033988749894

	arrays = [[randint(1, R) for i in range(N)] for j in range(P)]
	collisions = {}

	for array in arrays:
		hash_table = HashTable(M, CONST)

		for element in array:
			hash_table.add_element(element)

		hash_table.add_collisions(collisions)

	collisions_sum = 0
	no_collisions = 0

	for key in collisions.keys():
		if key == 1:
			no_collisions += collisions[key]
			collisions_sum += collisions[key]
		else:
			collisions_sum += collisions[key]

	if CONST == KNUTH_CONST:
		print(f'Средний показатель коллизий для константы Кнута: {100 - 100 * no_collisions / collisions_sum:.{5}f}')
	else:
		print(f'Средний показатель коллизий для моей константы: {100 - 100 * no_collisions / collisions_sum:.{5}f}')



def linear_probing(P:int, N: int, R: int, M: int, CONST: float):
	KNUTH_CONST = 0.618033988749894

	arrays = [[randint(1, R) for i in range(N)] for j in range(P)]
	collisions = {}
	counter = [0]

	for array in arrays:
		hash_table = HashTable(M, CONST)

		for element in array:
			hash_table.add_element_by_linear_probing(element, counter)

		hash_table.add_collisions(collisions)

	if len(collisions) == 1:
		if CONST == KNUTH_CONST:
			print(f'Линейное зондирование прошло успешно для константы Кнута с общим числом поиска: {counter[0]}')
		else:
			print(f'Линейное зондирование прошло успешно для моей константы с общим числом поиска: {counter[0]}')
	else:
		print('Обнаружены коллизии')



def double_hashing(P:int, N: int, R: int, M: int, CONST: float):
	KNUTH_CONST = 0.618033988749894

	arrays = [[randint(1, R) for i in range(N)] for j in range(P)]
	collisions = {}

	for array in arrays:
		hash_table = HashTable(M, CONST)

		for element in array:
			hash_table.add_element_with_double_hashing(element)	

		hash_table.add_collisions(collisions)

	collisions_sum = 0
	no_collisions = 0

	for key in collisions.keys():
		if key == 1:
			no_collisions += collisions[key]
			collisions_sum += collisions[key]
		else:
			collisions_sum += collisions[key]

	if CONST == KNUTH_CONST:
		print(f'Средний показатель коллизий для константы Кнута с двойным хешированием: {100 - 100 * no_collisions / collisions_sum:.{5}f}')
	else:
		print(f'Средний показатель коллизий для моей константы с двойным хешированием: {100 - 100 * no_collisions / collisions_sum:.{5}f}')		



# TASK 2.1

def task_2_1(x: int, N: int, M: int):
	array = [randint(0, M) for i in range(N)]
	array.sort()

	counter = [0]
	index = binary_search(array, left = 0, right = len(array) - 1, x = int(x), counter = counter)
	
	if index == -1:
		print('Бинарным поиск: число отсутствует')
	else:
		print(f'Бинарным поиск (число итераций): {counter[0]}')

	counter = [0]
	index = interpolation_search(array, left = 0, right = len(array) - 1, x = int(x), counter = counter)
	
	if index == -1:
		print('Интерполяционный поиск: число отсутствует', end = '\n\n')
	else:
		print(f'Интерполяционный поиск (число итераций): {counter[0]}', end = '\n\n')



# TASK 2.2

#	 UNBALANCED BST         		   AVL TREE
#
#		  10							  30
# 		   \							 /  \
#  		    20          BALANCING	    20  40	
#   		 \         ---------->     /  \   \
#   		 30						  10  25  50
#  		    /  \
# 		   25  40
#      		    \
#      		    50

def task_2_2():	 
	BST = BinarySearchTree()
	BST_root = None
	AVL = AVL_Tree()
	AVL_root = None

	for data in [10, 20, 30, 40, 50, 25]:
		BST_root = BST.insert(BST_root, data)  
		AVL_root = AVL.insert(AVL_root, data)

	print('Центрированный обход:')
	BST.inorder_traversal(BST_root)
	print('\nПрямой обход:')
	BST.preorder_traversal(BST_root)
	print('\nОбратный обход:')
	BST.postorder_traversal(BST_root) 

	print(f'\nВысота дерева: {BST.height(BST_root)}', end = '\n')
	print('Дерево сбалансированно' if BST.is_balanced(BST_root) else 'Дерево несбалансированно')

	print('\nПрямой обход AVL дерева:')
	AVL.preorder_traversal(AVL_root)
	print('\n')

	

# TASK 2.3

def task_2_3(P:int, N: int, R: int, M: int):
	# {e} - {pi}
	MY_CONST = 0.718281828459045 - 0.141592653589793
	# {fi}
	KNUTH_CONST = 0.618033988749894

	multiplication_method(P, N, R, M, MY_CONST)
	multiplication_method(P, N, R, M, KNUTH_CONST)

	linear_probing(P, N, R, M, MY_CONST)
	linear_probing(P, N, R, M, KNUTH_CONST)

	double_hashing(P, N, R, M, MY_CONST)
	double_hashing(P, N, R, M, KNUTH_CONST)



# Выполнить: бинарный и интерполяционный поиск, алгоритмы для BST, алгоритмы хеширования.

if __name__ == '__main__':
	task_2_1(x = input('Введите число, которое нужно найти: '), N = 10000, M = 1000000)
	task_2_2()
	task_2_3(P = 1000, N = 1000, R = 2000, M = 2048)