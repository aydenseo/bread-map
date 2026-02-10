import json

with open("captured_api_responses.json", "r", encoding="utf-8") as f:
    items = json.load(f)

found_rating = False
for item in items:
    if "allSearch" in item["url"]:
        data = item["data"]
        place_list = data.get("result", {}).get("place", {}).get("list", [])
        
        for p in place_list:
            print(f"Name: {p.get('name')}")
            # print all keys and values that look like a number < 5 and > 0
            for k, v in p.items():
                if isinstance(v, (int, float, str)):
                    try:
                        f = float(v)
                        if 3.0 <= f <= 5.0 and "id" not in k and "x" not in k and "y" not in k:
                            print(f"  candidate rating? {k}: {v}")
                            found_rating = True
                    except:
                        pass
                        
            # Check specifically known keys
            if "score" in p:
                print(f"  score: {p['score']}")
            if "grade" in p:
                print(f"  grade: {p['grade']}")
            if "rating" in p:
                print(f"  rating: {p['rating']}")
                
print(f"Found any rating candidate? {found_rating}")
