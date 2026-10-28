
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
                timeout=45000
            )

            print("Ответ получен")
            print("HTTP:", response.status if response else "нет ответа")

            try:
                page.wait_for_load_state(
                    "domcontentloaded",
                    timeout=15000
                )
            except Exception:
                print("Страница загружается медленно, продолжаем проверку")

            page.wait_for_timeout(5000)

            print("Заголовок:", page.title())
            print("Адрес:", page.url)
            print("Поля ввода:", page.locator("input").count())
            print("Кнопки:", page.locator("button").count())

        except Exception as e:
            print("ОШИБКА ЗАГРУЗКИ:", repr(e))

        finally:
            browser.close()

if __name__ == "__main__":
    main()
