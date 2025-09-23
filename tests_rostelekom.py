import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


@pytest.fixture(scope="session")
def driver():
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)
    yield driver
    driver.quit()


def open_login_page(driver):
    driver.get("https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth?"
               "client_id=account_b2c&redirect_uri=https://b2c.passport.rt.ru/account_b2c/login"
               "&response_type=code&scope=openid")


def login(driver, username, password):
    open_login_page(driver)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username")))
    driver.find_element(By.ID, "username").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password)
    time.sleep(5)  # пауза для капчи (если появится)
    driver.find_element(By.ID, "kc-login").click()

#----------------------------------------------------------------------------------------------------------------------#
# ТЕСТ1: Загрузка страницы входа
def test_load_login_page(driver):
    open_login_page(driver)
    WebDriverWait(driver, 10).until(EC.title_contains("Ростелеком ID"))
    assert "Ростелеком ID" in driver.title

#----------------------------------------------------------------------------------------------------------------------#
# ТЕСТ2: Наличие элементов на странице
def test_elements_on_login_page(driver):
    open_login_page(driver)
    assert driver.find_element(By.ID, "username")
    assert driver.find_element(By.ID, "password")
    assert driver.find_element(By.ID, "kc-login")
    assert driver.find_element(By.LINK_TEXT, "Забыл пароль")

#----------------------------------------------------------------------------------------------------------------------#
# ТЕСТ3: Регистрация пользователя по номеру телефона
def test_registration_phone(driver):
    open_login_page(driver)
    driver.find_element(By.ID, "kc-register").click()
    driver.find_element(By.NAME, "firstName").send_keys("Иван")
    driver.find_element(By.NAME, "lastName").send_keys("Иванов")
    region = driver.find_element(By.XPATH, "//input[@type='text' and @autocomplete='new-password']")
    region.send_keys("Новосибирск")
    driver.find_element(By.CLASS_NAME, "rt-select__list-item").click()
    driver.find_element(By.ID, "address").send_keys("89952453497")
    driver.find_element(By.NAME, "password").send_keys("51151013Dd")
    driver.find_element(By.NAME, "password-confirm").send_keys("51151013Dd")
    driver.find_element(By.XPATH, '//button[text()=" Зарегистрироваться "]').click()
    WebDriverWait(driver, 10).until(EC.title_contains("Ростелеком ID"))
    assert "Ростелеком ID" in driver.title

#----------------------------------------------------------------------------------------------------------------------#
# ТЕСТ4: Восстановление пароля по телефону
def test_password_recovery(driver):
    open_login_page(driver)
    driver.find_element(By.LINK_TEXT, "Забыл пароль").click()
    driver.find_element(By.ID, "username").send_keys("89952453497")
    time.sleep(15)  # ввод капчи руками
    driver.find_element(By.XPATH, '//button[text()=" Продолжить "]').click()
    time.sleep(20)  # код из СМС руками
    driver.find_element(By.NAME, "password-new").send_keys("51151013Dd")
    driver.find_element(By.NAME, "password-confirm").send_keys("51151013Dd")
    driver.find_element(By.ID, "t-btn-reset-pass").click()
    WebDriverWait(driver, 10).until(EC.title_contains("Ростелеком ID"))
    assert "Ростелеком ID" in driver.title

#----------------------------------------------------------------------------------------------------------------------#
# ТЕСТ5: Попытка восстановления со старым паролем
def test_password_recovery_old_password(driver):
    open_login_page(driver)
    driver.find_element(By.LINK_TEXT, "Забыл пароль").click()
    driver.find_element(By.ID, "username").send_keys("89952453497")
    time.sleep(20)
    driver.find_element(By.XPATH, '//button[text()=" Продолжить "]').click()
    time.sleep(20)
    driver.find_element(By.NAME, "password-new").send_keys("51151013Dd")
    driver.find_element(By.NAME, "password-confirm").send_keys("51151013Dd")
    driver.find_element(By.ID, "t-btn-reset-pass").click()
    error_msg = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "form-error-message"))
    )
    assert error_msg.is_displayed()

#----------------------------------------------------------------------------------------------------------------------#
# ТЕСТ6: Успешный вход по телефону
def test_successful_login_phone(driver):
    login(driver, "89952453497", "51151013Dd")
    WebDriverWait(driver, 10).until(EC.title_contains("Ростелеком ID"))
    assert "Ростелеком ID" in driver.title

#----------------------------------------------------------------------------------------------------------------------#
# ТЕСТ7: Ошибка — неверный логин
def test_incorrect_username(driver):
    login(driver, "89911111111", "51151013Dd")
    error_msg = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "form-error-message"))
    )
    assert error_msg.is_displayed()

#----------------------------------------------------------------------------------------------------------------------#
# ТЕСТ8: Ошибка — неверный пароль
def test_incorrect_password(driver):
    login(driver, "89952453497", "wrongpass")
    error_msg = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "form-error-message"))
    )
    assert error_msg.is_displayed()

#----------------------------------------------------------------------------------------------------------------------#
# ТЕСТ9: Пустые поля логина и пароля
def test_empty_username_and_password(driver):
    open_login_page(driver)
    driver.find_element(By.ID, "kc-login").click()
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "username-meta")))

