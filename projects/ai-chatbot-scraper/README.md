# ai-chatbot-scraper

A scalable, anti-bot-aware ChatGPT.com scraper using [Crawl4AI](https://github.com/unclecode/crawl4ai).

## Features
- Submits a prompt to chatgpt.com
- Waits for the markdown response
- Saves the markdown, a screenshot, and a PDF
- Uses browser stealth to avoid detection
- Scalable and easy to extend

## Setup

1. Install dependencies:

```bash
pip install -r requirements.txt  # or use pyproject.toml with your tool
python -m playwright install
```

2. Run the scraper with your prompt:

```bash
python main.py "How to cook a pizza?"
```

- Outputs will be saved in the `outputs/` directory:
  - `chatgpt_response.html` (markdown as HTML)
  - `chatgpt_response.png` (screenshot)
  - `chatgpt_response.pdf` (PDF)

## Notes
- For best results, use proxies and rotate user agents if you encounter bot detection.
- If login is required, you must extend the `ChatGPTPromptHook` to handle authentication.
- This script is for educational and research purposes. Respect the site's terms of service.
