# Purpose : Example to show random proxy request 
# ProxyIpSite : https://www.ip-adress.com/proxy-list
# Date : 20-09-2017

import requests
import random
from bs4 import BeautifulSoup

s = requests.session()

proxylist = ['https://64.173.224.142:9991','https://212.47.252.49:3128','https://139.255.94.75:53281','https://195.154.77.130:3128']
ip = random.choice(proxylist)

print(ip)

proxies = {'https': str(ip) }
s.proxies.update(proxies)
req = s.get('https://www.healthfrog.in/chemists/medical-store/')
html = req.text
soup = BeautifulSoup(html, "html.parser")
container = soup.find("ul", {"class":["list1"]})
try:
	States = []
	Cities = []
	for row in container.findAll("li"):
		href = row.a.get('href')
		#print(href.rsplit('/', 1)[1])
		state = href.rsplit('/', 1)[1]
		#States.append(href.rsplit('/', 1)[1])
		print(state)
		citypage = s.get('https://www.healthfrog.in/chemists/medical-store/'+state+'')
		citypagehtml = citypage.text
		citypagesoup = BeautifulSoup(citypagehtml, "html.parser")
		citypagesoupcontainer = citypagesoup.find("ul", {"class":["list1"]})
		for row in citypagesoupcontainer.findAll("li"):
			href = row.a.get('href')
			city = href.rsplit('/', 1)[1]
			print("State:",state,":----------------City:",city)
			#Cities.append(href.rsplit('/', 1)[1])

except Exception as e:
	print(e)