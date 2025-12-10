# Run search and populate database with real AI tools
from scraper import search_and_scrape
from analysis import extract_tool_names
from db_cache import validated_results_manager

# Clear everything first
from pymongo import MongoClient
import os
from dotenv import load_dotenv
load_dotenv()

connection_string = os.getenv("AZURE_COSMOS_CONNECTION_STRING")
client = MongoClient(connection_string)
db = client["kmu_meet_ki"]
collection = db["validated_results"]

# Delete all
for doc in collection.find({}):
    collection.delete_one({"_id": doc["_id"]})
print("Cleared database")

# Search queries
QUERIES = {
    "Marketing": "best AI marketing tools Jasper Copy.ai HubSpot",
    "Customer Success": "best AI customer service chatbot Intercom Zendesk Drift",
    "HR": "best AI HR recruiting tools HireVue Workday",
    "Product": "best AI product tools Notion Figma Miro",
    "General": "best AI business tools ChatGPT Claude Gemini"
}

for dept, query in QUERIES.items():
    print(f"\n=== Searching for {dept} ===")
    results = search_and_scrape(query, max_results=3)
    
    if results and "error" not in results[0]:
        # Use LLM to extract tool names
        print(f"  Found {len(results)} pages, extracting tools...")
        tools = extract_tool_names(results, dept)
        
        if tools:
            for tool in tools:
                source_url = results[0].get('url', '') if results else ''
                validated_results_manager.add_pending_result(
                    query=query,
                    department=dept,
                    llm_analysis=tool.get('description', ''),
                    apertus_validation="LLM extracted",
                    tool_name=tool.get('tool_name'),
                    source_url=source_url
                )
                print(f"    Added: {tool.get('tool_name')}")
        else:
            # Fallback - use page titles
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
        print(f"  ERROR: {results}")

print("\n=== DONE ===")

# Show what's in the database
pending = validated_results_manager.get_pending_results()
print(f"\nTotal tools in database: {len(pending)}")
for p in pending:
    print(f"  [{p.get('department')}] {p.get('tool_name')} - {p.get('source_url', '')[:40]}")
