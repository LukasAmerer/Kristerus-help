"""
Test script to verify Azure Cosmos DB (MongoDB API) connection and caching functionality.
This script performs a series of basic CRUD operations to ensure the database layer is working correctly.
"""
from db_cache import cache

print("Testing Azure Cosmos DB connection...")
print()

# --- Test Case 1: Store Data ---
# Attempt to store a sample question-answer pair in the database.
# This validates the write connection and schema validation (if any).
print("Test 1: Storing a test answer...")
success = cache.store_answer(
    question="Was ist künstliche Intelligenz?",
    department="General",
    answer="KI ist die Simulation menschlicher Intelligenz durch Maschinen."
)
print(f"Store result: {'✅ Success' if success else '❌ Failed'}")
print()

# --- Test Case 2: Retrieve Data (Cache HIT) ---
# Attempt to retrieve the exact same question just stored.
# This validates read connection and data persistence.
# Logic: If the data exists, it's a "Cache HIT".
print("Test 2: Retrieving cached answer...")
result = cache.get_cached_answer(
    question="Was ist künstliche Intelligenz?",
    department="General"
)
if result:
    print(f"✅ Cache HIT! (Data found as expected)")
    print(f"Answer: {result['answer'][:100]}...")
else:
    print("❌ Cache MISS (Unexpected - data should have been there)")
print()

# --- Test Case 3: Retrieve Non-Existent Data (Cache MISS) ---
# Attempt to retrieve a question that does not exist.
# This validates that the system correctly returns None for missing data, rather than crashing.
# Logic: If no data is found, it's a "Cache MISS", which is the expected outcome here.
print("Test 3: Trying non-existent question...")
result = cache.get_cached_answer(
    question="This question does not exist in cache",
    department="Marketing"
)
if result:
    print("❌ Unexpected cache HIT (Found data for a query that shouldn't exist)")
else:
    print("✅ Cache MISS (Expected outcome)")

print()
print("All tests completed!")
