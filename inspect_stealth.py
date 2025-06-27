import playwright_stealth

print("--- dir(playwright_stealth) ---")
print(dir(playwright_stealth))
print("\n--- help(playwright_stealth) ---")
try:
    help(playwright_stealth)
except Exception as e:
    print(f"Error calling help(): {e}")

# Try accessing common function names if they exist
if hasattr(playwright_stealth, 'stealth_sync'):
    print("\n--- help(playwright_stealth.stealth_sync) ---")
    try:
        help(playwright_stealth.stealth_sync)
    except Exception as e:
        print(f"Error calling help() on stealth_sync: {e}")
else:
    print("\n'stealth_sync' not found in playwright_stealth.")

if hasattr(playwright_stealth, 'sync_stealth'): # another common naming
    print("\n--- help(playwright_stealth.sync_stealth) ---")
    try:
        help(playwright_stealth.sync_stealth)
    except Exception as e:
        print(f"Error calling help() on sync_stealth: {e}")
else:
    print("\n'sync_stealth' not found in playwright_stealth.")

if hasattr(playwright_stealth, 'stealth'): # generic name
    print("\n--- help(playwright_stealth.stealth) ---")
    try:
        help(playwright_stealth.stealth)
    except Exception as e:
        print(f"Error calling help() on stealth: {e}")
else:
    print("\n'stealth' not found in playwright_stealth.")
