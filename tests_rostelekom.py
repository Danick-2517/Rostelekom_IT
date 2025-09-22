import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


@pytest.fixture(scope="class")
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

class TestLogin:
    def open_login_page(self, driver):
        driver.get("https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth?client_id=account_b2c&redirect_uri=https://b2c.passport.rt.ru/account_b2c/login&response_type=code&scope=openid&state=aea0f3e3-d6e6-4a96-b4f4-7afe3ce19b31")


# ТЕСТ1: Проверка загрузки страницы входа
    def test_load_login_page(self, driver):
        self.open_login_page(driver)  # Открытие страницы входа
        WebDriverWait(driver, 10).until(EC.title_contains("Ростелеком ID"))
        assert "Ростелеком ID" in driver.title

# ТЕСТ2: Проверка наличия элементов на странице
    def test_elements_on_login_page(self, driver):
        self.open_login_page(driver)  # Открытие страницы входа
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "username")))
        assert driver.find_element(By.ID, "username")  # Поле для логина
        assert driver.find_element(By.ID, "password")  # Поле для пароля
        assert driver.find_element(By.XPATH, '//button[text()=" Войти "]')  # Кнопка "Войти"
        assert driver.find_element(By.LINK_TEXT, "Забыл пароль")  # Ссылка на восстановление пароля

# ТЕСТ3: Проверка, регистрации пользователя по номеру телефона
    def test_registration(self, driver):

        self.open_login_page(driver)  # Открытие страницы входа
        # Нажать кнопку "Зарегистрироваться"
        WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//a[@id='kc-register']")))
        driver.find_element(By.XPATH, "//a[@id='kc-register']").click()
        # Ввести имя и фамилию
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "firstName")))
        driver.find_element(By.NAME, "firstName").send_keys("Ивания")
        driver.find_element(By.NAME, "lastName").send_keys("Иванова")
        # Нажать на поле "Регион" и выбрать необходимый регион
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='rt-input rt-input--rounded rt-input--orange rt-input--actions']//input[@type='text']")))
        driver.find_element(By.XPATH, "//div[@class='rt-input rt-input--rounded rt-input--orange rt-input--actions']//input[@type='text']").click()
        driver.find_element(By.XPATH, "//div[@class='rt-input rt-input--rounded rt-input--orange rt-input--active rt-input--actions']//input[@type='text']").send_keys("Новосибирск")
        driver.find_element(By.XPATH, "//div[@class='rt-select__list-item']").click()
        # Ввести номер телефона
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@id='address']")))
        driver.find_element(By.XPATH, "//input[@id='address']").send_keys("89538869624")
        # Ввести корректный пароль и подтвердить его
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "password")))
        driver.find_element(By.NAME, "password").send_keys("Rzvr@85vz")
        driver.find_element(By.NAME, "password-confirm").send_keys("Rzvr@85vz")
        # Нажать кнопку "Зарегистрироваться"
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[text()=" Зарегистрироваться "]')))
        driver.find_element(By.XPATH, '//button[text()=" Зарегистрироваться "]').click()
        time.sleep(10)
        # Проверить успешную регистрацию
        time.sleep(10)
        WebDriverWait(driver, 10).until(EC.title_contains("Ростелеком ID"))
        assert "Ростелеком ID" in driver.title


# ТЕСТ4: Проверка восстановления пароля клиента по номеру телефона
    def test_password_recovery(self, driver):
        self.open_login_page(driver)  # Открытие страницы входа
        # Нажать кнопку "Забыл пароль"
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//a[text()=" Забыл пароль "]')))
        driver.find_element(By.XPATH, '//a[text()=" Забыл пароль "]').click()
        # Ввести номер телефона
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@id='username']")))
        driver.find_element(By.XPATH, "//input[@id='username']").send_keys("89538869624")
        time.sleep(15) #задержка для ввода текста с картинки (при появлении)
        # Нажать кнопку "Продолжить"
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[text()=" Продолжить "]')))
        driver.find_element(By.XPATH, '//button[text()=" Продолжить "]').click()
        # Ввести код из СМС
        time.sleep(20) #Задержка для ввода кода из СМС
        # Ввести новый пароль
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "password-new")))
        driver.find_element(By.NAME, "password-new").send_keys("Rzvr@85VZ")
        driver.find_element(By.NAME, "password-confirm").send_keys("Rzvr@85VZ")
        # Нажать кнопку "Сохранить"
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@id='t-btn-reset-pass']")))
        driver.find_element(By.XPATH, "//button[@id='t-btn-reset-pass']").click()
        # Проверить успешное изменение пароля
        WebDriverWait(driver, 10).until(EC.title_contains("Ростелеком ID"))
        assert "Ростелеком ID" in driver.title

