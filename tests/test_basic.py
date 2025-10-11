import allure
import pytest
from selenium.webdriver.common.by import By

@allure.feature('Базовые проверки')
class TestBasicFunctionality:
    @allure.title('Приложение доступно и загружается')
    def test_app_available(self, driver):
        driver.get("https://stellarburgers.education-services.ru")
        
        import time
        time.sleep(3)
        
        # Проверяем, что страница загрузилась
        assert "stellarburgers" in driver.current_url
        assert driver.title != ""  # Заголовок не пустой
        
        # Проверяем наличие основных элементов
        assert len(driver.find_elements(By.TAG_NAME, "body")) > 0
        assert len(driver.find_elements(By.XPATH, "//*[contains(text(), 'бургер') or contains(text(), 'Burger')]")) > 0