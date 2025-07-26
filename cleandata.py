# import json

# INPUT_FILE = "D:\Y3\J.bod\\all.json"        # ไฟล์ต้นฉบับ
# OUTPUT_FILE = "programs_clean.json" # ไฟล์ที่คลีนแล้ว

# # โหลดไฟล์ JSON เดิม
# with open(INPUT_FILE, "r", encoding="utf-8") as f:
#     data = json.load(f)

# cleaned = []
# seen = set()

# for item in data:
#     # ตัดช่องว่างเกินในแต่ละฟิลด์
#     for key in item:
#         if isinstance(item[key], str):
#             item[key] = item[key].strip()

#     # สร้าง unique key ป้องกันข้อมูลซ้ำ (มหาวิทยาลัย + คณะ + ชื่อหลักสูตร)
#     unique_key = (
#         item.get("มหาวิทยาลัย", ""),
#         item.get("คณะ", ""),                     # ถ้ามีฟิลด์คณะ
#         item.get("ชื่อหลักสูตร", "")
#     )

#     if unique_key not in seen:
#         seen.add(unique_key)
#         cleaned.append(item)

# # บันทึกไฟล์ใหม่
# with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
#     json.dump(cleaned, f, ensure_ascii=False, indent=2)

# print(f"✅ คลีนข้อมูลเสร็จแล้ว เหลือ {len(cleaned)} รายการ (จาก {len(data)} รายการ)")

# import json

# # โหลดไฟล์ JSON เดิม
# with open("programs.json", "r", encoding="utf-8") as f:
#     data = json.load(f)

# cleaned = []
# seen = set()

# for item in data:
#     # ตัดช่องว่างเกิน
#     for key in item:
#         if isinstance(item[key], str):
#             item[key] = item[key].strip()

#     # สร้าง unique key ป้องกันข้อมูลซ้ำ (ใช้ มหาวิทยาลัย + ชื่อหลักสูตร)
#     unique_key = (item.get("มหาวิทยาลัย"), item.get("ชื่อหลักสูตร"))
#     if unique_key not in seen:
#         seen.add(unique_key)
#         cleaned.append(item)

# # บันทึกไฟล์ใหม่
# with open("allclean.json", "w", encoding="utf-8") as f:
#     json.dump(cleaned, f, ensure_ascii=False, indent=2)

# print(f"✅ ทำความสะอาดข้อมูลแล้ว เหลือ {len(cleaned)} รายการ")

import json

INPUT_FILE = "data/data_all.json"        # ไฟล์ต้นฉบับ
OUTPUT_FILE = "data/data_clean.json" # ไฟล์ที่คลีนแล้ว
REMOVED_FILE = "data/data_removed.json" # ไฟล์ที่ถูกลบออกไป

# โหลดไฟล์ JSON เดิม
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

cleaned = []
removed = []
seen = set()

for item in data:
    # ตัดช่องว่างเกินในแต่ละฟิลด์
    for key in item:
        if isinstance(item[key], str):
            item[key] = item[key].strip()

    # ใช้ มหาวิทยาลัย + คณะ + ชื่อหลักสูตร เป็น unique key
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

# บันทึกไฟล์ข้อมูลที่เหลือ
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(cleaned, f, ensure_ascii=False, indent=2)

# บันทึกไฟล์ข้อมูลที่ถูกลบออกไป
with open(REMOVED_FILE, "w", encoding="utf-8") as f:
    json.dump(removed, f, ensure_ascii=False, indent=2)

print(f"✅ คลีนเสร็จแล้ว เหลือ {len(cleaned)} รายการ (ลบออก {len(removed)} รายการ)")
print(f"📁 ไฟล์ที่คลีนแล้ว: {OUTPUT_FILE}")
print(f"📁 ไฟล์ที่ถูกลบออกไป: {REMOVED_FILE}")


