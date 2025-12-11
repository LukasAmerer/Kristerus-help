import requests
from bs4 import BeautifulSoup

def scrape_website(url):
    """
    Fetches the content of a website and returns the title and text.
    
    Args:
        url (str): The URL of the website to scrape.
        
    Returns:
        dict: A dictionary containing:
            - title (str): The title of the webpage.
            - text (str): The cleaned text content of the page.
            - url (str): The original URL.
            - status (str): "success" or "error".
            - message (str): Error message if status is "error".
    """
    try:
        # Add a user agent to mimic a real browser request to avoid being blocked
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Send HTTP GET request with a timeout
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Check for HTTP errors (e.g., 404, 500)

        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract webpage title
        title = soup.title.string if soup.title else "No Title Found"

        # Remove script and style elements to get only visible text
        for script in soup(["script", "style"]):
            script.extract()
        
        # Get text and clean it up using a separator
        text = soup.get_text(separator='\n')
        
        # Clean up excessive whitespace and blank lines
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)

        return {
            "title": title,
            "text": text,
            "url": url,
            "status": "success"
        }

    except requests.exceptions.RequestException as e:
        # Handle network-related errors (DNS, timeout, connection refused)
        return {
            "status": "error",
            "message": str(e)
        }
    except Exception as e:
        # Handle parsing or other unexpected errors
        return {
            "status": "error",
            "message": f"An unexpected error occurred: {str(e)}"
        }

def search_and_scrape(query, max_results=100):
    """
    Searches for the query using Google Search and scrapes the top results.
    
    Args:
        query (str): The search term.
        max_results (int): Maximum number of search results to process.
        
    Returns:
        list: A list of dictionaries containing title, url, snippet, and content.
    """
    from googlesearch import search
    
    results = []
    try:
        # Perform Google search
        # Note: googlesearch library might rate limit if used too heavily
        urls = list(search(query, num_results=max_results, lang="en"))
        
        for url in urls:
            # Scrape each URL found detailed content
            scraped_data = scrape_website(url)
            
            if scraped_data['status'] == 'success':
                results.append({
                    'title': scraped_data.get('title', 'No Title'),
                    'url': url,
                    'snippet': scraped_data.get('text', '')[:200],  # Short preview
                    'content': scraped_data.get('text', '')         # Full content
                })
            else:
                # Log failed scrapes but keep the URL in results
                results.append({
                    'title': 'Failed to scrape',
                    'url': url,
                    'snippet': '',
                    'content': f"Failed to scrape: {scraped_data.get('message', 'Unknown error')}"
                })
                
        return results
    except Exception as e:
        # Return a list with a single error object if the search fails broadly
        return [{"error": str(e)}]
