import json

INPUT_FILE = "data/data_all.json"        
OUTPUT_FILE = "data/data_clean.json" 
REMOVED_FILE = "data/data_removed.json" 

# Load old JSON flie
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

cleaned = []
removed = []
seen = set()

for item in data:
    # Cut excess spaces in each field
    for key in item:
        if isinstance(item[key], str):
            item[key] = item[key].strip()

    # Use university + faculty + course name as unique key.
    unique_key = (
        item.get("มหาวิทยาลัย", ""),
        item.get("คณะ", ""),                    
        item.get("ชื่อหลักสูตร", ""),
        item.get("ค่าใช้จ่าย", "")
    )

    if unique_key not in seen:
        seen.add(unique_key)
        cleaned.append(item)
    else:
        removed.append(item)

# Save the remaining data files
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(cleaned, f, ensure_ascii=False, indent=2)

# Save deleted data files
with open(REMOVED_FILE, "w", encoding="utf-8") as f:
    json.dump(removed, f, ensure_ascii=False, indent=2)

print(f"Cleaned done {len(cleaned)} order lefe (removed {len(removed)} order)")
print(f"Cleaned files: {OUTPUT_FILE}")
print(f"Removed files: {REMOVED_FILE}")


