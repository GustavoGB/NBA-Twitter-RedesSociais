from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import json
import os

if "all_players.json":
    with open("all_players.json", 'r') as f:
        all_players = json.load(f)

list_teams = ["Golden State Warriors", "LA Clippers","Boston Celtics", "Chicago Bulls", "Houston Rockets", "Cleveland Cavaliers", 
                "Dallas Mavericks", "Los Angeles Lakers", "Brooklyn Nets", "Memphis Grizzlies", "Washington Wizards", "Oklahoma City Thunder", 
                "Miami Heat", "Minnesota Timberwolves", "Indiana Pacers", "Denver Nuggets", "Charlotte Hornets", "Philadelphia 76ers", 
                "Portland Trail Blazers", "Boston Celtics", "Milwaukee Bucks", "New Orleans Pelicans", "Toronto Raptors", "Phoenix Suns",
                "New York Knicks", "Detroit Pistons", "Utah Jazz", "Sacramento Kings", "Atlanta Hawks", "Orlando Magic", "San Antonio Spurs"]


def parse_to_json(transfer, list_teams, list_players):
    dict_json = {}
    key = None
    key_team = None

    for player in list_players:
        if player in transfer:
            key = player
    if key == None: #Caso o jogador não esteja na base, não queremos adicionar uma chave vazia
        print(player)
        return -1
    
    for team in list_teams:
        if team in transfer:
            key_team = team
    if key_team == None: #Caso o time não esteja na base, não queremos adicionar uma chave vazia
        print(team)
        return -1
    l_temp = []
    l_temp.append(key_team)
    dict_json[key] = l_temp
    return dict_json

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

try:
    os.remove("in_fim_2019_signed.json")
    os.remove("in_fim_2019_waived.json")

    os.remove("in_fim_2018_signed.json")
    os.remove("in_fim_2018_waived.json")

    os.remove("in_fim_2017_signed.json")
    os.remove("in_fim_2017_waived.json")

    os.remove("in_fim_2016_signed.json")
    os.remove("in_fim_2016_waived.json")

    os.remove("in_fim_2015_signed.json")
    os.remove("in_fim_2015_waived.json")

    os.remove("in_fim_2014_signed.json")
    os.remove("in_fim_2014_waived.json")
except:
    pass

dict_signed_2019 = {}
with open("in_fim_2019_signed.json", 'w') as f: #colocar jogador e time
    dict_json = parse_to_json(first_signed, list_teams, all_players)
    dict_json2 = parse_to_json(last_signed, list_teams, all_players)
    if dict_json != -1:
        dict_signed_2019.update(dict_json)
    if dict_json2 != -1:
        dict_signed_2019.update(dict_json2)
    json.dump(dict_signed_2019, f, indent=1)

dict_waived_2019 = {}
with open("in_fim_2019_waived.json", 'w') as f: #colocar jogador e time
    dict_json = parse_to_json(first_waived, list_teams, all_players)
    dict_json2 = parse_to_json(last_waived, list_teams, all_players)
    if dict_json != -1:
        dict_waived_2019.update(dict_json)
    if dict_json2 != -1:
        dict_waived_2019.update(dict_json2)
    json.dump(dict_waived_2019, f, indent=1)


### 2018-2019 lista ###
driver.get("https://www.basketball-reference.com/leagues/NBA_2019_transactions.html")
print(driver.current_url)
assert "basketball-reference" in driver.current_url
paragrafos = driver.find_elements_by_xpath("//p")
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
dict_signed_2018 = {}
with open("in_fim_2018_signed.json", 'w') as f: #colocar jogador e time
    dict_json = parse_to_json(first_signed, list_teams, all_players)
    dict_json2 = parse_to_json(last_signed, list_teams, all_players)
    if dict_json != -1:
        dict_signed_2018.update(dict_json)
    if dict_json2 != -1:
        dict_signed_2018.update(dict_json2)
    json.dump(dict_signed_2018, f, indent=1)

