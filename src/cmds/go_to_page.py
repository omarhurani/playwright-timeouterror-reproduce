import arguably
from ..controllers.go_to_page import go_to_page as go_to_page_controller

@arguably.command
async def go_to_page(
    url: str,
    *,
    no_headless: bool = False,
):
    '''
    Go to a page and save a trace of the page load.
    
    Args:
        url: The URL of the page to navigate to.
        no_headless: Whether to run the browser in headless mode.
        
    Returns:
        None
    '''
    result = await go_to_page_controller(
        url, 
        headless=not no_headless,
        trace=True,  # Always capture trace for command-line usage
        trace_path='trace.zip'
    )
    
    if result["success"]:
        print(f"Successfully visited {url}")
        print(f"Title: {result['title']}")
        print("Trace saved to trace.zip")
    else:
        print(f"Error visiting {url}: {result['error']}")
