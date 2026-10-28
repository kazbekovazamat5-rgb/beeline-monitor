
import re
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
            page.wait_for_timeout(10000)

            print("Статус HTTP:", response.status if response else "нет ответа")
            print("Заголовок:", page.title())
            print("Адрес:", page.url)

            text = page.locator("body").inner_text()
            print("Текст страницы (первые 5000 символов):")
            print(text[:5000])

            print("Проверка окончания 0000:")
            matches = re.findall(r"\+7[\d\s()\-]{8,}", text)
            for number in matches:
                print(number)

        except Exception as e:
            print("Ошибка при загрузке страницы:", repr(e))
            raise
        finally:
            browser.close()

if __name__ == "__main__":
    main()
