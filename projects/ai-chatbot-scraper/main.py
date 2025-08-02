import asyncio
from pickle import TRUE
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode, ProxyConfig, ProxyRotationStrategy
from pathlib import Path
import sys
import base64
import json
import re

PROMPT = sys.argv[1] if len(sys.argv) > 1 else "Hello, ChatGPT!"
OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

# Updated selectors matching the new structure
SELECTORS = {
    "PROMPT_TEXTAREA": "textarea[name='prompt-textarea']",
    "PROMPT_CONTENTEDITABLE": "div#prompt-textarea",
    "STOP_STREAMING": '[aria-label="Stop streaming"]',
    "VOICE_MODE": 'button[data-testid="composer-speech-button"]',
    "MESSAGE_OUTPUT": ".markdown.prose.w-full.break-words",
    "SOURCES_BUTTON": 'button[aria-label="Sources"]',
    "UPLOAD_FILES_BUTTON": 'button[aria-label="Upload files and more"]',
    "NEW_CHAT_LINK": 'a[aria-label="New chat"]',
    "COPY_BUTTON": 'button[aria-label="Copy"]',
    "EDIT_IN_CANVAS": 'button[aria-label="Edit in canvas"]',
    "SEARCH_BUTTON": 'button[data-testid="composer-button-search"]',
    "WEB_SEARCH_BUTTON": 'button[aria-label="Search the web"]'
}

