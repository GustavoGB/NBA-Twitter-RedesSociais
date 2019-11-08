from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import json
import os
from collections import defaultdict


list_teams = ["Golden State Warriors", "LA Clippers","Boston Celtics", "Chicago Bulls", "Houston Rockets", "Cleveland Cavaliers", 
                "Dallas Mavericks", "Los Angeles Lakers", "Brooklyn Nets", "Memphis Grizzlies", "Washington Wizards", "Oklahoma City Thunder", 
                "Miami Heat", "Minnesota Timberwolves", "Indiana Pacers", "Denver Nuggets", "Charlotte Hornets", "Philadelphia 76ers", 
                "Portland Trail Blazers", "Boston Celtics", "Milwaukee Bucks", "New Orleans Pelicans", "Toronto Raptors", "Phoenix Suns",
                "New York Knicks", "Detroit Pistons", "Utah Jazz", "Sacramento Kings", "Atlanta Hawks", "Orlando Magic", "San Antonio Spurs"]

if "all_players.json":
    with open("all_players.json", 'r') as f:
        all_players = json.load(f)

def parse_to_json(transfer, year, list_teams, list_players):
    dict_json = {}
    key = None
    key_team = None

    for player in list_players:
        if player in transfer:
            key = player
    if key == None: 
        return -1
    
    for team in list_teams:
        if team in transfer:
            key_team = team
    if key_team == None: #Caso o time não esteja na base, não queremos adicionar uma chave vazia
        return -1
    l_temp = []
    l_temp.append(key_team)
    l_temp.append(year)
    dict_json[key] = l_temp
    return dict_json


driver = webdriver.Chrome(executable_path=r'C:\Users\Victo\Downloads\chromedriver_win32\chromedriver.exe')
driver.get("https://stats.nba.com/transactions/")
print(driver.current_url)
assert "" in driver.current_url

for i in range(100):
    try:
        see_more = driver.find_element_by_xpath("//div[@class='button-container small-12 columns']/a[@class='button']")

        actions = ActionChains(driver)
        actions.move_to_element(see_more)
        actions.perform()

        see_more.click()

    except:
        break #CHEGOU NO COMEÇO DE 2015 

containers = driver.find_elements_by_xpath("//div[@class='transactions-list__date columns large-12']")
dict_transferencias_signed = {}
dict_transferencias_waived = {}
dict_waived = defaultdict(list)
dict_signed = defaultdict(list)
for i in range(len(containers)):
    dict_json = {}
    all_container_transfers = 0
    container_transfer = 0
    #i+1 pega cada container
    #pegar a data do container
    ano = driver.find_element_by_xpath("//div[@class='transactions-list__date columns large-12']" + "[" + str(i+1) + "]" + "/div[@class='small-12 large-2 columns transactions-list__date']/span")
    virg1 = ano.text.find(",")
    string = ano.text[virg1+1:] #Achando só o ano
    virg2 = string.find(",")
    string_ano = string[virg2+2:] #+2 por causa do espaço
    
    
    #pegar as transferencias do container
    print(i+1, ano.text)
    last_transf = driver.find_element_by_xpath("//div[@class='transactions-list__date columns large-12']" + "[" + str(i+1) + "]" + "/div[@class='small-12 large-10 columns']/div[@class='small-12 large-12 columns transactions-list__container last']/div[@class='transactions-list__description small-6 medium-5 large-6 columns']")
    #print("----")
    #print(last_transf.text)
    #print("----")
    all_container_transfers = driver.find_elements_by_xpath("//div[@class='transactions-list__date columns large-12']" + "[" + str(i+1) + "]" + "/div[@class='small-12 large-10 columns']/div")
    if(len(all_container_transfers) > 1):
        for j in range(len(all_container_transfers)-1):
            container_transfer = driver.find_element_by_xpath("//div[@class='transactions-list__date columns large-12']" + "[" + str(i+1) + "]" + "/div[@class='small-12 large-10 columns']/div[@class='small-12 large-12 columns transactions-list__container']" + "[" + str(j+1) + "]" + "/div[@class='transactions-list__description small-6 medium-5 large-6 columns']")
            #colocar as transferencias numa lista e a last por ultimo
            if "re-signed" in container_transfer.text:
                pass
            elif "signed" in container_transfer.text:
                dict_json = parse_to_json(container_transfer.text, string_ano, list_teams, all_players) 
                if dict_json != -1:
                    for key,value in dict_json.items():
                        if(key in dict_signed):
                            print("repetido signed", dict_json)
                            dict_signed[key].append(value)
                        else:
                            l_temp = []
                            l_temp.append(value)
                            dict_signed[key] = l_temp

            elif "waived" in container_transfer.text:
                dict_json = parse_to_json(container_transfer.text, string_ano, list_teams, all_players) 
                if dict_json != -1:
                    for key,value in dict_json.items():
                        if(key in dict_waived):
                            print("repetido waived", dict_json)
                            dict_waived[key].append(value)
                        else:
                            l_temp = []
                            l_temp.append(value)
                            dict_waived[key] = l_temp

    #colocar a last na lista
    if "re-signed" in last_transf.text:
        pass
    elif "signed" in last_transf.text:
        dict_json = parse_to_json(last_transf.text, string_ano, list_teams, all_players) 
        if dict_json != -1:
            for key,value in dict_json.items():
                if(key in dict_signed):
                    print("repetido signed", dict_json)
                    dict_signed[key].append(value)
                else:
                    l_temp = []
                    l_temp.append(value)
                    dict_signed[key] = l_temp

    elif "waived" in last_transf.text:
        dict_json = parse_to_json(last_transf.text, string_ano, list_teams, all_players) 
        if dict_json != -1:
            for key,value in dict_json.items():
                if(key in dict_waived):
                    print("repetido waived", dict_json)
                    dict_waived[key].append(value)
                else:
                    l_temp = []
                    l_temp.append(value)
                    dict_waived[key] = l_temp

try:
    os.remove("signed.json")
    os.remove("waived.json")
except:
    pass

with open("signed.json", 'w') as f:
    json.dump(dict_signed, f, indent=1)

with open("waived.json", "w") as f:
    json.dump(dict_waived, f, indent=1)