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
udn_url = 'https://money.udn.com/rank/newest/1001/5591/1'
udn_base = 'https://money.udn.com'

#keywords = ['�E��', '�B����', '���x��', '�I�h�d', '�I���d', '�E�إ��i', 'MIH', 'Fii', '�u�~�I�p', '�L��', '�E��', '����', '��~', '�E�a�x']
keywords = ['�~��', '�^��', '�̱�', '����', '�q��', '��S��', '�E��', '�̭]']

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
			# ���D
			#print("���D�G" + i.text)
			# ���}
			#print("���}�G" + cnyes_base+i.get('href'))
			for k in range(len(keywords)):

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
						news = [i.time.get('datetime'), "\n" + i.get('title') + "\n" + cnyes_base+i.get('href')]
						print(news)
						params = {"message": news}
						r = requests.post("https://notify-api.line.me/api/notify", headers=headers, params=params)
						print(r.status_code)
					break

def udn_scraping_news():
	#Declare global variable
	global checktime, lasttime

	# Create fake user agent
	#user_info = {'user-agent': 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
	user_info = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}

	# Download search data
	r = requests.get(udn_url, headers=user_info)

	# Check download data success
	if r.status_code == requests.codes.ok:
		# Use BeautifulSoup to analysis HTML source code
		soup = BeautifulSoup(r.text, 'html.parser')

		# HTML source code
		#print(soup.prettify)

		# Analysis necessary data
		items = soup.find_all("tr", {"style": "table-row"})
		#print(items)

		news = []

		for i in items:
			# �ɶ�
			#print("TIME�G" + i.find("td", {"align": "right"}).text)
			# ���D
			#print("���D�G" + i.find('a').text)
			# ���}
			#print("���}�G" + i.find('a')['href'])
			for k in range(len(keywords)):		
				pos = i.text.find(keywords[k])
				if pos >= 0:
					# �ɶ�
					#print("TIME�G" + i.find("td", {"align": "right"}).text)
					# ���D
					#print("���D�G" + i.find('a').text)
					# ���}
					#print("���}�G" + i.find('a')['href'])

					newstime = datetime.strptime(str(checktime.year) + "/" + i.find("td", {"align": "right"}).text, "%Y/%m/%d %H:%M")
					print(str(newstime))
					if newstime > checktime:
						print("find news!")
						# Update last news time
						if lasttime < newstime:
							lasttime = newstime

						# Notify line message
						news = [newstime, "\n" + i.find('a').text + "\n" + i.find('a')['href']]
						print(news)
						params = {"message": news}
						r = requests.post("https://notify-api.line.me/api/notify", headers=headers, params=params)
						print(r.status_code)
					break

while True:
	cnyes_scraping_news()
	udn_scraping_news()

	print("checktime: " + str(checktime))
	print("lasttime: " + str(lasttime))

	if checktime != lasttime:
		checktime = lasttime
		#checktime += timedelta(hours = 1)
		print("Next run: Update checktime to: " + str(checktime))
	print(" ")
	print(" ")
	time.sleep(300)