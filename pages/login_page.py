from .base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class LoginPage(BasePage):
    # Поля ввода
    EMAIL_INPUT = (By.XPATH, "//input[@name='name']")
    PASSWORD_INPUT = (By.XPATH, "//input[@name='Пароль']")
    
    # Кнопки
    LOGIN_BUTTON = (By.XPATH, "//button[contains(text(), 'Войти')]")
    REGISTER_LINK = (By.XPATH, "//a[contains(text(), 'Зарегистрироваться')]")
    FORGOT_PASSWORD_LINK = (By.XPATH, "//a[contains(text(), 'Восстановить пароль')]")
    
    def wait_for_page_load(self):
        """Ожидание загрузки страницы авторизации"""
        self.wait.until(EC.presence_of_element_located(self.EMAIL_INPUT))
    
    def login(self, email, password):
        """Авторизация пользователя"""
        self.find_element(self.EMAIL_INPUT).send_keys(email)
        self.find_element(self.PASSWORD_INPUT).send_keys(password)
        self.click(self.LOGIN_BUTTON)
    
    def is_login_successful(self):
        """Проверка успешной авторизации"""
        try:
            # После успешного логина должны попасть на главную страницу
            from .main_page import MainPage
            main_page = MainPage(self.driver)
            main_page.wait_for_page_load()
            return True
        except:
            return False