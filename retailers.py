import time
import MySQLdb
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

url = "https://www.healthfrog.in/chemists/medical-store/gujarat/ahmedabad"
city = "ahmedabad"
browser = webdriver.Chrome()
browser.get(url)

time.sleep(1)
while True:
    try:
        loadMoreButton = browser.find_element_by_id("loadmore")
        time.sleep(2)
        loadMoreButton.click()
        time.sleep(5)
        html = browser.page_source
        soup = BeautifulSoup(html, "html.parser")
    except Exception as e:
        print(e)
        break

print('Page Loading Completed')
time.sleep(10)

print('data dump started')
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
            mobilenumber = row1[0].find("i",{"class":"fa-mobile"}).next_sibling.strip()
            telephonenumber = row1[0].find("i",{"class":"fa fa-phone"}).next_sibling.strip()
            if telephonenumber:
                contactnumber = telephonenumber + ","
            if mobilenumber:
                contactnumber = mobilenumber       
            
            print(c,":",contactnumber)
            c = c + 1
            #print(name)
            #print(href)
            #print(address)
            
            # prepare a cursor object using cursor() method
            cursor=db.cursor()
            try:
                sqlInsert = "INSERT INTO crawledretailer(`RetailerName`,`Address`,`ContactNumber`,`city`) VALUES ('%s', '%s', '%s','%s')" % (name,address,contactnumber,city)
                cursor.execute(sqlInsert)
                db.commit()
            except Exception as e:
               print("Error: Unable to Insert Data : ",e) 
               db.rollback()
        except AttributeError:
            print("Error: Google Ads Detected : ") 


except TimeoutException as ex: 
    isrunning = 0

print("data dump completed") 
#browser.close()
#browser.quit()