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
            

        except Exception as e:
            print(f"เกิดข้อผิดพลาดหลัก: {e}")
            await page.screenshot(path="error.png", full_page=True)
        finally:
            await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
