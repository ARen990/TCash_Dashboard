from playwright.async_api import async_playwright
import asyncio

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        await page.goto("https://course.mytcas.com/", wait_until='networkidle')
        await page.wait_for_timeout(3000)

        # Fine input search be flexible
        search_input = None
        search_selectors = [
            'input[id="search"]',
            'input[placeholder*="พิมพ์ชื่อมหาวิทยาลัย"]',
            'input[placeholder*="หลักสูตร"]',
            'input[type="text"]',
            '#search'
        ]

        for selector in search_selectors:
            try:
                await page.wait_for_selector(selector, timeout=3000)
                search_input = selector
                break
            except:
                continue

        if not search_input:
            print("Search box not found")
            await page.screenshot(path="search_input_not_found.png")
            await browser.close()
            return

        print("Found search box:", search_input)
        await page.fill(search_input, "วิศวกรรมปัญญาประดิษฐ์")
        await page.wait_for_timeout(1000)

        # Enter for finding
        await page.press(search_input, "Enter")
        print("Searching ...")

        await page.wait_for_timeout(4000)


if __name__ == "__main__":
    asyncio.run(main())
