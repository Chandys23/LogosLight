from database import get_random_verse, get_verses_by_references

# Test random verse
v = get_random_verse()
print(f"✓ Random verse: {v['reference']}")

# Test specific verses
vv = get_verses_by_references(['John 3:16', 'Psalms 23:1'])
print(f"✓ Found {len(vv)} verses:")
for verse in vv:
    print(f"  - {verse['reference']}")
