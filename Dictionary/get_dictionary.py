import requests
import json
import pandas as pd
from bs4 import BeautifulSoup

# import json
# with open('data.json', 'w') as f:
#     json.dump(data, f)

# import json
# with open('data.json', 'w', encoding='utf-8') as f:
#     json.dump(data, f, ensure_ascii=False, indent=4)
    
    
url = "https://ebird.org/region/TW/bird-list"
headers = {"Cookie": "I18N_LANGUAGE=zh"}
response = requests.get(url, headers=headers)
if response.status_code != 200:
    print("failed to get all short name")


soup = BeautifulSoup(response.text, "html.parser")

bird_cnt = 0
name_to_class = {}
class_to_name = {}

# find native bird
bird_list = soup.find("section", attrs={"aria-labelledby": "nativeNaturalized"})
bird_list = bird_list.find_all("li")    
for bird in bird_list:
    short_name = bird.get("id")
    chinese_name = bird.find("span", class_="Species-common").text
    
    name_to_class[short_name] = bird_cnt
    name_to_class[chinese_name] = bird_cnt
    
    class_to_name[bird_cnt] = [short_name, chinese_name]
    
    bird_cnt += 1
    

# find provisional bird
bird_list = soup.find("section", attrs={"aria-labelledby": "provisional"})
bird_list = bird_list.find_all("li")    
for bird in bird_list:
    short_name = bird.get("id")
    chinese_name = bird.find("span", class_="Species-common").text
    
    name_to_class[short_name] = bird_cnt
    name_to_class[chinese_name] = bird_cnt
    
    class_to_name[bird_cnt] = [short_name, chinese_name]
    
    bird_cnt += 1
    
    
with open(file="./data/json/class_to_name.json", mode="w", encoding="utf-8") as f:
    json.dump(class_to_name, f, ensure_ascii=False, indent=4)

with open(file="./data/json/name_to_class.json", mode="w", encoding="utf-8") as f:
    json.dump(name_to_class, f, ensure_ascii=False, indent=4)