async def main():
    browser_config = BrowserConfig(
        headless=False,           # Set to False for debugging
        viewport_height=1900,
        user_agent_mode="random",
        viewport_width=1900,
    )

    # Properly escape the prompt for JavaScript
    def escape_js_string(text):
        """Escape special characters for JavaScript string literal"""
        return (text.replace('\\', '\\\\')
                   .replace('"', '\\"')
                   .replace("'", "\\'")
                   .replace('\n', '\\n')
                   .replace('\r', '\\r')
                   .replace('\t', '\\t'))
    
    escaped_prompt = escape_js_string(PROMPT)
    escaped_selectors = {k: escape_js_string(v) for k, v in SELECTORS.items()}

    # JavaScript to handle the prompt submission, response extraction, and sources button click
    js_code = [
        f'''
        (async () => {{
            console.log("Starting ChatGPT interaction...");
            
            // Wait for selector utility function
            const waitForSelector = (selector, timeout = 10000) => {{
                return new Promise((resolve, reject) => {{
                    const element = document.querySelector(selector);
                    if (element) {{
                        resolve(element);
                        return;
                    }}
                    
                    const observer = new MutationObserver(() => {{
                        const element = document.querySelector(selector);
                        if (element) {{
                            observer.disconnect();
                            resolve(element);
                        }}
                    }});
                    
                    observer.observe(document.body, {{
                        childList: true,
                        subtree: true
                    }});
                    
                    setTimeout(() => {{
                        observer.disconnect();
                        reject(new Error("Timeout waiting for selector: " + selector));
                    }}, timeout);
                }});
            }};
            
            try {{
                // First, try to enable web search if available
                console.log("Looking for web search button to enable...");
                try {{
                    const webSearchButton = document.querySelector("{escaped_selectors['SEARCH_BUTTON']}") ||
                                           document.querySelector("{escaped_selectors['WEB_SEARCH_BUTTON']}") ||
                                           document.querySelector('button[aria-label*="search"]') ||
                                           document.querySelector('button[data-testid*="search"]');
                    
                    if (webSearchButton && !webSearchButton.disabled) {{
                        console.log("Found web search button, clicking to enable...");
                        webSearchButton.click();
                        await new Promise(r => setTimeout(r, 1000)); // Wait for search to be enabled
                        console.log("Web search enabled");
                    }} else {{
                        console.log("Web search button not found or already enabled");
                    }}
                }} catch (searchError) {{
                    console.log("Could not enable web search:", searchError.message);
                }}
                
                // Find the ProseMirror contenteditable div (this is the actual input)
                let promptElement = null;
                
                try {{
                    promptElement = await waitForSelector("div#prompt-textarea.ProseMirror", 10000);
                    console.log("Found ProseMirror prompt input");
                }} catch (e) {{
                    try {{
                        promptElement = await waitForSelector("div#prompt-textarea", 10000);
                        console.log("Found contenteditable prompt input");
                    }} catch (e2) {{
                        try {{
                            promptElement = await waitForSelector("{escaped_selectors['PROMPT_TEXTAREA']}", 5000);
                            console.log("Found textarea prompt input");
                        }} catch (e3) {{
                            throw new Error("Could not find any prompt input element");
                        }}
                    }}
                }}
                
                const promptText = "{escaped_prompt}";
                console.log("Setting prompt text:", promptText.substring(0, 50) + "...");
                
                // Handle ProseMirror contenteditable div
                if (promptElement.classList.contains('ProseMirror') || promptElement.contentEditable === 'true') {{
                    console.log("Handling ProseMirror contenteditable");
                    
                    // Focus first
                    promptElement.focus();
                    await new Promise(r => setTimeout(r, 200));
                    
                    // Clear existing content by selecting all and deleting
                    document.execCommand('selectAll', false, null);
                    document.execCommand('delete', false, null);
                    
                    // Insert the text using document.execCommand (works better with ProseMirror)
                    document.execCommand('insertText', false, promptText);
                    
                    // Alternative method: set innerHTML and dispatch events
                    if (!promptElement.textContent || promptElement.textContent.trim() === '') {{
                        promptElement.innerHTML = '<p>' + promptText.replace(/\\n/g, '<br>') + '</p>';
                        
                        // Trigger various events that ProseMirror might be listening for
                        ['input', 'change', 'keyup', 'paste'].forEach(eventType => {{
                            const event = new Event(eventType, {{ bubbles: true, cancelable: true }});
                            promptElement.dispatchEvent(event);
                        }});
                        
                        // Also trigger InputEvent
                        const inputEvent = new InputEvent("input", {{
                            bubbles: true,
                            cancelable: true,
                            inputType: "insertText",
                            data: promptText
                        }});
                        promptElement.dispatchEvent(inputEvent);
                    }}
                    
                }} else if (promptElement.tagName.toLowerCase() === 'textarea') {{
                    console.log("Handling textarea");
                    promptElement.value = promptText;
                    promptElement.dispatchEvent(new Event("input", {{ bubbles: true }}));
                }}
                
                console.log("Prompt text set, waiting before submit...");
                await new Promise(r => setTimeout(r, 1000));
                
                // Find and click submit button
                let submitted = false;
                
                // Look for submit button in the form or nearby
                const form = promptElement.closest('form');
                if (form) {{
                    const submitButton = form.querySelector('button[type="submit"]') || 
                                       form.querySelector('button[data-testid="send-button"]') ||
                                       form.querySelector('button[aria-label="Send message"]') ||
                                       form.querySelector('button svg[data-testid="send-button"]')?.closest('button') ||
                                       form.querySelector('button:last-of-type');
                    
                    if (submitButton && !submitButton.disabled) {{
                        console.log("Clicking submit button");
                        submitButton.click();
                        submitted = true;
                    }}
                }}
                
                // If no submit button found, try finding it elsewhere
                if (!submitted) {{
                    const submitButton = document.querySelector('button[data-testid="send-button"]') ||
                                       document.querySelector('button[aria-label="Send message"]') ||
                                       document.querySelector('button svg[data-testid="send-button"]')?.closest('button');
                    
                    if (submitButton && !submitButton.disabled) {{
                        console.log("Clicking submit button (found outside form)");
                        submitButton.click();
                        submitted = true;
                    }}
                }}
                
                // Final fallback: press Enter
                if (!submitted) {{
                    console.log("No submit button found, pressing Enter");
                    promptElement.focus();
                    
                    // Try multiple Enter key events
                    const enterEvents = [
                        new KeyboardEvent('keydown', {{ key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true }}),
                        new KeyboardEvent('keypress', {{ key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true }}),
                        new KeyboardEvent('keyup', {{ key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true }})
                    ];
                    
                    enterEvents.forEach(event => promptElement.dispatchEvent(event));
                }}
                
                console.log("Prompt submitted");
                
                console.log("Waiting for response to start...");
                
                // Wait for response to start (stop streaming button appears)
                await waitForSelector("{escaped_selectors['STOP_STREAMING']}", 30000);
                console.log("Response started streaming");
                
                // Wait for streaming to complete
                const waitForStreamingToComplete = async () => {{
                    let lastTextContent = "";
                    let stableCount = 0;
                    const requiredStableChecks = 4; // Text must be stable for 4 consecutive checks
                    let attempts = 0;
                    const maxAttempts = 200; // 200 seconds max wait
                    
                    console.log("Monitoring response streaming...");
                    
                    while (attempts < maxAttempts) {{
                        attempts++;
                        
                        // Get the current response text
                        const messageElements = document.querySelectorAll("{escaped_selectors['MESSAGE_OUTPUT']}");
                        const lastElement = messageElements[messageElements.length - 1];
                        const currentTextContent = lastElement ? (lastElement.textContent || lastElement.innerText || "") : "";
                        
                        // Check if text content has changed
                        if (currentTextContent === lastTextContent && currentTextContent.length > 0) {{
                            stableCount++;
                            console.log(`Text stable for ${{stableCount}}/${{requiredStableChecks}} checks (attempt ${{attempts}}, length: ${{currentTextContent.length}})`);
                        }} else {{
                            stableCount = 0;
                            lastTextContent = currentTextContent;
                            if (attempts % 5 === 0) {{ // Log every 5th attempt to reduce spam
                                console.log(`Text still changing... (attempt ${{attempts}}, length: ${{currentTextContent.length}})`);
                            }}
                        }}
                        
                        // Check UI indicators
                        const stopButton = document.querySelector("{escaped_selectors['STOP_STREAMING']}");
                        const voiceButton = document.querySelector("{escaped_selectors['VOICE_MODE']}");
                        const stopButtonVisible = stopButton && stopButton.offsetParent !== null;
                        const voiceButtonVisible = voiceButton && voiceButton.offsetParent !== null;
                        
                        // Streaming is finished when:
                        // 1. Text has been stable for required checks AND
                        // 2. Stop button is no longer visible AND
                        // 3. Voice button is visible (indicates completion)
                        if (stableCount >= requiredStableChecks && !stopButtonVisible && voiceButtonVisible) {{
                            console.log("Streaming completed - text is stable and UI indicates completion");
                            return true;
                        }}
                        
                        // Additional check: if stop button disappears and we have stable text
                        if (stableCount >= 2 && !stopButtonVisible && currentTextContent.length > 50) {{
                            console.log("Streaming likely completed - stop button gone and text is stable");
                            await new Promise(r => setTimeout(r, 2000)); // Wait 2 more seconds
                            return true;
                        }}
                        
                        await new Promise(r => setTimeout(r, 1000)); // Check every second
                    }}
                    
                    console.log("Timeout waiting for streaming to complete, proceeding anyway");
                    return false;
                }};
                
                const streamingCompleted = await waitForStreamingToComplete();
                console.log("Response streaming phase completed:", streamingCompleted);
                
                // Wait an additional 2 seconds to ensure everything is rendered
                await new Promise(r => setTimeout(r, 2000));
                
                // Now look for and click the Sources button
                console.log("Looking for Sources button...");
                try {{
                    const sourcesButton = await waitForSelector("{escaped_selectors['SOURCES_BUTTON']}", 10000);
                    console.log("Found Sources button, clicking...");
                    sourcesButton.click();
                    
                    // Wait 3 seconds after clicking sources button as requested
                    console.log("Waiting 3 seconds after clicking Sources button...");
                    await new Promise(r => setTimeout(r, 3000));
                    console.log("Sources button clicked and waited 3 seconds");
                }} catch (sourcesError) {{
                    console.log("Sources button not found or not clickable:", sourcesError.message);
                }}
                
                // Extract the response
                const messageElements = document.querySelectorAll("{escaped_selectors['MESSAGE_OUTPUT']}");
                const lastElement = messageElements[messageElements.length - 1];
                const response = lastElement ? lastElement.innerHTML : null;
                
                // Extract chat ID from URL
                const currentPageUrl = window.location.href;
                const chatIdMatch = currentPageUrl.match(/\\/c\\/([^\\/]+)/);
                const chatId = chatIdMatch ? chatIdMatch[1] : null;
                
                // Store results in window for extraction
                window.chatGptResponse = {{
                    response: response,
                    chatId: chatId,
                    url: chatId ? "#" + chatId : null,
                    fullUrl: currentPageUrl,
                    sourcesClicked: true
                }};
                
                console.log("Response extracted successfully");
                console.log("Chat ID:", chatId);
                
            }} catch (error) {{
                console.error("Error during ChatGPT interaction:", error);
                window.chatGptResponse = {{
                    error: error.message,
                    response: null,
                    chatId: null,
                    url: null,
                    sourcesClicked: false
                }};
            }}
        }})();
        '''
    ]

    run_config = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        wait_for="css:.markdown.prose.w-full.break-words",
        js_code=js_code,
        screenshot=True,
        magic=True,
        scan_full_page=True,
        simulate_user=True,
        pdf=True,
        verbose=True,
        delay_before_return_html=8, 
    )

    async with AsyncWebCrawler(config=browser_config) as crawler:
        from typing import cast
        from crawl4ai.models import CrawlResultContainer

        result = cast(CrawlResultContainer, await crawler.arun(
            url="https://chatgpt.com/",
            config=run_config
        ))

        if not getattr(result, "success", False):
            print(f"Crawl failed: {getattr(result, 'error_message', 'Unknown error')}")
            return

        # Extract the response data from the page
        try:
            # Try to extract the response from the executed JavaScript
            html_content = getattr(result, "html", "")
            
            # Look for the chatGptResponse in the HTML or try to extract from markdown
            response_data = None
            chat_id = None
            
            # Try to extract chat ID from URL if available
            if hasattr(result, 'url') and result.url:
                chat_id_match = re.search(r'/c/([^/]+)', result.url)
                if chat_id_match:
                    chat_id = chat_id_match.group(1)
            
            # Save the response data
            response_info = {
                "prompt": PROMPT,
                "chat_id": chat_id,
                "url": f"#{chat_id}" if chat_id else None,
                "full_url": getattr(result, 'url', None),
                "success": True,
                "sources_clicked": True  # Indicate that we attempted to click sources
            }
            
            info_path = OUTPUT_DIR / "response_info.json"
            with open(info_path, "w", encoding="utf-8") as f:
                json.dump(response_info, f, indent=2)
            print(f"Response info saved to {info_path}")
            
        except Exception as e:
            print(f"Error extracting response data: {e}")

        # Save markdown (this will contain the ChatGPT response)
        md_path = OUTPUT_DIR / "chatgpt_response.md"
        markdown = getattr(result, "markdown", None)
        if markdown:
            fit_md = getattr(markdown, "fit_markdown", None)
            raw_md = getattr(markdown, "raw_markdown", None)
            content = fit_md or raw_md or ""
            
            # Try to extract just the response part
            if content:
                # Look for the last message output section
                lines = content.split('\n')
                response_lines = []
                in_response = False
                
                for line in lines:
                    if 'markdown prose w-full break-words' in line or in_response:
                        in_response = True
                        response_lines.append(line)
                    elif in_response and line.strip() and not line.startswith(' '):
                        break
                
                if response_lines:
                    content = '\n'.join(response_lines)
            
            with open(md_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Markdown saved to {md_path}")
        else:
            print("No markdown extracted.")

        # Save screenshot (after sources button click)
        if getattr(result, "screenshot", None):
            screenshot_path = OUTPUT_DIR / "chatgpt_response_with_sources.png"
            with open(screenshot_path, "wb") as f:
                f.write(base64.b64decode(result.screenshot))
            print(f"Screenshot saved to {screenshot_path}")
        else:
            print("No screenshot captured.")

        # Save PDF
        if getattr(result, "pdf", None):
            pdf_path = OUTPUT_DIR / "chatgpt_response.pdf"
            with open(pdf_path, "wb") as f:
                f.write(base64.b64decode(result.pdf))
            print(f"PDF saved to {pdf_path}")
        else:
            print("No PDF captured.")

        # Save raw HTML for debugging
        html_path = OUTPUT_DIR / "page_source.html"
        html_content = getattr(result, "html", "")
        if html_content:
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(html_content)
            print(f"Raw HTML saved to {html_path}")

if __name__ == "__main__":
    asyncio.run(main())
