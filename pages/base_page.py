# pages/base_page.py
import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from config.urls import Urls

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.urls = Urls()
    
    @allure.step("Найти элемент {locator}")
    def find_element(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))
    
    @allure.step("Найти элементы {locator}")
    def find_elements(self, locator):
        return self.wait.until(EC.presence_of_all_elements_located(locator))
    
    @allure.step("Кликнуть на элемент {locator}")
    def click(self, locator):
        try:
            element = self.find_element(locator)
            element.click()
        except ElementClickInterceptedException:
            element = self.find_element(locator)
            self.driver.execute_script("arguments[0].click();", element)
    
    @allure.step("Кликнуть через JavaScript на элемент {locator}")
    def click_js(self, locator):
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].click();", element)
    
    @allure.step("Ожидать исчезновения элемента {locator}")
    def wait_for_element_to_disappear(self, locator, timeout=10):
        WebDriverWait(self.driver, timeout).until(
            EC.invisibility_of_element_located(locator)
        )
    
    @allure.step("Проверить видимость элемента {locator}")
    def is_element_visible(self, locator):
        try:
            return self.find_element(locator).is_displayed()
        except:
            return False
    
    @allure.step("Прокрутить к элементу {locator}")
    def scroll_to_element(self, locator):
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
    
    @allure.step("Ожидать загрузки страницы")
    def wait_for_page_loaded(self, timeout=15):
        WebDriverWait(self.driver, timeout).until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )
    
    @allure.step("Перейти по URL: {url}")
    def go_to_url(self, url):
        self.driver.get(url)
        self.wait_for_page_loaded()
    
    @allure.step("Получить текущий URL")
    def get_current_url(self):
        return self.driver.current_url
    
    @allure.step("Выполнить JavaScript код")
    def execute_script(self, script, *args):
        return self.driver.execute_script(script, *args)