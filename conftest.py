import allure
import pytest
import requests
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
import data
import helpers
from locators.base_page_locators import BasePageLocators
from locators.account_page_locators import AccountPageLocators


@allure.step("Запустить браузер. Перейти на главную страницу Stellar Burgers."
                    " Вернуть тип браузера. Закрыть браузер по завершении теста")
@pytest.fixture(params=['firefox', 'chrome'], scope='function')
def driver(request):
    browser = None

    if request.param == 'firefox':
        browser = webdriver.Firefox()
    elif request.param == 'chrome':
        browser = webdriver.Chrome()

    browser.get(data.Urls.MAIN_PAGE)

    yield browser

    browser.quit()


@allure.step("Запустить браузер. Перейти на главную страницу Stellar Burgers."
                    "Создать рандомного пользователя. Авторизоваться с рандомными учетными данными."
                    "Дождаться перехода на главную страницу."
                    " Вернуть тип браузера. Закрыть браузер и удалить рандомного пользователя по завершении теста")
@pytest.fixture(params=['firefox', 'chrome'], scope='function')
def driver_account(request):
    browser = None

    if request.param == 'firefox':
        browser = webdriver.Firefox()
    elif request.param == 'chrome':
        browser = webdriver.Chrome()

    browser.get(data.Urls.MAIN_PAGE)
    WebDriverWait(browser, 5).until(expected_conditions.visibility_of_element_located(BasePageLocators.account_button))
    browser.execute_script("arguments[0].click();", browser.find_element(*BasePageLocators.account_button))
    WebDriverWait(browser, 5).until(expected_conditions.visibility_of_element_located(AccountPageLocators.login_field))
    new_user = helpers.ApiNewUser.random_user_credentials()
    browser.find_element(*AccountPageLocators.login_field).send_keys(new_user['email'])
    browser.find_element(*AccountPageLocators.password_field).send_keys(new_user['password'])
    browser.execute_script("arguments[0].click();", browser.find_element(*AccountPageLocators.login_button))
    WebDriverWait(browser, 5).until(expected_conditions.url_to_be(data.Urls.MAIN_PAGE))

    yield browser


    headers = dict(Authorization=new_user['token'])
    status = 0
    while status != 202:
        response = requests.delete(data.Urls.USER_AUTHORIZATION_PAGE, headers=headers)
        status = response.status_code

    browser.quit()
