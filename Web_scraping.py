from playwright.async_api import async_playwright
import asyncio
import json

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        try:
            print("กำลังเข้าสู่เว็บไซต์...")
            await page.goto("https://course.mytcas.com/", wait_until='networkidle')
            await page.wait_for_timeout(3000)
            
            # ค้นหาและกรอกข้อมูล
            print("กำลังค้นหาช่องค้นหาและกรอกข้อมูล...")
            search_input = 'input[id="search"]'
            await page.wait_for_selector(search_input, timeout=10000)
            await page.fill(search_input, "วิศวกรรมคอมพิวเตอร์")
            
            # คลิกปุ่มค้นหา
            print("กำลังคลิกปุ่มค้นหา...")
            search_button = 'i.i-search'
            await page.click(search_button)
            
            # รอผลลัพธ์
            print("กำลังรอผลลัพธ์...")
            await page.wait_for_timeout(5000)
            await page.wait_for_load_state('networkidle', timeout=10000)
            
            # ถ่ายภาพหน้าจอ
            await page.screenshot(path="search_results.png", full_page=True)
            print(f"URL ปัจจุบัน: {page.url}")
            
            # หาผลลัพธ์
            result_selector = "div[class*='result']"
            await page.wait_for_selector(result_selector, timeout=10000)
            programs = await page.query_selector_all(result_selector)
            
            print(f"พบ {len(programs)} รายการ")
            
            # เก็บข้อมูล
            result = []
            for i, program in enumerate(programs):
                try:
                    # หาลิงก์
                    link_element = await program.query_selector("a[href]")
                    if not link_element:
                        continue
                        
                    href = await link_element.get_attribute("href")
                    if not href:
                        continue
                    
                    # สร้าง URL เต็ม
                    if href.startswith('/'):
                        full_link = f"https://course.mytcas.com{href}"
                    elif not href.startswith('http'):
                        full_link = f"https://course.mytcas.com/{href}"
                    else:
                        full_link = href

                    print(f"[{i+1}] เข้าถึง: {full_link}")

                    # เปิดหน้ารายละเอียด
                    detail_page = await browser.new_page()
                    try:
                        await detail_page.goto(full_link, wait_until='domcontentloaded', timeout=30000)
                        await detail_page.wait_for_timeout(2000)

                        # มหาวิทยาลัย
                        university_name = "ไม่พบข้อมูล"
                        uni_elem = await detail_page.query_selector("span.name a")
                        if uni_elem:
                            university_name = (await uni_elem.text_content()).strip()

                        # ข้อมูลทั้งหมดใน <dl> แยก <dt>/<dd>
                        data = {
                            "มหาวิทยาลัย": university_name,
                            "ชื่อหลักสูตร": "ไม่พบข้อมูล",
                            "ชื่อหลักสูตรภาษาอังกฤษ": "ไม่พบข้อมูล",
                            "ประเภทหลักสูตร": "ไม่พบข้อมูล",
                            "วิทยาเขต": "ไม่พบข้อมูล",
                            "ค่าใช้จ่าย": "ไม่พบข้อมูล",
                            "ลิงก์": full_link
                        }

                        items = await detail_page.query_selector_all("dl dt")
                        for dt in items:
                            key = (await dt.text_content()).strip()
                            dd = await dt.evaluate_handle("el => el.nextElementSibling")
                            value = await dd.text_content() if dd else ""

                            if "ชื่อหลักสูตรภาษาอังกฤษ" in key:
                                data["ชื่อหลักสูตรภาษาอังกฤษ"] = value.strip()
                            elif "ชื่อหลักสูตร" == key:
                                data["ชื่อหลักสูตร"] = value.strip()
                            elif "ประเภทหลักสูตร" in key:
                                data["ประเภทหลักสูตร"] = value.strip()
                            elif "วิทยาเขต" in key:
                                data["วิทยาเขต"] = value.strip()
                            elif "ค่าใช้จ่าย" in key:
                                data["ค่าใช้จ่าย"] = value.strip()

                        print(f"✅ {data['ชื่อหลักสูตร'][:50]}... จาก {data['มหาวิทยาลัย']}")

                        result.append(data)



                    except Exception as e:
                        print(f"เกิดข้อผิดพลาดในการเข้าถึงรายละเอียด: {e}")
                    finally:
                        await detail_page.close()

                except Exception as e:
                    print(f"เกิดข้อผิดพลาดในรายการที่ {i+1}: {e}")

        except Exception as e:
            print(f"เกิดข้อผิดพลาดหลัก: {e}")
            await page.screenshot(path="error.png", full_page=True)
        finally:
            await browser.close()

        # บันทึกผลลัพธ์
        if result:
            with open("programs.json", "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            print(f"✅ บันทึก {len(result)} รายการแล้ว")
        else:
            print("❌ ไม่มีข้อมูลให้บันทึก")

if __name__ == "__main__":
    asyncio.run(main())