import types


class Insert:

	def __init__(self, string, iterable, functions):
		'''
		Инициализация
		:param string: Строка формата 'Начало {}конец' Начало - то что всегда будет идти перед значением, конец - то что всегда будет идти в конце
		:type string: str
		:param iterable: Объект к которому можно обратится по индексу
		:type iterable: list|dict
		:param functions: Функции условий первый индекс - условия по индексу, второй индекс - условие по значениям в строке
		:type functions: list|dict
		'''
		self.string = string
		self.iterable = iterable
		self.index_func = functions[0]
		self.value_func = functions[1]

	def __str__(self):
		'''
		:return: итерируемый объект, форматируемая строка, документацию функций
		:rtype: str
		'''
		return f'Итерируемый объект: {self.iterable}\n' \
			   f'Строка: {self.string}\n' \
			   f'Функции: {self.index_func.__doc__, self.value_func.__doc__}\n'

	def insert(self, index, val):
		'''
		:param index: Номер линии начиная с 0
		:type index: int
		:param val: Значение всех параметров
		:type val: list
		:return: Либо '', либо отформатированную строку
		:rtype: str
		'''
		return self.string.format(self.iterable[index]) if any(
			(self.index_func(index), self.value_func(val))) else ''


class Line:
	def __init__(self, string, iter_list, strings=None, functions=None):
		'''
		:param string: Строка для форматирования 'Start {} anything {} end{}'
		:type string: str
		:param iter_list: Список или словарь для значений, к тоторым можно обратится по индексу
		:type iter_list: list|dict
		:param strings: Строки для вставок
		:type strings: list|dict
		:param functions: Функции фильтрации для вставок
		:type functions: list|dict
		'''

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

		self.string = string
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
					if string is None or string == '':
						string = '{}'
					elif string.count('{') == 0 and string.count('}') == 0:
						string += '{}'
				except (IndexError, KeyError):
					string = '{}'
				# Проверка функций
				try:
					func = functions[index]
				except (IndexError, KeyError, TypeError):
					func = [None, None]
				check_f(func)

				self.inserts.append(Insert(string, iter_list[index], func.copy()))

	def Start(self):
		'''
		:return: Выводит в терминал отформатированные строки
		'''

		for i in range(len(self.iter_list[0])):
			val = [self.iter_list[v][i] for v in range(len(self.iter_list))]
			rez = [insert.insert(i, val) for insert in self.inserts]
			print(self.string.format(*rez))


if __name__ == '__main__':
	def f1(x):
		'''Привет'''
		return True


	def f2(x):
		'''Пока'''
		return True


	list1 = [2, 7, 5]
	list2 = [2, 8, 5]
	list3 = {1: 15, 0: 4, 2: 15}
	list4 = '-' * 2 + '3'

	L = Line('Start: {}{}{}{} Rezult: {}', [list1, list4, list2, list3, ['верно', 'верно', True]],
			 ['пример > {} + ', 'пример > {} * ', '{} = ', '{:2}', ' {}'],
			 {0: [lambda x: x >= 0 and x <= 1], 1: [lambda x: x >= 2 and x < 3], 3: {1: f2, 0: f1}})

	print(*L.inserts, sep='', end='\n------\n')
	L.Start()
	print('------')

	l1 = [125, 77, 25, 333]
	l2 = '+-*/'
	l3 = [88, 99, 101, 555]
	l4 = [l1[0] + l3[0], l1[1] - l3[1], l1[2] * l3[2], l1[3] / l3[3]]
	l5 = ["int"] * 4
	l6 = ["float"] * 4
	L = Line('Math > {}{}{}{} Type rez: {}{}', [l1, l2, l3, l4, l5, l6], ['{:3}', ' {} ', '{:3}', ' = {:4}'],
			 {4: [None, lambda x: type(x[3]) == int], 5: [None, lambda x: type(x[3]) == float]})
	L.Start()

	f1 = open('Names', mode='r', encoding='utf-8')
	f2 = open('Last_names', mode='r', encoding='utf-8')
	f3 = open('mails', mode='r', encoding='utf-8')

	l1 = f1.read().split('\n')
	l2 = f2.read().split('\n')
	l3 = f3.read().split('\n')

	L = Line('Names: {} {} || gmail > {}', [l1, l2, l3], {2: '{}@gmail.com'})
	L.Start()
