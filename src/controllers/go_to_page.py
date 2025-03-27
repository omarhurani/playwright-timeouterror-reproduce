import asyncio
from playwright.async_api import async_playwright, Error as PlaywrightError, ViewportSize
from typing import Dict, Any, Optional
import tempfile
import json


async def go_to_page(
    url: str,
    *,
    headless: bool = True,
    trace: bool = False,
    trace_path: Optional[str] = None,
    viewport: Optional[ViewportSize] = None,
    timeout: int = 10000,
    user_agent: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Visit a URL using Playwright and return the result
    
    Args:
        url: The URL to visit
        headless: Whether to run browser in headless mode
        trace: Whether to capture a trace
        trace_path: Path where to save the trace file
        
    Returns:
        Dictionary with success status and additional info
    """
    try:
        print("Starting playwright", flush=True)
        async with async_playwright() as p:
            print("Starting automation. Launching browser", flush=True)
            
            user_dir = tempfile.mkdtemp("pw-")
            with open(f"{user_dir}/Preferences", "w") as f:
                json.dump({
                    "plugins": {
                        "always_open_pdf_externally": True,
                    }
                }, f)
            browser = await p.chromium.launch(
                headless=headless,
            )
            try:
                print("Browser launched, creating context", flush=True)
                context_kwargs = dict()
                if user_agent is not None:
                    context_kwargs["user_agent"] = user_agent
                if viewport is not None:
                    context_kwargs["viewport"] = viewport
                context = await browser.new_context(**context_kwargs)
                print(f"Context created with viewport {viewport}, creating new page", flush=True)
                page = await context.new_page()
                print("Page created")
                if trace:
                    print("Starting tracing", flush=True)
                    await context.tracing.start(screenshots=True, snapshots=True, sources=True)
                try:
                    print("Navigating to page", flush=True)
                    try:
                        await asyncio.wait_for(page.goto(url, timeout=timeout, wait_until='load'), timeout=(timeout / 1000.0) + 5)
                    except asyncio.TimeoutError:
                        return {"success": False, "error": "Asyncio timeout"}
                    title = await page.title()
                    print("Page navigated")
                finally:
                    if trace:
                        print("Stopping tracing", flush=True)
                        trace_file = trace_path or 'trace.zip'
                        await context.tracing.stop(path=trace_file)
                return {"success": True, "title": title}
            
            finally:
                print("Closing browser", flush=True)
                await browser.close()
                print("Browser closed, automation finished", flush=True)
            
    except PlaywrightError as e:
        return {"success": False, "error": str(e)}
    except Exception as e:
        return {"success": False, "error": f"Unexpected error: {str(e)}"}