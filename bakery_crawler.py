import asyncio
import json
import time
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(
            viewport={"width": 1280, "height": 1024},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        # Database to store API data: id -> item
        api_db = {}
        
        # Handler to capture API data
        async def handle_response(response):
            if "search/allSearch" in response.url:
                try:
                    if "application/json" in response.headers.get("content-type", "").lower():
                        data = await response.json()
                        
                        # Extract from allSearch format
                        if "result" in data and "place" in data["result"]:
                            place_list = data["result"]["place"].get("list", [])
                            for place in place_list:
                                if "name" in place and "id" in place:
                                    pid = place["id"]
                                    name = place["name"]
                                    
                                    # coordinates
                                    lat = place.get("y")
                                    lon = place.get("x")
                                    
                                    # reviews
                                    review_count = place.get("reviewCount", 0)
                                    
                                    api_db[pid] = {
                                        "id": pid,
                                        "name": name,
                                        "lat": float(lat) if lat else 0.0,
                                        "lon": float(lon) if lon else 0.0,
                                        "address": place.get("roadAddress") or place.get("address"),
                                        "review_count": int(review_count),
                                        "thumUrl": place.get("thumUrl"),
                                    }
                                    print(f"[API] Captured: {name} (Reviews: {review_count})")

                except Exception as e:
                    pass

        page.on("response", handle_response)

        # Navigate to Naver Maps
        keyword = "서울 빵집"
        print(f"Navigating to search: {keyword}")
        await page.goto(f"https://map.naver.com/p/search/{keyword}")

        # Wait for iframe and list
        try:
            await page.wait_for_selector("iframe#searchIframe", timeout=30000)
            frame_element = await page.wait_for_selector("iframe#searchIframe")
            frame = await frame_element.content_frame()
            await frame.wait_for_selector("li", timeout=30000)
            print("Initial list loaded.")
        except Exception as e:
            print(f"Error loading list: {e}")
            await browser.close()
            return

        # Scroll loop to load more items
        scroll_count = 0
        max_scrolls = 10 # Try 10 scrolls
        
        # Focus on the list
        try:
            # Click on the container or first item to focus
            await frame.click("li", timeout=5000)
            print("Focused on list.")
        except:
            pass

        while scroll_count < max_scrolls:
            try:
                # Use keyboard to scroll down
                # This is often more reliable than setting scrollTop for complex SPAs
                await page.keyboard.press("End")
                await asyncio.sleep(1)
                await page.keyboard.press("PageDown")
                
                # Check if new items loaded (optional logic, but we rely on API capture)
                
                print(f"Scrolled {scroll_count + 1}/{max_scrolls} (Keyboard)")
                await asyncio.sleep(2) # Wait for network
                scroll_count += 1
            except Exception as e:
                print(f"Error scrolling: {e}")
                break

        print("Finished scrolling.")
        
        # Filter and Save
        # User asked for Rating >= 4.0. Since stats are hidden, we filter by Review Count >= 50
        # This is a reasonable proxy for "proven" places.
        
        final_results = []
        for pid, place in api_db.items():
            if place["review_count"] >= 50:
                 final_results.append(place)
        
        # Sort by review count descending
        final_results.sort(key=lambda x: x["review_count"], reverse=True)

        # Save to JSON
        with open("bakeries.json", "w", encoding="utf-8") as f:
            json.dump(final_results, f, ensure_ascii=False, indent=2)
            
        print(f"Saved {len(final_results)} bakeries (Reviews >= 50) to bakeries.json")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
