
from playwright.sync_api import sync_playwright

URL = "https://moskva.beeline.ru/customers/products/krasivie-nomera/"

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(locale="ru-RU")

        try:
            page.goto(URL, wait_until="commit", timeout=45000)
            page.wait_for_timeout(7000)

            print("=== ПОЛЯ ВВОДА ===")
            for i, field in enumerate(page.locator("input").all()):
                print(
                    i,
                    "type:", field.get_attribute("type"),
                    "aria-label:", field.get_attribute("aria-label"),
                    "placeholder:", field.get_attribute("placeholder")
                )

            print("=== КНОПКИ ===")
            for i, button in enumerate(page.locator("button").all()):
                try:
                    text = button.inner_text(timeout=2000).strip()
                    aria = button.get_attribute("aria-label")
                    print(i, "текст:", repr(text), "aria:", aria)
                except Exception:
                    pass

            print("=== ЭЛЕМЕНТЫ СЛОВАМИ ===")
            print(page.locator("body").inner_text(timeout=10000)[:3500])

        finally:
            browser.close()

if __name__ == "__main__":
    main()
