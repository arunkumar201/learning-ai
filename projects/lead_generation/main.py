import asyncio
from crawl4ai import AsyncWebCrawler
from dotenv import load_dotenv
from utils.scraper_utils import get_browser_config, fetch_and_process_venue_page
from utils.scraper_utils import get_llm_strategy_for_venue
from utils.data_utils import save_venues_to_xlsx
from config import VENUE_BASE_URL, VENUE_CSS_SELECTOR, REQUIRED_KEYS
from uuid import uuid4

load_dotenv()


async def crawl_venue():
    """
    this is a placeholder function for crawling a venue.
    """
    print("Crawling venue...")
    # Initialize borwser,crawler and llm strategy configuration
    browser_config = get_browser_config()
    llm_strategy = get_llm_strategy_for_venue()

    # As Venue websitr might have pagination, we need to loop through the pages
    page_number = 1
    all_venues = []
    seen_names = set()
    session_id = uuid4()

    # Start the web crawler process
    async with AsyncWebCrawler(
        config=browser_config, llm_strategy=llm_strategy
    ) as crawler:
        while True:
            venues, not_result = await fetch_and_process_venue_page(
                crawler,
                page_number,
                base_url=VENUE_BASE_URL,
                css_selector=VENUE_CSS_SELECTOR,
                llm_strategy=llm_strategy,
                session_id=session_id,
                required_keys=REQUIRED_KEYS,
                seen_names=seen_names,
            )
            if not_result | page_number == 2:
                print("No more results found.")
                break
            if not venues:
                print("No venues found on page", page_number)
                break
            all_venues.extend(venues)
            page_number += 1
            print(f"Page {page_number}: {len(venues)} venues found.")
            # add some delay to avoid overwhelming the website
            await asyncio.sleep(1)
    #  Save all extracted venues to a CSV file
    if all_venues:
        save_venues_to_xlsx(all_venues, "complete_venues")
        print(f"Saved {len(all_venues)} venues to 'complete_venues.csv'.")
    else:
        print("No venues were found during the crawl.")

    # Display usage statistics for the LLM strategy
    llm_strategy.show_usage()


# start file
async def main():
    await crawl_venue()


if __name__ == "__main__":
    asyncio.run(main())
