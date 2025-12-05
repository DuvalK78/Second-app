import requests
from bs4 import BeautifulSoup
import json
import time

# ---------- SCRAPER MATÉRIEL.NET ----------
def scrape_materielnet(url):
    try:
        html = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}).text
        soup = BeautifulSoup(html, "html.parser")

        title = soup.select_one("h1.product__name").get_text(strip=True)

        img = soup.select_one(".product__visual img")
        image_url = img["src"] if img else None

        price_raw = soup.select_one(".product__price .price")
        price = None
        if price_raw:
            price = float(
                price_raw.get_text(strip=True)
                .replace("€", "")
                .replace(",", ".")
                .replace(" ", "")
            )

        old_price_raw = soup.select_one(".product__price .price--striked")
        old_price = None
        if old_price_raw:
            old_price = float(
                old_price_raw.get_text(strip=True)
                .replace("€", "")
                .replace(",", ".")
                .replace(" ", "")
            )

        return {
            "title": title,
            "url": url,
            "source": "materiel.net",
            "timestamp": int(time.time() * 1000),
            "price": price,
            "old_price": old_price,
            "tags": ["materiel.net", "tech", "promo"],
            "image": image_url
        }

    except Exception as e:
        print(f"[ERREUR Matériel.net] {url} -> {e}")
        return None


# ---------- LISTE DES PRODUITS À SCRAPER ----------
PRODUCT_URLS = [
    "https://www.materiel.net/produit/202503180031.html"
]

# ---------- ROUTAGE VERS LE BON SCRAPER ----------
def scrape_url(url):
    if "materiel.net" in url:
        return scrape_materielnet(url)
    else:
        print(f"❌ Aucun scraper pour : {url}")
        return None


# ---------- MAIN ----------
def main():
    deals = []

    for url in PRODUCT_URLS:
        print(f"Scraping : {url}")
        data = scrape_url(url)
        if data:
            deals.append(data)

    # Sauvegarde
    with open("deals.json", "w", encoding="utf-8") as f:
        json.dump(deals, f, indent=4, ensure_ascii=False)

    print("\n✔ Scraping terminé ! deals.json mis à jour.\n")


if __name__ == "__main__":
    main()
