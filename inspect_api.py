import asyncio
import json
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        # Search query
        keyword = "서울 빵집"
        
        # Store captured data
        captured_data = []

        # Define handler for responses
        async def handle_response(response):
            # Log all URLs to see what's happening
            # print(f"Response: {response.url} ({response.headers.get('content-type', '')})")
            
            try:
                # Capture all JSON-like responses
                ct = response.headers.get("content-type", "").lower()
                if "json" in ct or "application/graphql" in ct:
                    # filter out some noise
                    if "log" in response.url or "monitor" in response.url:
                        return

                    try:
                        data = await response.json()
                        captured_data.append({
                            "url": response.url,
                            "type": ct,
                            "data": data
                        })
                        print(f"Captured JSON from: {response.url}")
                    except:
                        pass
            except Exception as e:
                pass

        page.on("response", handle_response)

        # Go to Naver Maps
        print("Navigating to Naver Maps...")
        await page.goto(f"https://map.naver.com/p/search/{keyword}")
        
        # Wait for results to load
        try:
            # Wait for the iframe that contains the list
            await page.wait_for_selector("iframe#searchIframe", timeout=20000)
            print("Search iframe found.")
            
            # Switch to iframe
            frame_element = await page.wait_for_selector("iframe#searchIframe")
            frame = await frame_element.content_frame()
            
            # Wait for list items to appear to ensure data is loaded
            await frame.wait_for_selector("li", timeout=20000)
            print("List items loaded.")
            
            # Scroll down to trigger more
            await frame.evaluate("window.scrollTo(0, 1000)")
            await asyncio.sleep(5)
            
        except Exception as e:
            print(f"Error waiting for content: {e}")

        # Save captured data to inspect structure
        with open("captured_api_responses.json", "w", encoding="utf-8") as f:
            json.dump(captured_data, f, ensure_ascii=False, indent=2)
            
        print(f"Captured {len(captured_data)} JSON responses. Saved to captured_api_responses.json")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
