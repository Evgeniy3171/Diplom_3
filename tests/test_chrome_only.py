# tests/test_chrome_only.py
import allure
import pytest
from selenium import webdriver  # ДОБАВИТЬ ЭТУ СТРОЧКУ!
from selenium.webdriver.chrome.options import Options as ChromeOptions

@allure.feature('Chrome тесты')
class TestChromeOnly:
    
    @pytest.fixture
    def chrome_driver(self):
        """Фикстура только для Chrome"""
        options = ChromeOptions()
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        driver = webdriver.Chrome(options=options)
        driver.implicitly_wait(10)
        driver.maximize_window()
        
        yield driver
        driver.quit()
    
    @allure.title('Проверка Chrome драйвера')
    def test_chrome_driver(self, chrome_driver):
        """Тест только для Chrome"""
        assert chrome_driver is not None
        assert "chrome" in chrome_driver.name.lower()
        print(f"✅ Chrome драйвер работает: {chrome_driver.name}")