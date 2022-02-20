'''
Задание 4.1. 
A = {a, b, c}. 
Приписать справа к слову P символы bc (P -> Pbc).

Задание 4.2. 
A = {A, B}. 
Удвоить слово P (например: abb -> abbabb).
'''



# TABLE WITH ALPHABET AND STATES 

def load_table(table_path: str) -> list:
	table = {}

	with open(table_path) as f:
		lines = f.readlines()
		alphabet = list(lines.pop(0))[:-1:]
		alphabet.append('_')
		alphabet = tuple(alphabet)

		for symbol, line in zip(alphabet, lines):
			formatted_states = []
			states = line.split(' ')

			for state in states:
				if 'None' in state:
					formatted_states.append(None)
				else:
					formatted_states.append(state.replace('\n', ''))

			table[symbol] = formatted_states

	return table



# TURING MACHINE

def turing_machine(table: dict, tape: list) -> list:
	i = 0
	next_state = 1

	while True:
		current_symbol = tape[i]
		state = table[current_symbol][next_state - 1]
		
		# write symbol
		tape[i] = state[0]
		
		move_tape = state[1]
		next_state = int(state[2:])
	
		if next_state == 0:
			return ''.join(tape).replace('_','')

		# move tape
		if move_tape == '>':
			i += 1
			if i == len(tape):
				tape.append('_')
		elif move_tape == '<':
			i -= 1
			if i < 0:
				tape.insert(0, '_')
				i = 0



# TASK 4.1

def task_4_1():
	table = load_table('task_4_1.txt')
	tape = list(input('Введите слово, состоящее из букв {a, b, c}: ') + '_')
	result = turing_machine(table, tape)
	
	print(f'Результат: {result}')	



# TASK 4.2

def task_4_2():
	table = load_table('task_4_2.txt')
	tape = list(input('Введите слово, состоящее из букв {a, b}: ') + '_')
	result = turing_machine(table, tape)
	
	print(f'Результат: {result}')
	


if __name__ == '__main__':
	task_4_1()
	task_4_2()