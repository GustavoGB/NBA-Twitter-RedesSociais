from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import json
import os

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
driver = webdriver.Chrome(chrome_options=options, executable_path=r'C:\Users\Victo\Downloads\chromedriver_win32\chromedriver.exe')

driver.get("https://www.basketball-reference.com/leagues/NBA_2020_transactions.html")
print(driver.current_url)
assert "basketball-reference" in driver.current_url


paragrafos = driver.find_elements_by_xpath("//p")
### 2019-2020 lista ###
j = 0
a = 0
signed = -1
waived = -1
for i in range(len(paragrafos)):
    print(i)
    try: 
        if("re-signed" in paragrafos[i].text):
            pass
        elif("assigned" in paragrafos[i].text):
            pass
        elif(("signed" in paragrafos[i].text) and (j == 0)):
            first_signed = paragrafos[i].text
            j = 1
        elif( ("signed" in paragrafos[i].text) and (j == 1) ):
            signed = paragrafos[i].text
        elif( ("waived" in paragrafos[i].text) and (a == 0) ):
            first_waived = paragrafos[i].text
            a = 1  
        elif( ("waived" in paragrafos[i].text) and (a == 1) ):
            waived = paragrafos[i].text
        
        if(signed != -1):
            last_signed = signed
        if(waived != -1):
            last_waived = waived

    except Exception as e:
        print(e)
        break

print(first_signed, last_signed)
print(first_waived, last_waived)