dict_waived_2018 = {}
with open("in_fim_2018_waived.json", 'w') as f: #colocar jogador e time
    dict_json = parse_to_json(first_waived, list_teams, all_players)
    dict_json2 = parse_to_json(last_waived, list_teams, all_players)
    if dict_json != -1:
        dict_waived_2018.update(dict_json)
    if dict_json2 != -1:
        dict_waived_2018.update(dict_json2)
    json.dump(dict_waived_2018, f, indent=1)



### 2017-2018 lista ###
driver.get("https://www.basketball-reference.com/leagues/NBA_2018_transactions.html")
print(driver.current_url)
assert "basketball-reference" in driver.current_url
paragrafos = driver.find_elements_by_xpath("//p")
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
dict_signed_2017 = {}
with open("in_fim_2017_signed.json", 'w') as f: #colocar jogador e time
    dict_json = parse_to_json(first_signed, list_teams, all_players)
    dict_json2 = parse_to_json(last_signed, list_teams, all_players)
    if dict_json != -1:
        dict_signed_2017.update(dict_json)
    if dict_json2 != -1:
        dict_signed_2017.update(dict_json2)
    json.dump(dict_signed_2017, f, indent=1)

dict_waived_2017 = {}
with open("in_fim_2017_waived.json", 'w') as f: #colocar jogador e time
    dict_json = parse_to_json(first_waived, list_teams, all_players)
    dict_json2 = parse_to_json(last_waived, list_teams, all_players)
    if dict_json != -1:
        dict_waived_2017.update(dict_json)
    if dict_json2 != -1:
        dict_waived_2017.update(dict_json2)
    json.dump(dict_waived_2017, f, indent=1)


### 2016-2017 lista ###
driver.get("https://www.basketball-reference.com/leagues/NBA_2017_transactions.html")
print(driver.current_url)
assert "basketball-reference" in driver.current_url
paragrafos = driver.find_elements_by_xpath("//p")
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
dict_signed_2016 = {}
with open("in_fim_2016_signed.json", 'w') as f: #colocar jogador e time
    dict_json = parse_to_json(first_signed, list_teams, all_players)
    dict_json2 = parse_to_json(last_signed, list_teams, all_players)
    if dict_json != -1:
        dict_signed_2016.update(dict_json)
    if dict_json2 != -1:
        dict_signed_2016.update(dict_json2)
    json.dump(dict_signed_2016, f, indent=1)

dict_waived_2016 = {}
with open("in_fim_2016_waived.json", 'w') as f: #colocar jogador e time
    dict_json = parse_to_json(first_waived, list_teams, all_players)
    dict_json2 = parse_to_json(last_waived, list_teams, all_players)
    if dict_json != -1:
        dict_waived_2016.update(dict_json)
    if dict_json2 != -1:
        dict_waived_2016.update(dict_json2)
    json.dump(dict_waived_2016, f, indent=1)


### 2015-2016 lista ###
driver.get("https://www.basketball-reference.com/leagues/NBA_2016_transactions.html")
print(driver.current_url)
assert "basketball-reference" in driver.current_url
paragrafos = driver.find_elements_by_xpath("//p")
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
dict_signed_2015 = {}
with open("in_fim_2015_signed.json", 'w') as f: #colocar jogador e time
    dict_json = parse_to_json(first_signed, list_teams, all_players)
    dict_json2 = parse_to_json(last_signed, list_teams, all_players)
    if dict_json != -1:
        dict_signed_2015.update(dict_json)
    if dict_json2 != -1:
        dict_signed_2015.update(dict_json2)
    json.dump(dict_signed_2015, f, indent=1)

dict_waived_2015 = {}
with open("in_fim_2015_waived.json", 'w') as f: #colocar jogador e time
    dict_json = parse_to_json(first_waived, list_teams, all_players)
    dict_json2 = parse_to_json(last_waived, list_teams, all_players)
    if dict_json != -1:
        dict_waived_2015.update(dict_json)
    if dict_json2 != -1:
        dict_waived_2015.update(dict_json2)
    json.dump(dict_waived_2015, f, indent=1)