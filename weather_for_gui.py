from lxml import html
import requests as r
import draw_graph_for_temp as graph 
import time

def city_entry(city):
	time_start = time.time()
	weather = []								#массив температур в течении дня
	check_city = ''								#пустая строка для города с сайта
	a = list(tuple(city))
	for i in a:									#если есть пробел в названии города, то заменяю его на -
		if ' ' in a:
			a.insert(a.index(" "), "-")
			a.remove(' ')
	city = ''.join(a)
	url = "https://pogoda33.ru/погода-" + city + "/день"	#создаю ссылку с городом (изменил)
	try:
		req = r.get(url)							#запрашиваю страницу
		tree = html.fromstring(req.text)			#преобразую запрос в структуру html
		check = tree.xpath('/html/body/div/div[6]/div[1]/div[2]/div[2]/h2/text()')
		try:
			check = list(tuple(check[0]))				#раскладываю заголовок на буквы
			index_point = check.index('.')				#нахожу индекс точки, чтобы узнать город в заголовке
			for i in range (index_point + 2, len(check)):	
				if check[i] == ' ':
					check_city += '-'
				else:
					check_city += check[i]				#создал строку, в которой будет находиться город из заголовка
			if check_city.lower() == city:				#если введённый город совпадает с тем, что на сайте
				try:
					for i in range (4, 12):				#на сайте 8 дивов с температурой
						weather.append(int(tree.xpath('/html/body/div/div[7]/div[1]/div[' + str(i) + ']/div[2]/span/text()')[0]))
					graph.main(weather)
					name = graph.save(city.title())
					time_end = time.time()
					print("pars", time_end - time_start)
					return name
				except IndexError:
					graph.main(weather)
					name = graph.save(city.title())
					return name
			else:
				return "Такого города не нашёл"
		except IndexError:
			return "Некорректный ввод"
	except r.ConnectionError:
		return "No Internet connection!"

def weather_cloud(city):
	url = "https://pogoda33.ru/погода-" + city
	req = r.get(url)
	tree = html.fromstring(req.text)
	return tree.xpath("/html/body/div/div[5]/div[3]/div[8]/div[3]/text()")