#----------------------------------------------------------------------------------------------------------------------#
# ТЕСТ10: Пустое поле логина
def test_empty_username(driver):
    open_login_page(driver)
    driver.find_element(By.NAME, "password").send_keys("51151013Dd")
    driver.find_element(By.ID, "kc-login").click()
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "username-meta")))

#----------------------------------------------------------------------------------------------------------------------#
# ТЕСТ11: Пустое поле пароля
def test_empty_password(driver):
    open_login_page(driver)
    driver.find_element(By.ID, "username").send_keys("89952453497")
    driver.find_element(By.ID, "kc-login").click()
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "forgot_password")))

#----------------------------------------------------------------------------------------------------------------------#
# ТЕСТ12: Вход со спецсимволами
def test_login_with_special_characters(driver):
    login(driver, "#@$^+===", "54+-/0&^#")
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "form-error-message")))

#----------------------------------------------------------------------------------------------------------------------#
# ТЕСТ13: Вход с длинным логином и паролем
def test_login_with_long_credentials(driver):
    login(driver, "a" * 256, "b" * 256)
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "form-error-message")))

#----------------------------------------------------------------------------------------------------------------------#
# ТЕСТ14: Доступ к личному кабинету после входа
def test_profile_page_access_after_login(driver):
    login(driver, "89952453497", "51151013Dd")
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Личный кабинет')]"))
    ).click()
    WebDriverWait(driver, 10).until(EC.title_contains("Главная - Единый Личный Кабинет"))

#----------------------------------------------------------------------------------------------------------------------#
# ТЕСТ15: Доступ к заявкам аккаунта
def test_account_settings_access_after_login(driver):
    login(driver, "89952453497", "51151013Dd")
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Личный кабинет')]"))
    ).click()
    WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Заявки')]"))
    ).click()
    WebDriverWait(driver, 10).until(EC.title_contains("Мои заявки - Единый Личный Кабинет"))

#----------------------------------------------------------------------------------------------------------------------#
# ТЕСТ16: Превышение лимита попыток входа (капча)
def test_login_attempts_limit_exceeded(driver):
    for _ in range(5):
        login(driver, "89952453497", "wrongpass")
        open_login_page(driver)
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "rt-captcha__image"))
    )

#----------------------------------------------------------------------------------------------------------------------#
# ТЕСТ17: Регистрация по email
def test_registration_email(driver):
    open_login_page(driver)
    driver.find_element(By.ID, "kc-register").click()
    driver.find_element(By.NAME, "firstName").send_keys("Ира")
    driver.find_element(By.NAME, "lastName").send_keys("Иванова")
    region = driver.find_element(By.XPATH, "//input[@type='text' and @autocomplete='new-password']")
    region.send_keys("Новосибирск")
    driver.find_element(By.CLASS_NAME, "rt-select__list-item").click()
    driver.find_element(By.ID, "address").send_keys("kireevd14@gmail.com")
    driver.find_element(By.NAME, "password").send_keys("51151013Dd")
    driver.find_element(By.NAME, "password-confirm").send_keys("51151013Dd")
    driver.find_element(By.XPATH, '//button[text()=" Зарегистрироваться "]').click()
    WebDriverWait(driver, 10).until(EC.title_contains("Ростелеком ID"))

#----------------------------------------------------------------------------------------------------------------------#
# ТЕСТ18: Успешный вход по email
def test_login_with_email(driver):
    login(driver, "kireevd14@gmail.com", "51151013Dd")
    WebDriverWait(driver, 10).until(EC.title_contains("Ростелеком ID"))

#----------------------------------------------------------------------------------------------------------------------#
# ТЕСТ19: Проверка функции "Запомнить меня"
def test_remember_me_functionality(driver):
    login(driver, "89952453497", "51151013Dd")
    driver.find_element(By.ID, "logout-btn").click()
    open_login_page(driver)
    saved_username = driver.find_element(By.ID, "username").get_attribute("value")
    assert saved_username == "89952453497"

#----------------------------------------------------------------------------------------------------------------------#
# ТЕСТ20: Ограничение на лицевой счёт
def test_account_number_limit(driver):
    open_login_page(driver)
    driver.find_element(By.ID, "t-btn-tab-ls").click()
    account_number_field = driver.find_element(By.ID, "username")
    account_number_field.send_keys("12345678901234567890")
    entered_value = account_number_field.get_attribute("value")
    assert len(entered_value) == 12

#----------------------------------------------------------------------------------------------------------------------#
# ТЕСТ21: Авторизация по лицевому счёту
def test_account_login(driver):
    open_login_page(driver)
    driver.find_element(By.ID, "t-btn-tab-ls").click()
    driver.find_element(By.ID, "username").send_keys("123456789012")
    driver.find_element(By.NAME, "password").send_keys("51151013Dd")
    time.sleep(5)
    driver.find_element(By.ID, "kc-login").click()
    WebDriverWait(driver, 10).until(EC.title_contains("Ростелеком ID"))



# python3 -m pytest -v --driver Chrome Rostelekom_IT/tests_rostelekom.py
