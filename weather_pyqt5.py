from PyQt5 import QtWidgets as qw 			#модуль для создания объектов 
from PyQt5.QtGui import QPixmap				#класс для создания изображений
from PyQt5.QtCore import Qt 				#класс для позиционирования текста внутри виджетов
from PyQt5.QtWidgets import QMessageBox 	#класс для создания всплывающих окон (использую для отображения ошибок)
from PyQt5.QtGui import QIcon 				#класс для вставки изображения в виде иконки для приложения
import weather_for_gui as weather 			#мой модуль для парсинга страницы + рисование графика по массиву температур
import sys									#модуль для корректной работы окна
import datetime as date 					#модуль для узнавания текущей даты
import os.path 								#модуль для проверки нахождения файла в папке
from os import getcwd
from os.path import exists
from os import mkdir

class Window(qw.QMainWindow):				#создаю класс для работы с объектами внутри окна (иначе нельзя)
	display_width = 1920
	display_height = 1080
	window_width = 800
	window_height = 780
	position_x = display_width//2 - window_width//2	- 200				#вычисляю координаты центра дисплея по х
	position_y = display_height//2 - window_height//2 - 110				#вычисляю координаты центра дисплея по у

	def __init__(self):													#конструктор для класса (по сути, пишу то, что будет находиться в окне)
		super(Window, self).__init__()									#вызываю конструктор QMainWindow, т.к. всё будет на основе этого класса
		self.setWindowTitle("Узнать погоду!")	#здесь прописываю название своего окна

		self.setGeometry(self.position_x, self.position_y, self.window_width, self.window_height)
																			#и задаю позицию + размеры
		self.setWindowIcon(QIcon('icons/weather.png'))	#устанавливаю иконку для приложения
																			#устанавливаю иконку для своего приложения
		header = qw.QLabel(self)											#создаю текстовый виджет
		header.setText("Данное приложение было разработано в целях\nоблегчения поиска актуальной температуры")
		header.setAlignment(Qt.AlignCenter)									#позиционирую текст внутри виджета посередине
		style_headder = "color: #240672; font-size: 26px; font-family: ‘Signika’, sans-serif; border-top: 2px solid #BBC9C9; border-bottom: 2px solid #BBC9C9;"
		header.setStyleSheet(style_headder)
		header.adjustSize()													#задаю динамически изменяющийся размер виджету
		width_header = header.frameGeometry().width()						#узнаю ширину виджета
		width_center_header = self.window_width//2 - width_header//2		#вычисляю координаты центра окна по x для заголовка
		header.move(width_center_header, 20)								#и позиционирую по центру по ширине

		text_question = qw.QLabel(self)												#создаю текстовый виджет
		text_question.setText("Пожалуйста, введите город")				
		style_text_question = "color: #4E026E; font-size: 24px;"					#задаю стили для текста с просьбой ввести город
		text_question.setStyleSheet(style_text_question)					
		text_question.adjustSize()													#задаю динамически изменяющийся размер виджету
		width_text_question = text_question.frameGeometry().width()					#узнаю ширину виджета
		width_center_text_question = self.window_width//2 - width_text_question//2	
		text_question.move(width_center_text_question, 95)							#размещаю в окне


		city = qw.QLineEdit(self)														#создаю поле для ввода
		style_city = "font-size: 20px; border-radius: 5px; border: 1px solid black;"	#задаю стили этому полю
		city.setStyleSheet(style_city)													#устанавливаю стили
		city.setAlignment(Qt.AlignCenter)												#размещаю текст внутри поля по центру
		city.returnPressed.connect(lambda: self.button_click(city.text().lower())) 		#привязываю нажатие на enter
		city.setGeometry(self.window_width//2 - 100, 140, 200, 30)						#размещаю само поле по центру по ширине


		button = qw.QPushButton(self)														#создаю кнопку 
		button.setText("Узнать погоду!")													#текст кнопки
		style_button = "font-size: 24px; border-radius: 6px; border: 1px solid black; background-color: #3E13AF; color: white;"
		button.setStyleSheet(style_button)		
		button.clicked.connect(lambda: self.button_click(city.text().lower()))				#функция при нажатии на кнопку
		button.setGeometry(self.window_width//2 - 150, 185, 300, 40)						#позиция кнопки

		self.answer_with_city = qw.QLabel(self) 											#создаю текстовый ответ
																							#содержащий город и дату
		style_answer_with_city = "color: #A68C00; font-size: 24px;"							
		self.answer_with_city.setStyleSheet(style_answer_with_city)							#устанавливаю стили

		self.graph = qw.QLabel(self)														#создаю поле для изображения
		self.graph.setGeometry(self.window_width//2 - 320, 280, 640, 480)					#и задаю его размеры + положение

		self.img_cloud = qw.QLabel(self)
		self.img_cloud.setGeometry(self.window_width//2 + 110, 230, 40, 40)

	def button_click(self, city):		#испоьлзую функцию в классе, чтобы вызывать функцию, которая будет менять текст
		if city == '':
			warning("Ничего не введено")													#если ничего не введено, то 
																							#сообщаю об этом в всплывающем окне
		elif os.path.exists('graphics/' + city + "_" + str(date.date.today()) + '.png'): 	#ищу график с температурой для 
																							#введённого города в папке
			self.draw_img(city + "_" + str(date.date.today()))								#если найдеен, то выводу на экран
			print("График найден в папке, хоть отдохну маленько")							#и сообщаю об этом в cmd
			self.answer(city.title())
			#self.draw_cloud(weather.weather_cloud(city))
			print("В городе " + city.title() + " " + weather.weather_cloud(city)[0])
		else:
			result = weather.city_entry(city)															#если не найден, то запускаю париснг
			if (result == "Такого города не нашёл") or (result == "No Internet connection!") or (result == "Некорректный ввод"):	#обрабатываю некорректный ввод
				print(result)
				warning(result)																			#вызываю окошко с предупреждением
			else:
				#self.draw_cloud(weather.weather_cloud(city))
				print("В городе " + city.title() + " " + weather.weather_cloud(city)[0])
				self.answer(city.title())													#вызываю ф-ию печати ответа
				self.draw_img(result)														#вызываю функцию печати изображения
				print("Пришлось за тебя всё искать, лентяй")								

	def draw_img(self, city):																	#ф-ия печати графика
		url = "graphics/" + city +".png"			#формирую путь к графику
		img = QPixmap(url)																		#создаю объект изображения
		self.graph.setPixmap(img)																#отображаю в поле

	def answer(self, city):																			#печать ответа
		self.answer_with_city.setText("Погода в городе " + city + " на " + str(date.date.today()))	#предложение
		self.answer_with_city.adjustSize()															#подгон размера по ширине
		width_answer_with_city = self.answer_with_city.frameGeometry().width()						#ширина блока
		self.answer_with_city.move(self.window_width//2 - width_answer_with_city//2, 230)			#по середине ширины

	#def draw_cloud(self, cloud):
	#	url = "icons/" + cloud[0] + ".png"
	#	img = QPixmap(url)
	#	self.img_cloud.setPixmap(img)



def app():
	application = qw.QApplication (sys.argv)							#инициализация pyqt	
	window = Window()													#создание прототипа класса окна
	window.show()														#показ созданного окна
	sys.exit(application.exec_())										#без этой строчки окно закрывается сразу же

def warning(text):
	error_win = QMessageBox()											#создаю класс на основе QMessageBox (всплывающее окно)
	error_win.setWindowIcon(QIcon('C:/Users/Anton/Desktop/Python/progs/weather/qt/icons/warning.png'))		#задаю иконку для всплывающего окна
	error_win.setWindowTitle("Что-то пошло не так")						#название открывшегося окна
	error_win.setText(text)												#вывожу текст ошибки, который передаётся в ф-ию
	style_error_text = "font-size: 22px;"
	error_win.setStyleSheet(style_error_text)
	error_win.setIcon(QMessageBox.Warning)								#устанавливаю иконку (warning) около текста
	error_win.setStandardButtons(QMessageBox.Ok)						#добавляет кнопку Ok
	error_win.exec_()													#не позволяет сразу закрываться после открытия

if __name__ == "__main__":
	if not exists(getcwd() + "/graphics"):
		mkdir(getcwd() + "/graphics")
	app()