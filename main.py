import requests
import csv

response = requests.get("https://api.mangadex.org/manga?limit=10")

data = response.json()

for manga in data["data"]:
    for tag in manga["attributes"]["tags"]:
        print(tag["attributes"]["name"]["en"])

with open("manga_tags.csv", "w", newline="", encoding="utf-8") as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(["Manga Title", "Tag Name"])
    for i, manga in enumerate(data["data"]):
        # Getting the English title of the manga, if possible
        manga_title = manga["attributes"]["title"]
        for titles in manga["attributes"]["altTitles"]:
            if "en" in titles:
                manga_title = titles["en"]
                break

        # Creating the list of tag names    
        tag_names = ", ".join([
                    tag["attributes"]["name"]["en"] 
                    for tag in manga["attributes"]["tags"]
                    ])
        csvwriter.writerow([manga_title, tag_names])