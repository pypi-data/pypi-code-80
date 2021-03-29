import math
import pyttsx3 as pyt


class mfuncs():
	"""Вспомогательные функции"""
	def __init__(self, path):
		self.engine = pyt.init()
		
		with open(path, "r") as file:
			self.file = file.read()


	def mprint(text = None):
		"""
		Команда PRINT, которая показывает статистику о входящих данных
		"""
		if text is None:
			print('')
		else:
			try:
				text_count = len(text)
				text_type = type(text)

				print(f'{text} [Символов: {text_count}; Тип: «{text_type}»]')
			except:
				error = 'Ошибка: Невозможно вывести'
				print(error)

	def nstring(string = None, amount = 0):
		"""
		Функция, чтобы отнять от строки указанное количество символов (с конца)
		"""
		if string is None:
			print('Ошибка: Строка не указана')
		else:

			if amount == 0:
				print(string)
			else:
				result = string[:-amount]
				return result

	def oddcheck(number = 0):
		"""
		Функция, чтобы проверить, является-ли число чётным или нечётным
		"""
		try:
			if number % 2 == 0:
				print('Число чётное')
			else:
				print('Число НЕ чётное')
		except:
			print('Ошибка: Данную переменную невозможно поделить')

	def piglatin(word):
		"""
		Функция, чтобы зашифровать слово, в "PIG LATIN", только в начале добавляется f или c
		"""
		vowels = 'aeiou'
		ay = 'ay'
		f = 'f'
		c = 'c'


		first = word[0]

		if first in vowels:
			pigword = f + word + ay
		else:
			pigword = c + word[1:] + first + ay

		return pigword

	def clear():
		"""
		Функция, чтобы очистить место
		"""
		print('\n' * 1000)