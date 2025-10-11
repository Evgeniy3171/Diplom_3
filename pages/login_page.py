from selenium.webdriver.common.by import By
from .base_page import BasePage

class LoginPage(BasePage):
    # Локаторы для страницы логина
    EMAIL_INPUT = (By.XPATH, "//input[@name='name']")
    PASSWORD_INPUT = (By.XPATH, "//input[@name='Пароль']")
    LOGIN_BUTTON = (By.XPATH, "//button[contains(text(),'Войти')]")
    REGISTER_LINK = (By.XPATH, "//a[contains(text(),'Зарегистрироваться')]")
    FORGOT_PASSWORD_LINK = (By.XPATH, "//a[contains(text(),'Восстановить пароль')]")

    def set_email(self, email):
        self.find_element(self.EMAIL_INPUT).send_keys(email)

    def set_password(self, password):
        self.find_element(self.PASSWORD_INPUT).send_keys(password)

    def click_login_button(self):
        self.click_element(self.LOGIN_BUTTON)

    def login(self, email, password):
        self.set_email(email)
        self.set_password(password)
        self.click_login_button()