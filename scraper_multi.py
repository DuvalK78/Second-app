import requests
from bs4 import BeautifulSoup
import json
import time

# Liste de sites : facile à étendre
SITES = [
    {
        "name": "Matériel.net",
        "url": "https://www.materiel.net/",
        "selectors": {
            "item": ".product_pod",
            "title": "h3 a",
            "price": ".price_color",
            "image": "img",
            "link": "h3 a"
        }
    },
    # Tu peux rajouter 10 sites ici...
]

deals = []

for site in SITES:
    print(f"→ Scraping {site['name']}...")

    try:
        res = requests.get(site["url"], timeout=8)
        res.raise_for_status()

        soup = BeautifulSoup(res.text, "html.parser")

        for item in soup.select(site["selectors"]["item"]):
            title = item.select_one(site["selectors"]["title"])["title"]
            price = item.select_one(site["selectors"]["price"]).text.strip()
            img = item.select_one(site["selectors"]["image"])["src"].replace("../", site["url"])
            link = item.select_one(site["selectors"]["link"])["href"].replace("../", site["url"])

            deals.append({
                "site": site["name"],
                "title": title,
                "price": price,
                "image": img,
                "link": link
            })

        time.sleep(1)  # éviter de spam trop vite

    except Exception as e:
        print(f"⚠ Erreur sur {site['name']} : {e}")


with open("deals.json", "w", encoding="utf-8") as f:
    json.dump(deals, f, indent=4, ensure_ascii=False)

print("✔ Scraping terminé, fichier deals.json mis à jour !")
