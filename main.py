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

# �d��� �j�M URL
cnyes_url = 'https://news.cnyes.com/news/cat/headline'
cnyes_base = 'https://news.cnyes.com'

# �g�٤�� �j�M URL
udn_url = 'https://money.udn.com/money/cate/5591'
udn_base = 'https://money.udn.com'

keywords = ['�E��', '�B����', '���x��', '�I�h�d', '�I���d', '�E�إ��i', 'MIH', 'Fii', '�u�~�I�p', '�L��', '�E��', '����', '��~', '�E�a�x']
#keywords = ['�~��', '�^��', '�̱�', '����', '�q��', '��S��', '�E��', '�̭]']

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
				# ���D
				#print("���D�G" + i.text)
				# ���}
				#print("���}�G" + cnyes_base+i.get('href'))
				pos = i.text.find(keywords[k])
				if pos >= 0:
					# ���D
					#print("���D�G" + i.text)
					# ���}
					#print("���}�G" + cnyes_base+i.get('href'))

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
		print("find news in �d���! update checktime to: " + str(checktime))

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
				# ���D
				#print("���D�G" + i.text)
				# ���}
				#print("���}�G" + udn_base+i.get('href'))
				pos = i.text.find(keywords[k])
				if pos >= 0:
					# ���D
					#print("���D�G" + i.text)
					# ���}
					#print("���}�G" + udn_base+i.get('href'))

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