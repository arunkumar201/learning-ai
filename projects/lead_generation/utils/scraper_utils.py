import json
import os
from crawl4ai import (
    BrowserConfig,
    LLMExtractionStrategy,
    CrawlerRunConfig,
    AsyncWebCrawler,
    CacheMode,
)
from typing import List, Set
from dotenv import load_dotenv
from models.crawl_venue.venue import Venue
from utils.data_utils import is_complete_venue, is_duplicate_venue

load_dotenv()

ENV_TYPE = os.getenv("ENV_TYPE")


def get_browser_config() -> BrowserConfig:
    """
    Returns a BrowserConfig object with default settings.
    """
    browser_config = BrowserConfig(
        browser_type="chromium",
        headless=False,
        verbose=False,
        viewport_height=1080,
        viewport_width=1080,
        light_mode=False,
    )
    return browser_config


def get_llm_strategy_for_venue() -> LLMExtractionStrategy:
    """
    Returns a LLMExtractionStrategy object for venue data.
    """
    llm_strategy = LLMExtractionStrategy(
        provider="groq/deepseek-r1-distill-llama-70b",
        api_token="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",
        chunk_token_threshold=1000,
        schema=Venue.model_json_schema(),
        instruction=(
            "Extract all venue objects with 'name', 'location', 'price', 'capacity', and other necessary fields from the provided markdown content. "
            "'rating', 'reviews', and an effective and powerful sentence description of the venue from the following content."
        ),
        extraction_type="schema",
        input_format="markdown",
        verbose=False if ENV_TYPE == "PRODUCTION" else True,
    )
    return llm_strategy


async def has_more_results_venue(
    crawler: AsyncWebCrawler,
    url: str,
    session_id: str,
) -> bool:
    """
    Checks if the "No Results Found" message is present on the page.
    """
    result = await crawler.arun(
        url=url,
        config=CrawlerRunConfig(
            cache_mode=CacheMode.BYPASS,
            session_id=session_id,
        ),
    )

    if result.success:
        if "No Results Found" in result.cleaned_html:
            return True
    else:
        print(
            f"Error fetching page for 'No Results Found' check: {result.error_message}"
        )

    return False


async def fetch_and_process_venue_page(
    crawler: AsyncWebCrawler,
    page_number: int,
    base_url: str,
    css_selector: str,
    llm_strategy: LLMExtractionStrategy,
    session_id: str,
    required_keys: List[str],
    seen_names: Set[str],
):
    """
    Fetches and processes a page of venues.
    """
    url = f"{base_url}?page={page_number}"
    print(f"crawling page url {url}")
    print(f"Loading page {page_number}...")
    no_results = await has_more_results_venue(crawler, url, session_id)

    if no_results:
        return [], True

    # extract page content with the llm  extraction strategy
    result = await crawler.arun(
        url=url,
        config=CrawlerRunConfig(
            cache_mode=CacheMode.BYPASS,  # no cached data
            extraction_strategy=llm_strategy,
            css_selector=css_selector,
            session_id=session_id,  # Unique session ID for the crawl
        ),
    )

    if not (result.success and result.extracted_content):
        print(f"Error fetching page {page_number}: {result.error_message}")
        return [], False
    # Parse extracted content
    extracted_data = json.loads(result.extracted_content)
    if not extracted_data:
        print(f"No data found on page {page_number}")
        return [], False
    # process the extracted venue data
    complete_venues = []
    for venue in extracted_data:
        print("Processing venue:", venue)

        if venue.get("error") is False:
            venue.pop("error", None)

        if not is_complete_venue(venue, required_keys):
            continue

        if is_duplicate_venue(venue["name"], seen_names):
            print(f"Duplicate venue '{venue['name']}' found. Skipping.")
            continue

        seen_names.add(venue["name"])
        complete_venues.append(venue)

    if not complete_venues:
        print(f"No complete venues found on page {page_number}.")
        return [], False
    print(f"Extracted {len(complete_venues)} venues from page {page_number}.")
    return complete_venues, False
