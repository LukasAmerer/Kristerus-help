import requests
from bs4 import BeautifulSoup

def scrape_website(url):
    """
    Fetches the content of a website and returns the title and text.
    """
    try:
        # Add a user agent to mimic a browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise an error for bad status codes

        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract title
        title = soup.title.string if soup.title else "No Title Found"

        # Extract text (remove scripts and styles)
        for script in soup(["script", "style"]):
            script.extract()
        
        text = soup.get_text(separator='\n')
        
        # Clean up whitespace
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
        return {
            "status": "error",
            "message": str(e)
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"An unexpected error occurred: {str(e)}"
        }

def search_and_scrape(query, max_results=100):
    """
    Searches for the query using DuckDuckGo and scrapes the top results.
    """
    from duckduckgo_search import DDGS
    
    results = []
    try:
        with DDGS() as ddgs:
            search_results = list(ddgs.text(query, max_results=max_results, backend="html"))
            
        for res in search_results:
            url = res['href']
            scraped_data = scrape_website(url)
            if scraped_data['status'] == 'success':
                results.append({
                    'title': res['title'],
                    'url': url,
                    'snippet': res['body'],
                    'content': scraped_data['text']
                })
            else:
                results.append({
                    'title': res['title'],
                    'url': url,
                    'snippet': res['body'],
                    'content': f"Failed to scrape: {scraped_data.get('message', 'Unknown error')}"
                })
                
        return results
    except Exception as e:
        return [{"error": str(e)}]
