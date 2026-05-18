import requests
import csv
import time

MAX_OFFSET = 10000
MAX_RETRIES = 2
SUCCESS_STATUS = 200

offset = 0
retry_count = 0

with open("manga_tags.csv", "w", newline="", encoding="utf-8") as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(["Manga Title", "Tag Name"])
    while offset < MAX_OFFSET:

        response = requests.get(
            "https://api.mangadex.org/manga",
            params= {
                "limit": 100,
                "offset": offset
            }
        )

        try:
            response.raise_for_status()

        except requests.RequestException as e:

            print(f"Error fetching data for offset {offset}: {e}")
            retry_count += 1

            if retry_count >= MAX_RETRIES:
                print("Max retry attempts reached. Exiting.")
                offset += 100
                retry_count = 0
            time.sleep(2 ** retry_count)  # Wait before retrying
            continue
            
        data = response.json()

        for manga in data["data"]:
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

        retry_count = 0
        offset += 100
        time.sleep(0.5)

print("Data has been written to manga_tags.csv")