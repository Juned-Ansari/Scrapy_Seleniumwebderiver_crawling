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
req = s.get('https://www.ip-adress.com/proxy-list')
html = req.text
soup = BeautifulSoup(html, "html.parser")
container = soup.find("table", {"class":["htable proxylist"]})
tbody = container.find("tbody")
# print(tbody)
ProxyIps = []
try:
	#fetch Proxy Ips from https://www.ip-adress.com/proxy-list
	for row in tbody.find_all("tr"):
		ip = row.td.a.text.strip()
		port = row.td.a.next_sibling.strip()
		proxyip = (ip+port)
		ProxyIps.append(proxyip)

		#set dynamic proxy List
		pip = random.choice(ProxyIps)
		proxies = {'https': str(pip) }
		s.proxies.update(proxies)
		#End of Proxy Setting
	#End of Fetch Proxy Ips List	

	statepage = s.get('https://www.healthfrog.in/chemists/medical-store/')
	statepagehtml = statepage.text
	statepagesoup = BeautifulSoup(statepagehtml, "html.parser")
	statepagecontainer = statepagesoup.find("ul", {"class":["list1"]})
	try:
		for row in statepagecontainer.findAll("li"):
			href = row.a.get('href')
			state = href.rsplit('/', 1)[1]
			citypage = s.get('https://www.healthfrog.in/chemists/medical-store/'+state+'')
			citypagehtml = citypage.text
			citypagesoup = BeautifulSoup(citypagehtml, "html.parser")
			citypagesoupcontainer = citypagesoup.find("ul", {"class":["list1"]})
			for row in citypagesoupcontainer.findAll("li"):
				href = row.a.get('href')
				city = href.rsplit('/', 1)[1]
				print("State:",state,":----------------City:",city)
	except Exception as e:
		print(e)
		
except Exception as e:
	print("Error:",e)

