from .base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class PersonalAccountPage(BasePage):
    # Элементы личного кабинета
    PROFILE_LINK = (By.XPATH, "//a[contains(text(), 'Профиль')]")
    ORDER_HISTORY_LINK = (By.XPATH, "//a[contains(text(), 'История заказов')]")
    LOGOUT_BUTTON = (By.XPATH, "//button[contains(text(), 'Выход')]")
    
    # Поля профиля
    NAME_INPUT = (By.XPATH, "//input[@name='name']")
    EMAIL_INPUT = (By.XPATH, "//input[@name='email']")
    PASSWORD_INPUT = (By.XPATH, "//input[@name='password']")
    
    def wait_for_page_load(self):
        """Ожидание загрузки страницы личного кабинета"""
        self.wait.until(EC.presence_of_element_located(self.PROFILE_LINK))
    
    def logout(self):
        """Выход из аккаунта"""
        self.click(self.LOGOUT_BUTTON)