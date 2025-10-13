from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def find_element(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))
    
    def find_elements(self, locator):
        return self.wait.until(EC.presence_of_all_elements_located(locator))
    
    def click(self, locator):
        """Улучшенный клик с обработкой исключений"""
        try:
            element = self.find_element(locator)
            element.click()
        except ElementClickInterceptedException:
            # Если элемент перекрыт, пробуем клик через JavaScript
            print("⚠️ Элемент перекрыт, используем JS клик")
            element = self.find_element(locator)
            self.driver.execute_script("arguments[0].click();", element)
    
    def click_js(self, locator):
        """Клик через JavaScript (обход проблем с перекрытием)"""
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].click();", element)
    
    def wait_for_element_to_disappear(self, locator, timeout=10):
        WebDriverWait(self.driver, timeout).until(
            EC.invisibility_of_element_located(locator)
        )
    
    def is_element_visible(self, locator):
        try:
            return self.find_element(locator).is_displayed()
        except:
            return False
    
    def scroll_to_element(self, locator):
        """Скролл к элементу"""
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
    
    def wait_for_page_loaded(self, timeout=15):
        """Ожидание полной загрузки страницы"""
        WebDriverWait(self.driver, timeout).until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )