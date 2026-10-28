
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

            response = page.goto(
                URL,
                wait_until="commit",
                timeout=60000,
            )

            print(
                "HTTP:",
                response.status if response else "нет ответа",
            )

            page.wait_for_timeout(10000)

            print("Заголовок:", page.title())
            print("Адрес:", page.url)

            # Проверяем, загрузилось ли приложение каталога
            inputs = page.locator("input")
            buttons = page.locator(
                'button, [role="button"], input[type="checkbox"]'
            )

            print("Полей ввода:", inputs.count())
            print("Кнопок и переключателей:", buttons.count())

            field = None

            for i in range(inputs.count()):
                item = inputs.nth(i)

                try:
                    if item.is_visible() and item.is_enabled():
                        field = item
                        print("Поле ввода найдено:", i)
                        break
                except Exception:
                    continue

            if field is None:
                print("ПОЛЕ НЕ НАЙДЕНО")
                print("Сохраняем диагностический снимок")
                page.screenshot(
                    path="beeline_debug.png",
                    full_page=True,
                )
                print("Текст страницы:")
                print(page.locator("body").inner_text()[:5000])
                return

            field.fill(ENDING)
            print("Введено окончание:", ENDING)

            print("Пытаемся найти кнопку замка")

            lock_found = False

            for i in range(buttons.count()):
                item = buttons.nth(i)

                try:
                    if not item.is_visible():
                        continue

                    description = " ".join([
                        item.inner_text() or "",
                        item.get_attribute("aria-label") or "",
                        item.get_attribute("title") or "",
                    ]).lower()

                    if any(
                        word in description
                        for word in ["замок", "lock", "окончание"]
                    ):
                        item.click(timeout=3000)
                        print("Нажат элемент замка:", i)
                        lock_found = True
                        break

                except Exception:
                    continue

            if not lock_found:
                print(
                    "Кнопка замка автоматически не определена. "
                    "Нужна дополнительная диагностика."
                )

            search_button = page.get_by_role(
                "button",
                name=re.compile("найти красоту", re.I),
            ).first

            if search_button.count() == 0:
                search_button = page.get_by_text(
                    re.compile("найти красоту", re.I)
                ).first

            if search_button.count() == 0:
                print("КНОПКА ПОИСКА НЕ НАЙДЕНА")
                page.screenshot(
                    path="beeline_debug.png",
                    full_page=True,
                )
                return

            search_button.click(timeout=10000)
            print("Нажата кнопка поиска")

            page.wait_for_timeout(8000)

            text = page.locator("body").inner_text()

            print("ТЕКСТ СТРАНИЦЫ:")
            print(text[:10000])

            # Оставляем только совпадения по окончанию 0000
            candidates = re.findall(
                r"(?<!\d)(?:\+7|8)?[\s().-]*"
                r"\d{3}[\s().-]*\d{3}[\s.-]*\d{2}[\s.-]*\d{2}"
                r"(?!\d)",
                text,
            )

            matches = set()

            for candidate in candidates:
                digits = re.sub(r"\D", "", candidate)

                if len(digits) == 11 and digits.startswith("7"):
                    national = digits[1:]
                elif len(digits) == 11 and digits.startswith("8"):
                    national = digits[1:]
                elif len(digits) == 10:
                    national = digits
                else:
                    continue

                if national.endswith(ENDING):
                    matches.add("+7 " + national)

            print("СОВПАДЕНИЯ ПО ОКОНЧАНИЮ", ENDING)

            if matches:
                for number in sorted(matches):
                    print("NUMBER:", number)
            else:
                print(
                    "Совпадений не обнаружено. "
                    "Это не подтверждает, что таких номеров нет."
                )

            page.screenshot(
                path="beeline_debug.png",
                full_page=True,
            )

        except Exception as error:
            print("ОШИБКА:", repr(error))

            try:
                page.screenshot(
                    path="beeline_debug.png",
                    full_page=True,
                )
            except Exception:
                pass

            raise

        finally:
            browser.close()


if __name__ == "__main__":
    main()
