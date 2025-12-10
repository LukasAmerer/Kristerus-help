from db_cache import validated_results_manager

pending = validated_results_manager.get_pending_results()
approved = validated_results_manager.get_all_approved()

print(f"Pending: {len(pending)}")
print(f"Approved: {len(approved)}")

print("\nPending items:")
for r in pending[:10]:
    print(f"  - [{r.get('department')}] {r.get('query', '')[:50]}")

print("\nApproved items:")
for r in approved[:10]:
    print(f"  - [{r.get('department')}] {r.get('query', '')[:50]}")
