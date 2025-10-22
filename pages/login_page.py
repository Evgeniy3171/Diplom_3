# pages/login_page.py
import allure
from .base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class LoginPage(BasePage):
    # Поля ввода
    EMAIL_INPUT = (By.XPATH, "//input[@name='name']")
    PASSWORD_INPUT = (By.XPATH, "//input[@name='Пароль']")
    
    # Кнопки
    LOGIN_BUTTON = (By.XPATH, "//button[contains(text(), 'Войти')]")
    
    @allure.step("Перейти на страницу авторизации")
    def go_to_login_page(self):
        self.go_to_url(self.urls.LOGIN_PAGE)
        self.wait_for_page_load()
    
    @allure.step("Ожидать загрузки страницы авторизации")
    def wait_for_page_load(self):
        self.wait.until(EC.presence_of_element_located(self.EMAIL_INPUT))
    
    @allure.step("Ввести email: {email}")
    def enter_email(self, email):
        self.find_element(self.EMAIL_INPUT).send_keys(email)
    
    @allure.step("Ввести пароль")
    def enter_password(self, password):
        self.find_element(self.PASSWORD_INPUT).send_keys(password)
    
    @allure.step("Нажать кнопку входа")
    def click_login_button(self):
        self.click(self.LOGIN_BUTTON)
    
    @allure.step("Выполнить авторизацию")
    def login(self, email, password):
        self.enter_email(email)
        self.enter_password(password)
        self.click_login_button()