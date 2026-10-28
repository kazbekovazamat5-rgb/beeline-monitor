
from playwright.sync_api import sync_playwright

URL = "https://moskva.beeline.ru/customers/products/krasivie-nomera/"

def main():
    print("Проверяем каталог Билайн в Москве")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(locale="ru-RU")

        try:
            response = page.goto(
                URL,
                wait_until="domcontentloaded",
                timeout=120000
            )

            print("HTTP:", response.status if response else "нет ответа")
            print("Заголовок:", page.title())

            page.wait_for_timeout(5000)

            fields = page.locator("input")
            print("Количество полей ввода:", fields.count())

            for i in range(fields.count()):
                field = fields.nth(i)
                print(
                    "Поле", i,
                    "| placeholder:", field.get_attribute("placeholder"),
                    "| type:", field.get_attribute("type"),
                    "| aria-label:", field.get_attribute("aria-label")
                )

            buttons = page.locator("button")
            print("Количество кнопок:", buttons.count())

            for i in range(min(buttons.count(), 30)):
                print("Кнопка", i, ":", buttons.nth(i).inner_text())

        finally:
            browser.close()

if __name__ == "__main__":
    main()
