import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        # iPhone 12 Pro UA
        iphone_ua = "Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1"
        
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent=iphone_ua,
            viewport={"width": 390, "height": 844},
            is_mobile=True,
            has_touch=True
        )
        page = await context.new_page()

        # Capture API
        async def handle_response(response):
            if "search" in response.url or "graphql" in response.url:
                if "json" in response.headers.get("content-type", "").lower():
                    try:
                        data = await response.json()
                        # print data keys to see if they differ
                        if "result" in data and "place" in data["result"]:
                            list_items = data["result"]["place"]["list"]
                            if list_items:
                                print(f"Captured {len(list_items)} items with Mobile UA")
                                print("Sample Item Keys:", list_items[0].keys())
                                if "score" in list_items[0] or "grade" in list_items[0]:
                                    print("FOUND RATING IN API!")
                    except:
                        pass
        
        page.on("response", handle_response)
        
        print("Navigating to mobile Naver Maps...")
        await page.goto("https://m.map.naver.com/search2/search.naver?query=%EC%84%9C%EC%9A%B8%20%EB%B9%B5%EC%A7%91")
        
        await page.wait_for_timeout(5000)
        
        # Also dump body text to see if rating is visible
        text = await page.inner_text("body")
        print("Body text sample (first 500 chars):")
        print(text[:500])
        
        # Check for star rating pattern
        if "별점" in text or "4." in text:
            print("Possible rating in text.")
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
