# tests/test_firefox_only.py
import allure
import pytest
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions

@allure.feature('Firefox тесты')
class TestFirefoxOnly:
    
    @pytest.fixture
    def firefox_driver(self):
        """Фикстура только для Firefox"""
        options = FirefoxOptions()
        options.add_argument("--width=1920")
        options.add_argument("--height=1080")
        
        driver = webdriver.Firefox(options=options)
        driver.implicitly_wait(10)
        driver.maximize_window()
        
        yield driver
        driver.quit()
    
    @allure.title('Проверка Firefox драйвера')
    def test_firefox_driver(self, firefox_driver):
        """Тест только для Firefox"""
        assert firefox_driver is not None
        assert "firefox" in firefox_driver.name.lower()
        print(f"✅ Firefox драйвер работает: {firefox_driver.name}")