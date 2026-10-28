
from playwright.sync_api import sync_playwright

URL = "https://moskva.beeline.ru/customers/products/krasivie-nomera/"

def main():
    print("Проверяем элементы поиска Билайна")

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
            page.wait_for_timeout(5000)

            print("\n--- ПОЛЯ ВВОДА ---")
            fields = page.locator("input").all()

            for i, field in enumerate(fields):
                print(
                    f"Поле {i}:",
                    "type =", field.get_attribute("type"),
                    "| aria-label =", field.get_attribute("aria-label"),
                    "| placeholder =", field.get_attribute("placeholder"),
                    "| role =", field.get_attribute("role")
                )

            print("\n--- КНОПКИ ---")
            buttons = page.locator("button").all()

            for i, button in enumerate(buttons):
                try:
                    print(
                        f"Кнопка {i}:",
                        "текст =", repr(button.inner_text(timeout=1500)),
                        "| aria-label =", button.get_attribute("aria-label"),
                        "| title =", button.get_attribute("title"),
                        "| HTML =", (button.get_attribute("outerHTML") or "")[:300]
                    )
                except Exception as e:
                    print(f"Кнопка {i}: ошибка чтения: {e}")

        finally:
            browser.close()

if __name__ == "__main__":
    main()
