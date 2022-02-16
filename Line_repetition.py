import types

class Insert:
	def __init__(self, string, iterable, functions):
		string = string.split('{}')
		self.first_string = string[0]
		self.last_string = string[1]
		self.iterable = iterable
		self.index_func = functions[0]
		self.value_func = functions[1]

	def __str__(self):
		return f'Итерируемый объект{self.iterable}\n' \
			   f'Строка: |{self.first_string}{{}}{self.last_string}|\n' \
			   f'Функции: {self.index_func.__doc__, self.value_func.__doc__}\n'

	def insert(self, index, val):
		return self.first_string + str(self.iterable[index]) + self.last_string if any(
			(self.index_func(index), self.value_func(val))) else ''


class Line:
	def __init__(self, string, iter_list, strings=None, functions=None):

		def all_f():
			f = lambda x: True
			f.__doc__ = 'All'
			return f
		def nothing_f():
			f = lambda x: False
			f.__doc__ = 'Nothing'
			return f

		def check_f(func):
			def try_index_f(func):
				for i in range(2):
					try:
						func[i]
					except KeyError:
						func[i] = None
					except IndexError:
						func.append(None)

			try_index_f(func)
			func_l = [isinstance(func[i], types.FunctionType) for i in range(len(func))]
			if any(func_l):
				for i in range(len(func)):
					if not func_l[i]:
						func[i] = nothing_f()
			else:
				for i in range(len(func)):
					if not func_l[i]:
						func[i] = all_f()


		self.parts_string = string.split('{}')
		self.inserts = []
		self.iter_list = iter_list
		if (dif := len(set([len(iter_object) for iter_object in iter_list]))) != 1:
			print(f"The size of iterated objects does not match\n"
				  f"Размер итерируемых объектов не совпадает\n"
				  f"The number of objects of different sizes is equal to {dif}\n"
				  f"Количество различных по размеру объектов равно {dif}")
		else:
			for index in range(len(self.iter_list)):
				# Проверка строк
				try:
					string = strings[index]
					if string is None:
						string = '{}'
				except (IndexError, KeyError):
					string = '{}'
				# Проверка функций
				try:
					func = functions[index]
				except (IndexError, KeyError):
					func = [None, None]
				check_f(func)

				self.inserts.append(Insert(string, iter_list[index], func.copy()))

	def __str__(self):
		pass

	def Start(self):

		for i in range(len(self.iter_list[0])):
			string = ''
			val = [self.iter_list[v][i] for v in range(len(self.iter_list))]
			for index in range(len(self.parts_string)-1):
				string += self.parts_string[index] + self.inserts[index].insert(i, val)
			else:
				string += self.parts_string[-1]
			print(string)




if __name__ == '__main__':
	def f1(x):
		'''Привет'''
		return True

	def f2(x):
		'''Пока'''
		return True

	list1 = [1, 2, 3]
	list2 = [4, 5, 6]
	list3 = [7, 8, 9]
	# I = Insert('перед {} за', [], [lambda x: True, lambda x: True])
	# print(f'|{I.first_string}', f'{I.last_string}|', sep='')
	L = Line('slovo1_{}_slovo2 {} slovo3 {} {}', [list1, list2, list3, ['first', 'second', 'fird']], ['Перед значением {} после;'],
			 {0: [lambda x: x>=0 and x<=1], 1:[f1,f2]})
	print(*L.inserts, sep='')
	L.Start()
