import asyncio
from playwright.async_api import async_playwright

async def scrape_zoommer_phones():
    async with async_playwright() as p:
        # ვუშვებთ ბრაუზერს სტანდარტულ რეჟიმში
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        
        url = "https://zoommer.ge/mobiluri-telefonebi-c855"
        print(f"🔍 Accessing Zoommer (Standard Load): {url}")
        
        results = []

        try:
            # ვიყენებთ "networkidle"-ს, რომ დაველოდოთ ყველა ფასის ჩატვირთვას
            await page.goto(url, wait_until="networkidle", timeout=60000)
            
            # ველოდებით პროდუქტების კონტეინერს
            await page.wait_for_selector('div[id^="product-"]', timeout=20000)

            # ვიღებთ მხოლოდ იმას, რაც პირველ გვერდზეა (28 პროდუქტი)
            products = await page.query_selector_all('div[id^="product-"]')
            
            for item in products:
                # სახელი title ატრიბუტიდან
                name_elem = await item.query_selector('a[title]')
                # ფასი ლარის სიმბოლოს მიხედვით
                price_elem = await item.query_selector('text="₾"')
                
                if name_elem and price_elem:
                    name = (await name_elem.get_attribute('title')).strip()
                    price_raw = await price_elem.inner_text()
                    # ვტოვებთ მხოლოდ ციფრებს ფასში
                    clean_price = "".join(filter(str.isdigit, price_raw))
                    
                    if name and clean_price:
                        results.append({
                            "name": name,
                            "price": clean_price,
                            "currency": "GEL"
                        })

            # დუბლიკატებისგან დაზღვევა
            unique_results = list({res['name']: res for res in results}.values())
            print(f"✅ Success! Captured {len(unique_results)} products.")
            return unique_results

        except Exception as e:
            print(f"❌ Scraper error: {e}")
            return []
        finally:
            await browser.close()