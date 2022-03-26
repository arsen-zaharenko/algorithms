'''
Задание 5.
Решить диофантовое уравнение, используя генетический алгоритм.
''' 

from random import randint



# USEFUL FUNCTIONS

def read_powers(file_name: str) -> list:
	with open(file_name) as f:
		powers = f.readline().split(' ')
		
		u_pows = [int(powers[i]) for i in range(len(powers) - 1) if not i % 5]
		w_pows = [int(powers[i]) for i in range(len(powers) - 1) if not abs(i - 1) % 5]
		x_pows = [int(powers[i]) for i in range(len(powers) - 1) if not abs(i - 2) % 5]
		y_pows = [int(powers[i]) for i in range(len(powers) - 1) if not abs(i - 3) % 5]
		z_pows = [int(powers[i]) for i in range(len(powers) - 1) if not abs(i - 4) % 5]
		result = powers[-1]

		return [[u_pows, w_pows, x_pows, y_pows, z_pows], result]

def get_equation_form(powers: list) -> str:
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
			term += f'(z^{u_pows[i]})' if u_pows[i] > 1 else 'z'
		equation += f' + {term}' if equation else term

	return equation

def function(variables: list, powers: list) -> int:
	u, w, x, y, z = variables
	u_pows, w_pows, x_pows, y_pows, z_pows = powers

	return sum([u**u_pows[i] * w**w_pows[i] * x**x_pows[i] * y**y_pows[i] * z**z_pows[i] for i in range(len(u_pows))])
	


def task_5():
	variables = [1,2,3,2,1]
	powers, result = read_powers('2.txt')
	equation_form = get_equation_form(powers)
	print(function(variables, powers))



if __name__ == '__main__':
	task_5()