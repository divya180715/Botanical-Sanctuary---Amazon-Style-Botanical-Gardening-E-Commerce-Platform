import urllib.request
import re
import json

terms = [
    "indoor-plant", "monstera", "snake-plant", "succulent", "pothos", 
    "flower-seeds", "sunflower", "lavender", "herbs", "marigold",
    "flower-pot", "ceramic-pot", "terracotta-pot", "planter", "hanging-plant",
    "terrarium", "plant-stand", "living-wall", "propagation-station", "seagrass-basket",
    "pruning-shears", "watering-can", "gardening-tools", "garden-trowel", "garden-hose"
]

found_photos = {}

for term in terms:
    url = f"https://unsplash.com/napi/search/photos?query={term}&per_page=10"
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        resp = urllib.request.urlopen(req, timeout=5)
        data = json.loads(resp.read().decode('utf-8'))
        results = data.get('results', [])
        for item in results:
            pid = item['id']
            raw_url = item['urls']['raw']
            desc = item.get('alt_description') or item.get('description') or term
            img_url = f"{raw_url}&auto=format&fit=crop&w=800&q=80"
            if pid not in found_photos:
                found_photos[pid] = {
                    "id": pid,
                    "url": img_url,
                    "desc": desc,
                    "query": term
                }
    except Exception as e:
        print(f"Error searching {term}: {e}")

print(f"Total authentic botanical photos found: {len(found_photos)}")

with open("botanical_photos.json", "w", encoding="utf-8") as f:
    json.dump(found_photos, f, indent=2)
