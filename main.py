# coding: cp950
# coding: utf-8

from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import requests
import time

headers = {
	"Authorization": "Bearer " + "ImKVjQoh7iBF5uxUiMEVVUsfDasyvwORCGTjt7Mi4mC",
	"Content-Type": "application/x-www-form-urlencoded"
}

# 鉅亨網 搜尋 URL
cnyes_url = 'https://news.cnyes.com/news/cat/headline'
cnyes_base = 'https://news.cnyes.com'

# 經濟日報 搜尋 URL
udn_url = 'https://money.udn.com/money/cate/5591'
udn_base = 'https://money.udn.com'

keywords = ['鴻海', '劉揚偉', '郭台銘', '富士康', '富智康', '鴻華先進', 'MIH', 'Fii', '工業富聯', '夏普', '鴻準', '臻鼎', '樺漢', '鴻家軍']
#keywords = ['外資', '彭博', '疫情', '美股', '通膨', '比特幣', '鴻海', '疫苗']

# First use current time to scrap news
checktime = datetime.now()
lasttime = checktime
print("Now the date time is " + str(checktime.strftime("%Y-%m-%d %H:%M:%S")) + ", start to scraping news!")

def cnyes_scraping_news():
	#Declare global variable
	global checktime, lasttime

	# Download search data
	r = requests.get(cnyes_url)

	# Check download data success
	if r.status_code == requests.codes.ok:
		# Use BeautifulSoup to analysis HTML source code
		soup = BeautifulSoup(r.text, 'html.parser')

		# HTML source code
		#print(soup.prettify)
  
		# Analysis necessary data
		items = soup.find_all("a", {"class": "_1Zdp"})
		#print(items)

		news = []

		for i in items:
			for k in range(len(keywords)):
				# 標題
				#print("標題：" + i.text)
				# 網址
				#print("網址：" + cnyes_base+i.get('href'))
				pos = i.text.find(keywords[k])
				if pos >= 0:
					# 標題
					#print("標題：" + i.text)
					# 網址
					#print("網址：" + cnyes_base+i.get('href'))

					newstime = datetime.strptime(i.time.get('datetime'), "%Y-%m-%dT%H:%M:%S+08:00")
					print(str(newstime))
					if newstime > checktime:
						print("find news!")
						# Update last news time
						if lasttime < newstime:
							lasttime = newstime

						# Notify line message
						news = [i.time.get('datetime'), i.get('title'), cnyes_base+i.get('href')]
						print(news)
						params = {"message": news}
						r = requests.post("https://notify-api.line.me/api/notify", headers=headers, params=params)
						print(r.status_code)
					break

	#FIXME
	if checktime != lasttime:
		checktime = lasttime
		#checktime += timedelta(hours = 1)
		print("find news in 鉅亨網! update checktime to: " + str(checktime))

#FIXME
def udn_scraping_news():
	#Declare global variable
	global checktime, lasttime

	# Download search data
	r = requests.get(udn_url)

	# Check download data success
	if r.status_code == requests.codes.ok:
		# Use BeautifulSoup to analysis HTML source code
		soup = BeautifulSoup(r.text, 'html.parser')

		# HTML source code
		#print(soup.prettify)
  
		# Analysis necessary data
		items = soup.find_all("dt", {"class": "more_5612"})
		#print(items)

		news = []

		for i in items:
			for k in range(len(keywords)):
				# 標題
				#print("標題：" + i.text)
				# 網址
				#print("網址：" + udn_base+i.get('href'))
				pos = i.text.find(keywords[k])
				if pos >= 0:
					# 標題
					#print("標題：" + i.text)
					# 網址
					#print("網址：" + udn_base+i.get('href'))

					newstime = datetime.strptime(i.time.get('datetime'), "%Y-%m-%dT%H:%M:%S+08:00")
					print(str(newstime))
					if newstime > checktime:
						print("find news!")
						# Update last news time
						if lasttime < newstime:
							lasttime = newstime

						# Notify line message
						news = [i.time.get('datetime'), i.get('title'), udn_base+i.get('href')]
						print(news)
						params = {"message": news}
						r = requests.post("https://notify-api.line.me/api/notify", headers=headers, params=params)
						print(r.status_code)
					break

	if checktime != lasttime:
		checktime = lasttime
		#checktime += timedelta(hours = 1)
		print("find news! update checktime to: " + str(checktime))

while True:
	cnyes_scraping_news()
	print("----------Next run----------")
	print(" ")
	print(" ")
	time.sleep(300)