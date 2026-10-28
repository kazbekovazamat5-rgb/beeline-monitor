
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
            
            html = page.content()
            for word in ["api", "number", "phone", "search", "graphql", "flocktory"]:
                print(f"\n--- {word} ---")
                pos = 0
                count = 0
                while True:
                    pos = html.lower().find(word, pos)
                    if pos == -1 or count >= 3:
                        break
                    print(html[max(0, pos-150):pos+250])
                    pos += len(word)
                    count += 1


        except Exception as e:
            print("Ошибка:", repr(e))

        finally:
            browser.close()

if __name__ == "__main__":
    main()
