# Run search and populate database with real AI tools
# This script orchestrates the process of finding new AI tools and saving them to the database.

from scraper import search_and_scrape
from analysis import extract_tool_names
from db_cache import validated_results_manager

# Import database connection libraries and environment/config
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Database Setup ---
# Connect to Azure Cosmos DB (MongoDB API)
connection_string = os.getenv("AZURE_COSMOS_CONNECTION_STRING")
client = MongoClient(connection_string)
db = client["kmu_meet_ki"]
collection = db["validated_results"]

# --- Clear Existing Data ---
# WARNING: This deletes *all* existing entries in the 'validated_results' collection.
# This essentially resets the "Research Assistant" database.
for doc in collection.find({}):
    collection.delete_one({"_id": doc["_id"]})
print("Cleared database")

# --- Define Search Queries ---
# A dictionary mapping departments to specific search queries.
# These queries target lists of "best UI tools" for each sector.
QUERIES = {
    "Marketing": "best AI marketing tools Jasper Copy.ai HubSpot",
    "Customer Success": "best AI customer service chatbot Intercom Zendesk Drift",
    "HR": "best AI HR recruiting tools HireVue Workday",
    "Product": "best AI product tools Notion Figma Miro",
    "General": "best AI business tools ChatGPT Claude Gemini"
}

# --- Execution Loop ---
# Iterate over each department and its query
for dept, query in QUERIES.items():
    print(f"\n=== Searching for {dept} ===")
    
    # helper: Perform Google search and scrape the top 3 result pages
    results = search_and_scrape(query, max_results=3)
    
    # Check if we got valid results and no search errors
    if results and "error" not in results[0]:
        print(f"  Found {len(results)} pages, extracting tools...")
        
        # Use LLM (Language Model) to parse the text and identify specific tool names
        tools = extract_tool_names(results, dept)
        
        if tools:
            # If the LLM successfully extracted tools, add them to the database
            for tool in tools:
                # Use the URL of the first search result as the source citation
                source_url = results[0].get('url', '') if results else ''
                
                # Store the result using the manager (handles DB insertion)
                validated_results_manager.add_pending_result(
                    query=query,
                    department=dept,
                    llm_analysis=tool.get('description', ''),
                    apertus_validation="LLM extracted",  # Mark origin
                    tool_name=tool.get('tool_name'),
                    source_url=source_url
                )
                print(f"    Added: {tool.get('tool_name')}")
        else:
            # Fallback: If LLM extraction fails, just store the raw page titles
            for r in results[:3]:
                validated_results_manager.add_pending_result(
                    query=query,
                    department=dept,
                    llm_analysis=r.get('snippet', ''),
                    apertus_validation="Direct scrape",
                    tool_name=r.get('title', 'Unknown')[:50],
                    source_url=r.get('url', '')
                )
                print(f"    Added (fallback): {r.get('title', '')[:40]}")
    else:
        # Print error details if search/scrape failed
        print(f"  ERROR: {results}")

print("\n=== DONE ===")

# --- Verification ---
# Print out pending items currently in the database to verify success
pending = validated_results_manager.get_pending_results()
print(f"\nTotal tools in database: {len(pending)}")
for p in pending:
    print(f"  [{p.get('department')}] {p.get('tool_name')} - {p.get('source_url', '')[:40]}")