# ТЕСТ5: Указании старого пароля при востановлении пароля
    def test_password_recovery_double(self, driver):
        self.open_login_page(driver)  # Открытие страницы входа
        # Нажать кнопку "Забыл пароль"
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//a[text()=" Забыл пароль "]')))
        driver.find_element(By.XPATH, '//a[text()=" Забыл пароль "]').click()
        # Ввести номер телефона
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@id='username']")))
        driver.find_element(By.XPATH, "//input[@id='username']").send_keys("89538869624")
        time.sleep(20)  # Задержа для ввода текста с картинки
        # Нажать кнопку "Продолжить"
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[text()=" Продолжить "]')))
        driver.find_element(By.XPATH, '//button[text()=" Продолжить "]').click()
        # Ввести код из СМС
        time.sleep(20)  # Задержка для ввода кода из СМС
        # Ввести новый пароль
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "password-new")))
        driver.find_element(By.NAME, "password-new").send_keys("Rzvr@85VZ")
        driver.find_element(By.NAME, "password-confirm").send_keys("Rzvr@85VZ")
        # Нажать кнопку "Сохранить"
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@id='t-btn-reset-pass']")))
        driver.find_element(By.XPATH, "//button[@id='t-btn-reset-pass']").click()
        # Проверить появление ошибке
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//span[@id='form-error-message']"))) #Ожидается сообщение 'Этот пароль уже использовался, укажите другой пароль'
        assert (driver.find_element(By.XPATH, "//span[@id='form-error-message']"))

# ТЕСТ6: Успешный вход в систему
    def test_successful_login(self, driver):
        self.open_login_page(driver)  # Открытие страницы входа
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))
        # Вводим логин и пароль
        driver.find_element(By.ID, "username").send_keys("89538869624")
        driver.find_element(By.NAME, "password").send_keys("Rzvr@85VZ")
        time.sleep(10)  # задержка для ввода текста с картинки (при появлении)
        # Нажимаем кнопку "Войти"
        driver.find_element(By.XPATH, '//button[text()=" Войти "]').click()
        time.sleep(5) #Задержка для загрузки страницы
        # Проверяем открытие страницы профиля
        WebDriverWait(driver, 10).until(EC.title_contains("Ростелеком ID"))
        assert "Ростелеком ID" in driver.title


# ТЕСТ7: Неправильный логин
    def test_incorrect_username(self, driver):
        self.open_login_page(driver)  # Открытие страницы входа
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))
        # Вводим неверный логин и корректный пароль
        driver.find_element(By.ID, "username").send_keys("89528847585")
        driver.find_element(By.NAME, "password").send_keys("Rzvr@85VZ")
        # Нажимаем кнопку "Войти"
        driver.find_element(By.XPATH, '//button[text()=" Войти "]').click()
        #Ожидается сообщение о неверном логине или пароле
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//span[@id='form-error-message']")))
        assert (driver.find_element(By.XPATH, "//span[@id='form-error-message']"))

# ТЕСТ8: Неправильный пароль
    def test_incorrect_password(self, driver):
        self.open_login_page(driver)  # Открытие страницы входа
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))
        # Вводим корректный логин и неверный пароль
        driver.find_element(By.ID, "username").send_keys("89538869624")
        driver.find_element(By.NAME, "password").send_keys("h94rjflk")
        # Нажимаем кнопку "Войти"
        driver.find_element(By.XPATH, '//button[text()=" Войти "]').click()
        #Ожидается сообщение о неверном логине или пароле
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//span[@id='form-error-message']")))
        assert (driver.find_element(By.XPATH, "//span[@id='form-error-message']"))


# ТЕСТ9: Пустые поля логина и пароля
    def test_empty_username_and_password(self, driver):
        self.open_login_page(driver)  # Открытие страницы входа
        # Нажимаем кнопку "Войти" без ввода логина и пароля
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[@id='kc-login']")))
        driver.find_element(By.XPATH, '//button[text()=" Войти "]').click()
        # Проверяем появление "Введите номер телефона"
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//span[@id='username-meta']")))
        assert (driver.find_element(By.XPATH, "//span[@id='username-meta']"))

# ТЕСТ10: Пустое поле логина
    def test_empty_username(self, driver):
        self.open_login_page(driver)  # Открытие страницы входа
        #Вводим корректный пароль
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "password")))
        driver.find_element(By.NAME, "password").send_keys("Rzvr@85vz")
        # Нажимаем кнопку "Войти"
        driver.find_element(By.XPATH, '//button[text()=" Войти "]').click()
        # Проверяем появление "Введите номер телефона"
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//span[@id='username-meta']")))
        assert (driver.find_element(By.XPATH, "//span[@id='username-meta']"))

