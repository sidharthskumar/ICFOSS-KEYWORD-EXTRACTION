import requests
import codecs
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import NoSuchElementException

path = "E:\Work\ICFOSS\ICFOSS-KeyWord-Extractor\POSTagging"

f = open("tokenized_text.txt", 'r', encoding="utf-8")
txt = f.read()

driver = webdriver.Firefox(path)
driver.get('http://www.iiitmk.ac.in/MalayalamPOSTagger/index1.jsp')

a = driver.find_element_by_id('mal_text')
a.send_keys(txt)



driver.find_element_by_xpath("//input[@value='Tag The Sentence']").click();

sleep(4)
s=""
page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')
for line in soup.find_all(attrs ={"size":"3"}):
				print(line.string)
				s+=line.string+'\n'

filename = "tagged_text.txt"
fout = open("tagged_text.txt", 'w', encoding='utf-8')
fout.write("" + s + "")
f.close()
fout.close()



