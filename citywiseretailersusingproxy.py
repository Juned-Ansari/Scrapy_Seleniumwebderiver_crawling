# Purpose : Fetch City Wise Retailers Name using proxy Ips
# ProxyIpSite : https://www.ip-adress.com/proxy-list
# Date : 25-09-2017

import requests
import time
import MySQLdb
import random
from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException

# Open database connection
db = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user="root", # your username
                     passwd="root", # your password
                     db="testdb", # name of the data base
                     port=3306)

s = requests.session()
req = s.get('https://www.ip-adress.com/proxy-list')
proxyhtml = req.text
proxysoup = BeautifulSoup(proxyhtml, "html.parser")
proxycontainer = proxysoup.find("table", {"class":["htable proxylist"]})
tbody = proxycontainer.find("tbody")
ProxyIps = []
try:
	#fetch Proxy Ips from https://www.ip-adress.com/proxy-list
	for row in tbody.find_all("tr"):
		ip = row.td.a.text.strip()
		port = row.td.a.next_sibling.strip()
		proxyip = (ip+port)
		if (port!=":80" and port!=":8080"):
			ProxyIps.append(proxyip)

	#set dynamic proxy List
	print(*ProxyIps)
	pip = random.choice(ProxyIps)
	print("IPS:",pip)
	PROXY = str(pip)  # IP:PORT or HOST:PORT
	print("Data Crawling using IP : ",PROXY)
	url = "https://www.healthfrog.in/chemists/medical-store/maharashtra/thane"
	city = "thane"
	chrome_options = webdriver.ChromeOptions()
	chrome_options.add_argument('--proxy-server=http://%s' % PROXY)
	browser = webdriver.Chrome(chrome_options=chrome_options)
	browser.get(url)
	time.sleep(100)
	while True:
	    try:
	        loadMoreButton = browser.find_element_by_id("loadmore")
	        time.sleep(2)
	        loadMoreButton.click()
	        time.sleep(20)
	        html = browser.page_source
	        soup = BeautifulSoup(html, "html.parser")
	    except Exception as e:
	        print(e)
	        break

	print('Page Loading Completed')
	time.sleep(10)

	print('data dump started for City: ',city)
	contactnumber=""
	c=1
	try:
	    for row in soup.find_all("div", {"class":["listing ", "listing"]}):
	        try:
	            name = row.h3.a.string
	            address = row.p.get_text()
	            href = row.h3.a.get('href')
	            contatnumberpage = BeautifulSoup(urlopen(href).read(), 'html.parser')
	            row1 = contatnumberpage.findAll("div", {"class":"listing detail"})
	            telephonenumber = row1[0].find("i",{"class":"fa fa-phone"}).next_sibling.strip()
				mobilenumber = row1[0].find("i",{"class":"fa fa-mobile"}).next_sibling.strip()
	            if telephonenumber:
	            	contactnumber = telephonenumber + ","
	            if mobilenumber:
	            	contactnumber += mobilenumber        
	            
	            print(c)
	            c = c + 1
	            #print(name)
	            #print(href)
	            #print(address)
	            
	            # prepare a cursor object using cursor() method
	            cursor=db.cursor()
	            try:
	                sqlInsert = 'INSERT INTO crawledretailer(`RetailerName`,`Address`,`ContactNumber`,`city`) VALUES (%s, %s, %s,%s);'
	                cursor.execute(sqlInsert,(name,address,contactnumber,city))
	                db.commit()
	            except Exception as e:
	               print("Error: Unable to Insert Data : ",e) 
	               db.rollback()
	        except AttributeError:
	            print("Error: Google Ad Detected : ") 


	except TimeoutException as ex: 
	    isrunning = 0

	print("data dump completed for City: ",city)
	browser.close()
	browser.quit()
		
except Exception as e:
	print("Error:",e)

