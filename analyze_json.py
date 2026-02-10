import json

with open("captured_api_responses.json", "r", encoding="utf-8") as f:
    items = json.load(f)

for item in items:
    if "place/summary" in item["url"]:
        print(f"Found place/summary content from: {item['url']}")
        data = item["data"]
        print("Keys in data:", data.keys())
        print("Sample data:", json.dumps(data, ensure_ascii=False, indent=2))
        break
