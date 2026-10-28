
from playwright.sync_api import sync_playwright

URL = "https://moskva.beeline.ru/customers/products/krasivie-nomera/"

def main():
    print("Проверяем каталог Билайн")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(locale="ru-RU")

        try:
            page.goto(URL, wait_until="commit", timeout=45000)
            page.wait_for_timeout(5000)

            print("Заголовок:", page.title())
            print("Адрес:", page.url)

            fields = page.locator("input")
            print("Количество полей:", fields.count())

            for i in range(fields.count()):
                field = fields.nth(i)
                print(
                    "Поле", i,
                    "| type:", field.get_attribute("type"),
                    "| aria-label:", field.get_attribute("aria-label"),
                    "| placeholder:", field.get_attribute("placeholder")
                )

            buttons = page.locator("button")
            print("Количество кнопок:", buttons.count())

            for i in range(min(buttons.count(), 25)):
                button = buttons.nth(i)
                print(
                    "Кнопка", i,
                    "| aria-label:", button.get_attribute("aria-label"),
                    "| title:", button.get_attribute("title")
                )

        except Exception as e:
            print("Ошибка:", repr(e))

        finally:
            browser.close()

if __name__ == "__main__":
    main()
