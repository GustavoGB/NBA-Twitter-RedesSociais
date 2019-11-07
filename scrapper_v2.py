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


def parse_to_json(transfer, year, list_teams, list_players):
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
for i in range(len(containers)):
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
                dict_transferencias_signed[container_transfer.text] = string_ano
                dict_transferencias_signed[last_transf.text] = string_ano
            elif "waived" in container_transfer.text:
                dict_transferencias_waived[container_transfer.text] = string_ano
                dict_transferencias_waived[last_transf.text] = string_ano

    else:
        #colocar a last na lista
        if "re-signed" in last_transf.text:
            pass
        elif "signed" in last_transf.text:
            dict_transferencias_signed[last_transf.text] = string_ano
        elif "waived" in last_transf.text:
            dict_transferencias_waived[last_transf.text] = string_ano

try:
    os.remove("signed.json")
    os.remove("waived.json")
except:
    pass

if "all_players.json":
    with open("all_players.json", 'r') as f:
        all_players = json.load(f)
print("Colocando nos jsons...")
dict_signed = {}
with open("signed.json", 'w') as f:
    for key in dict_transferencias_signed:
        dict_json = parse_to_json(key, dict_transferencias_signed[key], list_teams, all_players) 
        if dict_json != -1:
            dict_signed.update(dict_json)
    json.dump(dict_signed, f, indent=1)

dict_waived = {}
with open("waived.json", "w") as f:
    for transfer in dict_transferencias_waived:
        dict_json = parse_to_json(transfer, dict_transferencias_waived[key], list_teams, all_players) 
        if dict_json != -1:
            dict_waived.update(dict_json)
    json.dump(dict_waived, f, indent=1)