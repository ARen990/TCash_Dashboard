from playwright.async_api import async_playwright
import asyncio
import json

SEARCH_TERMS = ["วิศวกรรม ปัญญาประดิษฐ์"]

async def scrape_programs(search_term, browser):
    page = await browser.new_page()
    await page.goto("https://course.mytcas.com/", wait_until="networkidle")
    await page.wait_for_timeout(2000)

    await page.fill('input[id="search"]', search_term)
    await page.click('i.i-search')
    await page.wait_for_timeout(3000)

    all_links = []
    page_num = 1

    while True:
        print(f"page {page_num}")
        links = await page.query_selector_all("ul.t-programs li a[href]")

        for link in links:
            href = await link.get_attribute("href")
            if href:
                full_link = href if href.startswith("http") else f"https://course.mytcas.com{href}"
                all_links.append(full_link)

        # Check the next page button
        next_button = await page.query_selector("button.next, a.next")
        if next_button:
            await next_button.click()
            await page.wait_for_timeout(2500)
            page_num += 1
        else:
            break

    print(f"✅ found {len(all_links)} order for '{search_term}'")
    await page.close()
    return all_links



async def scrape_details(links, browser):
    page = await browser.new_page()
    result = []

    for i, link in enumerate(links):
        try:
            await page.goto(link, wait_until="domcontentloaded", timeout=30000)
            await page.wait_for_timeout(1500)

            uni = await page.query_selector("span.name a")
            university = (await uni.text_content()).strip() if uni else "ไม่พบข้อมูล"

            data = {
                "มหาวิทยาลัย": university,
                "ชื่อหลักสูตร": "ไม่พบข้อมูล",
                "ชื่อหลักสูตรภาษาอังกฤษ": "ไม่พบข้อมูล",
                "ประเภทหลักสูตร": "ไม่พบข้อมูล",
                "วิทยาเขต": "ไม่พบข้อมูล",
                "ค่าใช้จ่าย": "ไม่พบข้อมูล",
                "ลิงก์": link
            }

            items = await page.query_selector_all("dl dt")
            for dt in items:
                key = (await dt.text_content()).strip()
                dd = await dt.evaluate_handle("el => el.nextElementSibling")
                value = (await dd.text_content()).strip() if dd else ""

                if key == "ชื่อหลักสูตร":
                    data["ชื่อหลักสูตร"] = value
                elif "ชื่อหลักสูตรภาษาอังกฤษ" in key:
                    data["ชื่อหลักสูตรภาษาอังกฤษ"] = value
                elif "ประเภทหลักสูตร" in key:
                    data["ประเภทหลักสูตร"] = value
                elif "วิทยาเขต" in key:
                    data["วิทยาเขต"] = value
                elif "ค่าใช้จ่าย" in key:
                    data["ค่าใช้จ่าย"] = value

            print(f"[{i+1}/{len(links)}] {data['มหาวิทยาลัย']} - {data['ชื่อหลักสูตร']}")
            result.append(data)

        except Exception as e:
            print(f"⚠️ error {i+1}: {e}")

    await page.close()
    return result


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        all_results = []

        for term in SEARCH_TERMS:
            links = await scrape_programs(term, browser)
            details = await scrape_details(links, browser)
            all_results.extend(details)

        with open("programs_wak_ai.json", "w", encoding="utf-8") as f:
            json.dump(all_results, f, ensure_ascii=False, indent=2)
        print(f"\n🎉 Data is available {len(all_results)} order")

        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
