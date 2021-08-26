import matplotlib.pyplot as mp 
import numpy
import datetime as date
import time

area, graph = mp.subplots()

def main (weather):
	time_start = time.time()
	graph.cla()														#очищение предыдущего графика
	if len(weather) == 8:												
		x = [i for i in range (0, 24, 3)]
		graph.set_xticks(numpy.arange(0, 24, 1))					#шаг оси х (массив от 0 до 24 с шагом 3)
		graph.set_yticks(numpy.arange(min(weather), max(weather) + 1, 1))
	else:
		x = [i for i in range (3, 24, 3)]
		print(weather)
		print(x)
		graph.set_xticks(numpy.arange(3, 24, 1))					#шаг оси х (массив от 0 до 24 с шагом 3)
		graph.set_yticks(numpy.arange(min(weather), max(weather) + 1, 1))


	graph.spines['right'].set_visible(0)							#убрать границу графика справа
	graph.spines['top'].set_visible(0)								#убрать границу графика сверху

	graph.set_ylabel('Градусы')										#названия осей
	graph.set_xlabel('Часы')

	graph.set_ylim(min(weather) - 1, max(weather) + 1)				#предел по х
	graph.set_xlim(min(x), max(x) + 1)								#предел по у

	graph.spines['bottom'].set_position(('data', min(weather)-1))	#!расположение оси x в y = 0

	graph.grid(alpha = 0.3)

	graph.plot(x, weather)
	time_end = time.time()
	print("graph", time_end - time_start)
	

def save(city):
	name_png = city + "_" + str(date.date.today())
	area.savefig('graphics/' + name_png + '.png')						#сохраняет график в виде png (формат можно менять)
	return name_png