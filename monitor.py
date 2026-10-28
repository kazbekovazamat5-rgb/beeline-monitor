
import re
from playwright.sync_api import sync_playwright

URL = "https://moskva.beeline.ru/customers/products/krasivie-nomera/"

def main():
    print("Проверяем каталог Билайн в Москве...")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(locale="ru-RU")

        try:
            page.goto(URL, wait_until="commit", timeout=120000)
page.wait_for_timeout(10000)

            print("Заголовок страницы:", page.title())
            print("Адрес страницы:", page.url)

            fields = page.locator("input").all()
            print("Полей ввода найдено:", len(fields))

            for i, field in enumerate(fields):
                try:
                    print(
                        f"Поле {i}:",
                        "placeholder =", field.get_attribute("placeholder"),
                        "type =", field.get_attribute("type")
                    )
                except Exception:
                    pass

            print("Фрагмент текста страницы:")
            print(page.locator("body").inner_text()[:5000])

        finally:
            browser.close()

if __name__ == "__main__":
    main()
