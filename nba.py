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

containers = driver.find_elements_by_xpath("//div[@class='transactions-list__date columns large-12']")
transfers = driver.find_elements_by_xpath("//div[@class='transactions-list__description small-6 medium-5 large-6 columns']")
#years = driver.find_elements_by_xpath("//div[@class='small-12 large-2 columns transactions-list__date']/span")
years = []
for i in range(len(containers)):
    print(i)
    all_containers_transfers = []
    arg = "//div[@class='transactions-list__date columns large-12']" + "[" + str(i+1) + "]" + "/" + "div[@class='small-12 large-2 columns transactions-list__date']/span"
    year = driver.find_element_by_xpath(arg)

    arg_last ="//div[@class='transactions-list__date columns large-12']" + "[" + str(i+1) + "]"+ "/div[@class='small-12 large-10 columns']/div[@class='small-12 large-12 columns transactions-list__container last']/div[@class='transactions-list__description small-6 medium-5 large-6 columns']"
    last = driver.find_element_by_xpath(arg_last)
    all_containers_transfers.append(last.text)

    j=1
    while(1):
        try:
            print("j:",j)
            arg1 ="//div[@class='transactions-list__date columns large-12']" + "[" + str(i+1) + "]"+ "/div[@class='small-12 large-10 columns']/div[@class='small-12 large-12 columns transactions-list__container']" + "[" + str(j) + "]"+ "/div[@class='transactions-list__description small-6 medium-5 large-6 columns']"
            container_transfer = driver.find_element_by_xpath(arg1)
            if(container_transfer):
                all_containers_transfers.append(container_transfer.text)
                j = j + 1
 
            else:
                break
        except Exception as e:
            break
    print("sai")
    virg1 = year.text.find(",")
    string = year.text[virg1+1:] #Achando só o ano
    virg2 = string.find(",")
    string = string[virg2+1:]

    for i in range(len(all_containers_transfers)): #criando uma lista de anos com o mesmo tamanho
        years.append(string)


print(len(years), len(transfers))

'''
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
    '''