"""
Test script to verify Azure Cosmos DB MongoDB connection
"""
from db_cache import cache

print("Testing Azure Cosmos DB connection...")
print()

# Test 1: Store an answer
print("Test 1: Storing a test answer...")
success = cache.store_answer(
    question="Was ist künstliche Intelligenz?",
    department="General",
    answer="KI ist die Simulation menschlicher Intelligenz durch Maschinen."
)
print(f"Store result: {'✅ Success' if success else '❌ Failed'}")
print()

# Test 2: Retrieve the answer (should be cache HIT)
print("Test 2: Retrieving cached answer...")
result = cache.get_cached_answer(
    question="Was ist künstliche Intelligenz?",
    department="General"
)
if result:
    print(f"✅ Cache HIT!")
    print(f"Answer: {result['answer'][:100]}...")
else:
    print("❌ Cache MISS (unexpected)")
print()

# Test 3: Try to get non-existent answer (should be cache MISS)
print("Test 3: Trying non-existent question...")
result = cache.get_cached_answer(
    question="This question does not exist in cache",
    department="Marketing"
)
if result:
    print("❌ Unexpected cache HIT")
else:
    print("✅ Cache MISS (expected)")

print()
print("All tests completed!")
