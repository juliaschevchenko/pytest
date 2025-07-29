import sys
import os
import allure
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pages.login_page import LoginPage

@allure.title("Успешная авторизация")
def test_successful_login(page):
    login_page = LoginPage(page)
    login_page.goto()
    login_page.login('student', 'Password12')

    # Проверка: заголовок и URL
    page.wait_for_url("**/logged-in-successfully/")
    assert page.locator("h1").inner_text() == "Logged In Successfully"

@allure.title("Неуспешная авторизация")
def test_invalid_login(page):
    login_page = LoginPage(page)
    login_page.goto()
    login_page.login("invalid_user", "wrongpass")

    # Проверка сообщения об ошибке
    error_message = page.locator("div#error").inner_text()
    assert "Your username is invalid!" in error_message
