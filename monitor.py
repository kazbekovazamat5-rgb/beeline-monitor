
from playwright.sync_api import sync_playwright

URL = "https://moskva.beeline.ru/customers/products/krasivie-nomera/"

def main():
    print("Проверяем доступность каталога Билайн")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(locale="ru-RU")

        try:
            response = page.goto(
                URL,
                wait_until="commit",
                timeout=30000
            )
            print("Ответ получен")
            print("HTTP:", response.status if response else "нет ответа")
            print("Заголовок:", page.title())
            print("Адрес:", page.url)
            print("Текст страницы:")
            print(page.locator("body").inner_text(timeout=15000)[:3000])

        finally:
            browser.close()

if __name__ == "__main__":
    main()
