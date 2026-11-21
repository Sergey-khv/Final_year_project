from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class AuthPage:

    def __init__(self, driver: WebDriver) -> None:
        self.__url = "https://ru.yougile.com/team/"
        self.__driver = driver
        self.__wait = WebDriverWait(driver, 10)

    def go(self):
        # Открываем страницу входа
        self.__driver.get(self.__url)

    def login_as(self, email: str, password: str):
        # 1. Ждём появления поля ввода email
        #    Используем type='email', так как ID элементов могут быть динамическими
        email_input = self.__wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='email']"))
        )
        email_input.clear()
        email_input.send_keys(email)

        # 2. Пытаемся сразу найти поле пароля
        #    Если его нет — значит, вход разбит на два шага, и нужно нажать «Далее»
        try:
            password_input = self.__wait.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='password']"))
            )
        except Exception:
            # Поле пароля не появилось сразу — нажимаем кнопку перехода к следующему шагу
            submit_btn = self.__wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH,
                     "//button[contains(@type, 'submit') or contains(text(), 'Войти') "
                     "or contains(text(), 'Далее') or contains(text(), 'Продолжить')]")
                )
            )
            submit_btn.click()
            # Теперь ждём поле пароля
            password_input = self.__wait.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='password']"))
            )

        password_input.clear()
        password_input.send_keys(password)

        # 3. Нажимаем финальную кнопку входа
        #    Кнопка — это div внутри form с классами cursor-pointer/select-none/relative,
        #    а не button[type='submit'], поэтому ищем по CSS-селектору
        login_btn = self.__wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "form div.cursor-pointer.select-none.relative")
            )
        )
        login_btn.click()

        # 4. Ждём завершения входа — проверяем, что URL изменился
        #    (можно заменить на ожидание конкретного элемента личного кабинета)
        self.__wait.until(EC.url_contains("/team/"))

    def get_current_url(self):
        # Возвращаем текущий URL драйвера
        return self.__driver.current_url
