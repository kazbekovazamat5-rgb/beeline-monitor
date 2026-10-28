
import re
from playwright.sync_api import sync_playwright

URL = "https://moskva.beeline.ru/customers/products/krasivie-nomera/"
ENDING = "0000"


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(
            locale="ru-RU",
            viewport={"width": 390, "height": 844},
        )

        try:
            print("Открываем каталог Билайн Москва")
            page.goto(URL, wait_until="domcontentloaded", timeout=90000)
            page.wait_for_timeout(7000)

            print("Заголовок:", page.title())
            print("Адрес:", page.url)

            # Ищем поле ввода цифр
            inputs = page.locator("input")
            print("Полей ввода:", inputs.count())

            field = None
            for i in range(inputs.count()):
                item = inputs.nth(i)
                try:
                    if item.is_visible() and item.is_enabled():
                        field = item
                        print("Выбрано поле ввода:", i)
                        break
                except Exception:
                    pass

            if field is None:
                print("ОШИБКА: видимое поле ввода не найдено.")
                page.screenshot(path="beeline_debug.png", full_page=True)
                return

            # Вводим окончание номера
            field.fill(ENDING)
            print("Введено окончание:", ENDING)

            # Пытаемся включить поиск по окончанию:
            # на сайте замок может быть кнопкой или переключателем.
            controls = page.locator(
                'button, [role="button"], input[type="checkbox"]'
            )
            print("Кнопок и переключателей:", controls.count())

            for i in range(controls.count()):
                control = controls.nth(i)
                try:
                    if not control.is_visible():
                        continue
                    label = (
                        (control.inner_text() or "")
                        + " "
                        + (control.get_attribute("aria-label") or "")
                        + " "
                        + (control.get_attribute("title") or "")
                    ).lower()
                    if "замок" in label or "lock" in label:
                        control.click()
                        print("Нажат элемент замка:", i)
                        break
                except Exception:
                    pass

            # Ищем кнопку поиска по тексту
            search_button = page.get_by_role(
                "button", name=re.compile("найти красоту", re.I)
            ).first

            if search_button.count() == 0:
                search_button = page.get_by_text(
                    re.compile("найти красоту", re.I)
                ).first

            if search_button.count() > 0:
                search_button.click(timeout=10000)
                print("Нажата кнопка поиска")
            else:
                print("ОШИБКА: кнопка «Найти красоту» не найдена.")
                page.screenshot(path="beeline_debug.png", full_page=True)
                return

            page.wait_for_timeout(8000)

            text = page.locator("body").inner_text()
            print("Текст результатов:")
            print(text[:12000])

            # Ищем российские мобильные номера в тексте результатов
            numbers = set(
                re.findall(
                    r'(?<!\d)(?:\+7|8)?[\s(.-]*'
                    r'\d{3}[\s).-]*\d{3}[\s.-]*\d{2}[\s.-]*\d{2}'
                    r'(?!\d)',
                    text,
                )
            )

            matches = sorted(
                n for n in numbers
                if re.sub(r"\D", "", n).endswith(ENDING)
            )

            print("Номера с окончанием", ENDING, ":")
            if matches:
                for number in matches:
                    print("NUMBER:", number)
            else:
                print("Совпадений в видимом тексте не найдено.")

            page.screenshot(path="beeline_debug.png", full_page=True)

        except Exception as e:
            print("ОШИБКА:", repr(e))
            try:
                page.screenshot(path="beeline_debug.png", full_page=True)
            except Exception:
                pass
            raise
        finally:
            browser.close()


if __name__ == "__main__":
    main()
