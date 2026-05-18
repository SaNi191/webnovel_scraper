import requests
import csv
import time

MAX_OFFSET = 10000

data = []
offset = 0

while offset < MAX_OFFSET:
    response = requests.get(f"https://api.mangadex.org/manga?limit=100&offset={offset}")
    manga = response.json()
    data.extend(manga["data"])
    offset += 100
    time.sleep(0.2)

with open("manga_tags.csv", "w", newline="", encoding="utf-8") as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(["Manga Title", "Tag Name"])
    for manga in data:
        # Getting the English title of the manga, if possible
        manga_title = list(manga["attributes"]["title"].values())[0]
        for titles in manga["attributes"]["altTitles"]:
            if "en" in titles:
                manga_title = list(titles.values())[0]
                break

        # Creating the list of tag names    
        tag_names = ", ".join([
                    tag["attributes"]["name"]["en"] 
                    for tag in manga["attributes"]["tags"]
                    ])
        csvwriter.writerow([manga_title, tag_names])

print("Data has been written to manga_tags.csv")