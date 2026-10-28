
from playwright.sync_api import sync_playwright

URL = "https://moskva.beeline.ru/customers/products/krasivie-nomera/"

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(locale="ru-RU")

        try:
            page.goto(URL, wait_until="commit", timeout=45000)
            page.wait_for_timeout(15000)

            print("Заголовок:", page.title())
            print("Адрес:", page.url)

            print("Фреймы:", page.frames.__len__())
            for i, frame in enumerate(page.frames):
                print("Фрейм", i, "| адрес:", frame.url)

            print("HTML страницы:")
            print(page.content()[:6000])

        except Exception as e:
            print("Ошибка:", repr(e))

        finally:
            browser.close()

if __name__ == "__main__":
    main()
