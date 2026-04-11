import asyncio
import schedule
import time
from src.database.models import init_db, save_price
from src.scraper.zoommer_scraper import scrape_zoommer_phones

async def run_analysis():
    print(f"🕒 Update started at: {time.ctime()}")
    init_db()
    
    print("🚀 Starting Zoommer scraper...")
    try:
        products = await scrape_zoommer_phones()
        if products:
            for item in products:
                # Store name is hardcoded to "Zoommer" to ensure accuracy
                save_price(item['name'], item['price'], item['currency'], "Zoommer")
            print(f"✅ Successfully updated {len(products)} products.")
        else:
            print("⚠️ No products found. Check scraper selectors.")
    except Exception as e:
        print(f"❌ Scraper error: {e}")

def job():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(run_analysis())
    finally:
        loop.close()

async def main():
    await run_analysis()
    schedule.every().day.at("03:00").do(job)

    print("⏳ Scheduler is running...")
    while True:
        schedule.run_pending()
        await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(main())