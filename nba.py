#C:\Users\HaranKumar\Downloads\chromedriver_win32_2.0\chromedriver.exe

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import json
import os

dict_signed = {}
dict_re_signed = {}
list_signed = []
list_re_signed = []

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
        return -1
    
    for team in list_teams:
        if team in transfer:
            key_team = team
    if key_team == None: #Caso o time não esteja na base, não queremos adicionar uma chave vazia
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
    see_more = driver.find_element_by_xpath("//div[@class='button-container small-12 columns']/a[@class='button']")

    actions = ActionChains(driver)
    actions.move_to_element(see_more)
    actions.perform()

    see_more.click()

transfers = driver.find_elements_by_xpath("//div[@class='transactions-list__description small-6 medium-5 large-6 columns']")


for t in transfers:
    if "re-signed" in t.text:
        list_re_signed.append(t.text)
    elif "signed" in t.text:
        list_signed.append(t.text)

os.remove("signed.json")
os.remove("re_signed.json")


if "all_players.json":
    with open("all_players.json", 'r') as f:
        all_players = json.load(f)

with open("signed.json", 'w') as f:
    for transfer in list_signed:
        dict_json = parse_to_json(transfer, list_teams, all_players) 
        if dict_json != -1:
            dict_signed.update(dict_json)
    json.dump(dict_signed, f, indent=1)

with open("re_signed.json", "w") as f:
    for transfer in list_re_signed:
        dict_json = parse_to_json(transfer, list_teams, all_players)
        if dict_json != -1:
            dict_re_signed.update(dict_json)
    json.dump(dict_re_signed, f, indent=1)