# ТЕСТ11: Пустое поле пароля
    def test_empty_password(self, driver):
        self.open_login_page(driver)  # Открытие страницы входа
        #Вводим корректный логин
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username")))
        driver.find_element(By.ID, "username").send_keys("89538869624")
        # Нажимаем кнопку "Войти"
        driver.find_element(By.XPATH, '//button[text()=" Войти "]').click()
        #Ожидается сообщение о неверном логине или пароле
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//a[@id='forgot_password']")))
        assert (driver.find_element(By.XPATH, "//a[@id='forgot_password']"))

# ТЕСТ12: Вход с использованием специальных символов в логине и пароле
    def test_login_with_special_characters(self, driver):
        self.open_login_page(driver)  # Открытие страницы входа
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username")))
        #Вводим вместо логина и пароля спец символы
        driver.find_element(By.ID, "username").send_keys("#@$^+===")
        driver.find_element(By.NAME, "password").send_keys("54+-/0&^#")
        # Нажимаем кнопку "Войти"
        driver.find_element(By.XPATH, '//button[text()=" Войти "]').click()
        # Ожидается сообщение о неверном логине или пароле
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//span[@id='form-error-message']")))
        assert (driver.find_element(By.XPATH, "//span[@id='form-error-message']"))

# ТЕСТ13: Вход с длинным логином и паролем
    def test_login_with_long_username_and_password(self, driver):
        long_username = "a" * 256
        long_password = "b" * 256
        self.open_login_page(driver)  # Открытие страницы входа
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username"))) #Ожидание появления поля для ввода номера телефона
        driver.find_element(By.ID, "username").send_keys(long_username)
        driver.find_element(By.NAME, "password").send_keys(long_password)
        driver.find_element(By.XPATH, '//button[text()=" Войти "]').click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//span[@id='form-error-message']"))) #Ожидается сообщение о неверном логине или пароле

# ТЕСТ14: Доступ к личному кабинету после входа
    def test_profile_page_access_after_login(self, driver):
        self.open_login_page(driver)  # Открытие страницы входа
        self.test_successful_login(driver) #успешный вход
        # Нажимаем кнопку "Личный кабинет"
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Личный кабинет')]")))
        driver.find_element(By.XPATH, "//span[contains(text(),'Личный кабинет')]").click()
        # Проверяем открытие страницы профиля
        WebDriverWait(driver, 10).until(EC.title_contains("Главная - Единый Личный Кабинет"))
        assert ("Главная - Единый Личный Кабинет", driver.title)


# ТЕСТ15: Доступ к заявкам аккаунта после входа
    def test_account_settings_access_after_login(self, driver):
        self.open_login_page(driver)  # Открытие страницы входа
        self.test_successful_login(driver)  # успешный вход
        # Нажимаем кнопку "Личный кабинет"
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Личный кабинет')]")))
        driver.find_element(By.XPATH, "//span[contains(text(),'Личный кабинет')]").click()
        # Нажимаем кнопку "Заявки"
        WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'app-header_navigation_link') and contains(text(), 'Заявки')]")))
        driver.find_element(By.XPATH, "//a[contains(@class, 'app-header_navigation_link') and contains(text(), 'Заявки')]").click()
        # Проверяем заголовок страницы заявок
        WebDriverWait(driver, 10).until(EC.title_contains("Мои заявки - Единый Личный Кабинет"))
        assert ("Мои заявки - Единый Личный Кабинет", driver.title)

# ТЕСТ16: Превышение лимита попыток входа
    def test_login_attempts_limit_exceeded(self, driver):
        for _ in range(5):  # Входим несколько раз с неверными данными
            self.test_incorrect_password(driver)
            # Проверяем появление картинки с кодом
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//img[@class='rt-captcha__image']")))

