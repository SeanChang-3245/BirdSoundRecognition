import requests
import os
import json
from bs4 import BeautifulSoup


def get_count(bird_url):
    short_name = bird_url.split("/")[-1]
    api_url = f"https://ebird.org/ml-search-api/v2/stats/obs?speciesCode={short_name}"

    headers = {}
    response = requests.get(api_url, headers=headers)
    
    if response.status_code != 200:
        print(f"failed to get {short_name} record count")
        return 0

    data = response.json()
    num = data["countsWithAudio"]
    return num
    

def download_bird_sound(record_url, dir_name):
    response = requests.get(record_url)
    if response.status_code != 200:
        print("failed to download")
        return
    
    file_name = f"{dir_name}/1.mp3"
    
    if response:
        with open(file_name, "wb") as file:
            file.write(response.content)
        print("-" * 30)
    else:
        print("failed to download audio")
    

def fetch_one_bird_sound(bird_url, dir_name):
    print(f"downloading from {bird_url} to {dir_name}")
    
    headers = {}
    response = requests.get(bird_url, headers=headers)
    
    if response.status_code != 200:
        print("failed to load page")
        return
    
    print(f"{get_count(bird_url=bird_url)} record in total")
    
    print("-" * 30)    
    


def main():
    NUMBER_OF_BIRDS = 672
    NUMBER_OF_BIRDS = 5
    url = "https://ebird.org/region/TW/bird-list"
    
    
    headers = {"Cookie": "I18N_LANGUAGE=zh"}
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print("failed to load page")
        return
    
    soup = BeautifulSoup(response.text, "html.parser")
    species_list = soup.find_all("a", class_="Species Species--h4")
        
    for i in range(NUMBER_OF_BIRDS):
        bird = species_list[i]
        
        bird_zh_name = bird.find("span",  class_="Species-common").text
        bird_url = bird.get("href")[:-3] # used to acquire the global data, not only the data in Taiwan
        
        print(bird_zh_name)
        print(bird_url)
        dir_name = f"data/{bird_zh_name}"
        
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

        fetch_one_bird_sound(bird_url=bird_url, dir_name=dir_name)
    
    pass

if __name__ == "__main__":
    # download_bird_sound("https://cdn.download.ams.birds.cornell.edu/api/v2/asset/621596400/mp3", "./test/")
    main()