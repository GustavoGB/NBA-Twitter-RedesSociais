#C:\Users\HaranKumar\Downloads\chromedriver_win32_2.0\chromedriver.exe

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import json
import os

dict_signed = {}
dict_waived = {}
dict_re_signed = {}
list_signed = []
list_re_signed = []
list_waived = []


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


driver = webdriver.Chrome(executable_path=r'C:\Users\Victo\Downloads\chromedriver_win32\chromedriver.exe')
driver.get("https://stats.nba.com/transactions/")
print(driver.current_url)
assert "" in driver.current_url

for i in range(1):
    try:
        see_more = driver.find_element_by_xpath("//div[@class='button-container small-12 columns']/a[@class='button']")

        actions = ActionChains(driver)
        actions.move_to_element(see_more)
        actions.perform()

        see_more.click()
    except:
        break #CHEGOU NO COMEÇO DE 2015 

containers = driver.find_elements_by_xpath("//div[@class='transactions-list__date columns large-12']")
transfers = driver.find_elements_by_xpath("//div[@class='transactions-list__description small-6 medium-5 large-6 columns']")
in_fim_signed = []
in_fim_waived = []
dict_ = {}
if "in_fim_2019_signed.json" and "in_fim_2019_waived.json" and "in_fim_2018_signed.json" and "in_fim_2018_waived.json" and "in_fim_2017_signed.json" and "in_fim_2017_waived.json" and "in_fim_2016_signed.json" and "in_fim_2016_waived.json" and "in_fim_2015_signed.json" and "in_fim_2015_waived.json":
    with open("in_fim_2019_signed.json", 'r') as f:
        in_fim_2019_signed = json.load(f)
    with open("in_fim_2019_waived.json", 'r') as f:
        in_fim_2019_waived = json.load(f)
    with open("in_fim_2018_signed.json", 'r') as f:
        in_fim_2018_signed = json.load(f)
    with open("in_fim_2018_waived.json", 'r') as f:
        in_fim_2018_waived = json.load(f)
    with open("in_fim_2017_signed.json", 'r') as f:
        in_fim_2017_signed = json.load(f)
    with open("in_fim_2017_waived.json", 'r') as f:
        in_fim_2017_waived = json.load(f)
    with open("in_fim_2016_signed.json", 'r') as f:
        in_fim_2016_signed = json.load(f)
    with open("in_fim_2016_waived.json", 'r') as f:
        in_fim_2016_waived = json.load(f)
    with open("in_fim_2015_signed.json", 'r') as f:
        in_fim_2015_signed = json.load(f)
    with open("in_fim_2015_waived.json", 'r') as f:
        in_fim_2015_waived = json.load(f)

    dict_[list(in_fim_2019_signed.keys())[1]] = in_fim_2019_signed[list(in_fim_2019_signed.keys())[1]]
    dict_[list(in_fim_2019_waived.keys())[1]] = in_fim_2019_waived[list(in_fim_2019_waived.keys())[1]]
    dict_[list(in_fim_2018_signed.keys())[1]] = in_fim_2018_signed[list(in_fim_2018_signed.keys())[1]]
    dict_[list(in_fim_2018_waived.keys())[1]] = in_fim_2018_waived[list(in_fim_2018_waived.keys())[1]]
    dict_[list(in_fim_2017_signed.keys())[1]] = in_fim_2017_signed[list(in_fim_2017_signed.keys())[1]]
    dict_[list(in_fim_2017_waived.keys())[1]] = in_fim_2017_waived[list(in_fim_2017_waived.keys())[1]]
    dict_[list(in_fim_2016_signed.keys())[1]] = in_fim_2016_signed[list(in_fim_2016_signed.keys())[1]]
    dict_[list(in_fim_2016_waived.keys())[1]] = in_fim_2016_waived[list(in_fim_2016_waived.keys())[1]]
    dict_[list(in_fim_2015_signed.keys())[1]] = in_fim_2015_signed[list(in_fim_2015_signed.keys())[1]]
    dict_[list(in_fim_2015_waived.keys())[1]] = in_fim_2015_waived[list(in_fim_2015_waived.keys())[1]]

    in_fim_signed.append(list(in_fim_2019_signed.keys())[1])
    in_fim_signed.append(list(in_fim_2018_signed.keys())[1])
    in_fim_signed.append(list(in_fim_2017_signed.keys())[1])
    in_fim_signed.append(list(in_fim_2016_signed.keys())[1])

    in_fim_waived.append(list(in_fim_2019_waived.keys())[1])
    in_fim_waived.append(list(in_fim_2018_waived.keys())[1])
    in_fim_waived.append(list(in_fim_2017_waived.keys())[1])
    in_fim_waived.append(list(in_fim_2016_waived.keys())[1])


    years_signed = []
    years_waived = []
    year_signed = 2019
    year_waived = 2019


    for t in transfers:
        if "re-signed" in t.text:
            list_re_signed.append(t.text)
        elif "signed" in t.text:
            if(in_fim_signed[0] in t.text) and (dict_[in_fim_signed[0]][0] in t.text):
                year_signed-=1
                in_fim_signed = in_fim_signed[1:]
            list_signed.append(t.text)
            years_signed.append(year_signed)
        elif "waived" in t.text:
            if(in_fim_waived[0] in t.text) and (dict_[in_fim_waived[0]][0] in t.text):
                year_waived-=1
                in_fim_waived = in_fim_waived[1:]
            list_waived.append(t.text)
            years_waived.append(year_waived)

print(dict_)
print("-------------------")
print(in_fim_signed)
print("-------------------")
print(in_fim_waived)

try:
    os.remove("signed.json")
    os.remove("re_signed.json")
    os.remove("waived.json")
except:
    pass

if "all_players.json":
    with open("all_players.json", 'r') as f:
        all_players = json.load(f)

with open("signed.json", 'w') as f:
    for transfer in list_signed:
        dict_json = parse_to_json(transfer, list_teams, all_players) 
        if dict_json != -1:
            dict_signed.update(dict_json)

    index = 0
    for key in dict_signed:
        dict_signed[key].append(years_signed[index])
        index = index + 1
    json.dump(dict_signed, f, indent=1)

with open("waived.json", "w") as f:
    for transfer in list_waived:
        dict_json = parse_to_json(transfer, list_teams, all_players) 
        if dict_json != -1:
            dict_waived.update(dict_json)

    index = 0
    for key in dict_waived:
        dict_waived[key].append(years_waived[index])
        index = index + 1
    json.dump(dict_waived, f, indent=1)