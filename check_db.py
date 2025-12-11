"""
Diagnostic script to verify the current state of the database.
Prints the count and a sample of 'pending' vs 'approved' items.
Useful for administrators to quickly check data health.
"""
from db_cache import validated_results_manager

# Fetch lists of all pending and approved items
pending = validated_results_manager.get_pending_results()
approved = validated_results_manager.get_all_approved()

# Print summary statistics
print(f"Pending: {len(pending)}")
print(f"Approved: {len(approved)}")

# Detailed list of Pending items (limit 10)
print("\nPending items:")
for r in pending[:10]:
    print(f"  - [{r.get('department')}] {r.get('query', '')[:50]}")

# Detailed list of Approved items (limit 10)
print("\nApproved items:")
for r in approved[:10]:
    print(f"  - [{r.get('department')}] {r.get('query', '')[:50]}")
