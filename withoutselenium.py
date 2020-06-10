import requests, time, re
import random
import MySQLdb
from urllib.request import urlopen
from bs4 import BeautifulSoup

# Open database connection
db = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user="root", # your username
                     passwd="root", # your password
                     db="testdb", # name of the data base
                     port=3306)

# req = requests.session()
# proxylist = ['188.166.173.215:8118']
# ip = random.choice(proxylist)
# print(ip)
# proxies = {'http': str(ip),'https' : str(ip) }
# req.proxies.update(proxies)

def hitter(page, state, city):
    url = "https://www.healthfrog.in/importlisting.html"

    payload = "page="+str(page)+"&mcatid=chemists&keyword=medical-store&state="+state+"&city="+city
    headers = {
        'content-type': "application/x-www-form-urlencoded",
        'connection': "keep-alive",
        'cache-control': "no-cache"
    }
    time.sleep(10)
    response = requests.request("POST", url, data=payload, headers=headers)
    return response.text

def getPhoneNo(link):
    time.sleep(3)
    contactnumber=""
    soup1 = BeautifulSoup(urlopen(link).read(), "html.parser")
    mobile = soup1.find("i",{"class":"fa-mobile"}).next_sibling.strip()
    phone = soup1.find("i",{"class":"fa fa-phone"}).next_sibling.strip()
    try:
        if phone:
            contactnumber = phone
        if mobile:
            contactnumber = mobile
    except AttributeError:
        contactnumber = None
    return contactnumber

def getChemists(soup, city):
    time.sleep(10)
    stores = []
    for row in soup.find_all("div", {"class":"listing"}):
        #print(row)
        link = row.h3.a.get('href')
        dummy = {
            'name': row.h3.string,
            'address': row.p.get_text(),
            'phone': getPhoneNo(link),
            'city': city
        }
        #print(dummy)
        stores.append(dummy)
    return stores

if __name__ == '__main__':
    page, chemists = 1, []
    city, state = 'Mumbai', 'Maharashtra'
    html = hitter(page, state, city)
    condition = not re.match(r'\A\s*\Z', html)
    while(condition):
        soup = BeautifulSoup(html, 'html.parser')
        chemists += getChemists(soup, city)
        page += 1
        html = hitter(page, state, city)
        condition = not re.match(r'\A\s*\Z', html)
    # print(chemists)
    print("Dumpt Started For City "+ city)
    for i in range(len(chemists)):
         # prepare a cursor object using cursor() method
         cursor=db.cursor()
         try:
            sqlInsert = "INSERT INTO crawledretailer(`RetailerName`,`Address`,`ContactNumber`,`city`) VALUES ('%s', '%s', '%s','%s')" % (chemists[i]['name'],chemists[i]['address'],chemists[i]['phone'],chemists[i]['city'])
            cursor.execute(sqlInsert)
            db.commit()
         except Exception as e:
            print("Error: Unable to Insert Data : ",e)
            db.rollback()
    print("Dumpt Completed For City "+ city)