from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import allure

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.base_url = "https://stellarburgers.education-services.ru"

    def find_element(self, locator, time=15):
        """Поиск элемента с увеличенным временем ожидания"""
        try:
            return WebDriverWait(self.driver, time).until(
                EC.presence_of_element_located(locator),
                message=f"Element {locator} not found"
            )
        except TimeoutException:
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="screenshot_on_error",
                attachment_type=allure.attachment_type.PNG
            )
            raise

    def find_element_visible(self, locator, time=15):
        """Поиск видимого элемента"""
        try:
            return WebDriverWait(self.driver, time).until(
                EC.visibility_of_element_located(locator),
                message=f"Element {locator} not visible"
            )
        except TimeoutException:
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="screenshot_on_error",
                attachment_type=allure.attachment_type.PNG
            )
            raise

    def click_element(self, locator):
        element = self.find_element_visible(locator)
        element.click()

    def get_text(self, locator):
        element = self.find_element_visible(locator)
        return element.text

    def is_element_visible(self, locator, timeout=5):
        try:
            self.find_element_visible(locator, timeout)
            return True
        except:
            return False
    
    def go_to_main_page(self):
        """Переход на главную страницу"""
        self.driver.get(self.base_url)
        self.wait_for_page_load()

    def wait_for_page_load(self, timeout=15):
        """Ожидание загрузки страницы"""
        WebDriverWait(self.driver, timeout).until(
            lambda driver: driver.execute_script('return document.readyState') == 'complete'
        )