from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import json

driver = webdriver.Chrome(executable_path=r'C:\Users\Victo\Downloads\chromedriver_win32\chromedriver.exe')
driver.get("https://stats.nba.com/players/list/")
print(driver.current_url)
assert "nba" in driver.current_url

def change_order(old_string):
    words = old_string.split() #Sempre tem apenas um ou dois sobrenomes
    if(len(words)==3):
        new_string = words[-1] + " " + words[0] + " " + words[1]
    else:
        new_string = words[-1] + " " + words[0]
    return new_string


players = driver.find_elements_by_xpath("//li[@class='players-list__name']")

list_player = []
for player in players:
    list_player.append(player.text.replace(',', ''))

for i in range(len(list_player)):
    list_player[i] = change_order(list_player[i])

with open("all_players.json", "w") as f:
    json.dump(list_player, f)