# ТЕСТ17: Проверка, регистрации пользователя по email
    def test_registration_mail(self, driver):
        self.open_login_page(driver)  # Открытие страницы входа
        # Нажать кнопку "Зарегистрироваться"
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[@id='kc-register']")))
        driver.find_element(By.XPATH, "//a[@id='kc-register']").click()
        # Ввести имя и фамилию
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "firstName")))
        driver.find_element(By.NAME, "firstName").send_keys("Ира")
        driver.find_element(By.NAME, "lastName").send_keys("Иванова")
        # Нажать на поле "Регион" и выбрать необходимый регион
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='rt-input rt-input--rounded rt-input--orange rt-input--actions']//input[@type='text']")))
        driver.find_element(By.XPATH, "//div[@class='rt-input rt-input--rounded rt-input--orange rt-input--actions']//input[@type='text']").click()
        driver.find_element(By.XPATH, "//div[@class='rt-input rt-input--rounded rt-input--orange rt-input--active rt-input--actions']//input[@type='text']").send_keys("Новосибирск")
        driver.find_element(By.XPATH, "//div[@class='rt-select__list-item']").click()
        # Ввести номер телефона
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@id='address']")))
        driver.find_element(By.XPATH, "//input[@id='address']").send_keys("lera.shabelskaya@mail.ru")
        # Ввести корректный пароль и подтвердить его
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "password")))
        driver.find_element(By.NAME, "password").send_keys("Kthf2025")
        driver.find_element(By.NAME, "password-confirm").send_keys("Kthf2025")
        # Нажать кнопку "Зарегистрироваться"
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[text()=" Зарегистрироваться "]')))
        driver.find_element(By.XPATH, '//button[text()=" Зарегистрироваться "]').click()
        # Проверить успешную регистрацию
        WebDriverWait(driver, 10).until(EC.title_contains("Ростелеком ID"))
        assert "Ростелеком ID" in driver.title

# ТЕСТ18: Вход с использованием email
    def test_login_with_email_instead_of_username(self, driver):
        self.open_login_page(driver)  # Открытие страницы входа
        # Вводим email и пароль
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@id='username']")))
        driver.find_element(By.XPATH, "//input[@id='username']").send_keys("lera.shabelskaya@mail.ru")
        driver.find_element(By.NAME, "password").send_keys("Kthf2025")
        time.sleep(10) #задержка для ввода текста с картинки (при появлении)
        # Нажимаем кнопку войти
        driver.find_element(By.XPATH, '//button[text()=" Войти "]').click()
        # Проверить успешный вход
        WebDriverWait(driver, 10).until(EC.title_contains("Ростелеком ID"))
        assert "Ростелеком ID" in driver.title

# ТЕСТ19: Проверка функции "Запомнить меня"
    def test_remember_me_functionality(self, driver):
        self.open_login_page(driver)  # Открытие страницы входа
        self.test_successful_login(driver)  # успешный вход
        # Выходим из системы
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='logout-btn']")))
        driver.find_element(By.XPATH, "//div[@id='logout-btn']").click()
        # Снова открываем страницу входа и проверяем наличие сохраненных данных
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@id='username']")))
        username_field = driver.find_element(By.XPATH, "//input[@id='username']")
        # Проверяем заполнено ли поле логина
        saved_username = username_field.get_attribute('value')
        assert (saved_username, "89538869624")

# ТЕСТ20: Проверка ограничения на ввод лицевого счета
    def test_account_number_limit(self, driver):
        self.open_login_page(driver)  # Открытие страницы входа
        # Нажать кнопку "Лицевой счет"
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='t-btn-tab-ls']")))
        driver.find_element(By.XPATH, "//div[@id='t-btn-tab-ls']").click()
        # Ввести номер лицевого счета больше 12 цифр
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@id='username']")))
        account_number_field = driver.find_element(By.XPATH, "//input[@id='username']")
        account_number_field.send_keys("12345678901234567890")
        # Проверить, что в поле не вводится больше 12 цифр
        entered_value = account_number_field.get_attribute('value')
        assert (len(entered_value), 12)

# ТЕСТ21: Авторизация клиента с помощью лицевого счета
    def test_account_login(self, driver):
        self.open_login_page(driver)  # Открытие страницы входа
        # Нажать кнопку "Лицевой счет"
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='t-btn-tab-ls']")))
        driver.find_element(By.XPATH, "//div[@id='t-btn-tab-ls']").click()
        # Ввести номер лицевого счета и пароль
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@id='username']")))
        driver.find_element(By.XPATH, "//input[@id='username']").send_keys("123456789012")
        driver.find_element(By.NAME, "password").send_keys("Hquus8le")
        time.sleep(10)  # задержка для ввода текста с картинки (при появлении)
        # Нажать кнопку "Войти"
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[text()=" Войти "]')))
        driver.find_element(By.XPATH, '//button[text()=" Войти "]').click()
        WebDriverWait(driver, 10).until(EC.title_contains("Ростелеком ID"))
        assert "Ростелеком ID" in driver.title



# python3 -m pytest -v --driver Chrome Rostelekom_IT/tests_rostelekom.py