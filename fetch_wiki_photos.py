import urllib.request
import json
import os

WIKI_API = "https://en.wikipedia.org/w/api.php"

# Dictionary of product IDs to Wikipedia search queries
QUERY_MAP = {
    # Live plants
    "p-101": "Monstera deliciosa",
    "p-102": "Sansevieria trifasciata",
    "p-103": "Ficus lyrata",
    "p-104": "Spathiphyllum",
    "p-105": "Echeveria",
    "p-106": "Epipremnum aureum",
    "p-107": "Zamioculcas",
    "p-108": "Dypsis lutescens",

    # Seeds
    "s-201": "Wildflower",
    "s-202": "Bonsai",
    "s-203": "Herb",
    "s-204": "Lavandula",
    "s-205": "Helianthus annuus",
    "s-206": "Tagetes",
    "s-207": "Basil",
    "s-208": "Zinnia elegans",

    # Pots & Planters
    "pot-301": "Flowerpot",
    "pot-302": "Macramé",
    "pot-303": "Terracotta",
    "pot-304": "Sub-irrigated planter",
    "pot-305": "Ceramic",
    "pot-306": "Window box",
    "pot-307": "Porcelain",
    "pot-308": "Pottery",

    # Decor
    "dec-401": "Terrarium",
    "dec-402": "Houseplant",
    "dec-403": "Glass",
    "dec-404": "Preserved moss",
    "dec-405": "Hydroponics",
    "dec-406": "Bamboo",
    "dec-407": "Basket weaving",
    "dec-408": "Fairy lights",

    # Tools
    "tool-501": "Secateurs",
    "tool-502": "Watering can",
    "tool-503": "Soil pH",
    "tool-504": "Seaweed fertilizer",
    "tool-505": "Trowel",
    "tool-506": "Sprayer",
    "tool-507": "Garden hose",
    "tool-508": "Cultivator"
}

output_images = {}

for pid, title in QUERY_MAP.items():
    try:
        # Get page thumbnail image from Wikipedia API
        url = f"{WIKI_API}?action=query&titles={urllib.parse.quote(title)}&prop=pageimages&format=json&pithumbsize=800"
        req = urllib.request.Request(url, headers={'User-Agent': 'VerdantBotanics/1.0 (contact: admin@verdant.local)'})
        data = json.loads(urllib.request.urlopen(req, timeout=5).read().decode('utf-8'))
        pages = data.get('query', {}).get('pages', {})
        img_url = None
        for page_id, page_val in pages.items():
            if 'thumbnail' in page_val:
                img_url = page_val['thumbnail']['source']
                break
        if img_url:
            output_images[pid] = img_url
            print(f"FOUND [{pid}] {title} -> {img_url}")
        else:
            print(f"NO THUMBNAIL [{pid}] {title}")
    except Exception as e:
        print(f"ERROR [{pid}] {title} -> {e}")

print(f"\nTotal photos found: {len(output_images)} / {len(QUERY_MAP)}")
with open("wiki_photos.json", "w", encoding="utf-8") as f:
    json.dump(output_images, f, indent=2)
