import allure
import pytest
import os
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

# Настройка логирования
logger = logging.getLogger(__name__)

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="browser to run tests: chrome or firefox")
    parser.addoption("--headless", action="store_true", help="run tests in headless mode")

@pytest.fixture
def driver(request):
    browser_name = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")
    
    driver_instance = None
    
    try:
        if browser_name == "chrome":
            from selenium.webdriver.chrome.service import Service as ChromeService
            
            options = ChromeOptions()
            if headless:
                options.add_argument("--headless")
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            
            # Используем переменные окружения или webdriver-manager
            chrome_driver_path = os.getenv('CHROME_DRIVER_PATH')
            if chrome_driver_path and os.path.exists(chrome_driver_path):
                service = ChromeService(executable_path=chrome_driver_path)
                driver_instance = webdriver.Chrome(service=service, options=options)
                logger.info("Chrome драйвер запущен через переменную окружения")
            else:
                from webdriver_manager.chrome import ChromeDriverManager
                service = ChromeService(ChromeDriverManager().install())
                driver_instance = webdriver.Chrome(service=service, options=options)
                logger.info("Chrome драйвер запущен через webdriver-manager")
                
        elif browser_name == "firefox":
            from selenium.webdriver.firefox.service import Service as FirefoxService
            
            options = FirefoxOptions()
            if headless:
                options.add_argument("--headless")
            options.add_argument("--width=1920")
            options.add_argument("--height=1080")
            
            # Используем переменные окружения или webdriver-manager
            firefox_driver_path = os.getenv('FIREFOX_DRIVER_PATH')
            if firefox_driver_path and os.path.exists(firefox_driver_path):
                service = FirefoxService(executable_path=firefox_driver_path)
                driver_instance = webdriver.Firefox(service=service, options=options)
                logger.info("Firefox драйвер запущен через переменную окружения")
            else:
                from webdriver_manager.firefox import GeckoDriverManager
                service = FirefoxService(GeckoDriverManager().install())
                driver_instance = webdriver.Firefox(service=service, options=options)
                logger.info("Firefox драйвер запущен через webdriver-manager")
                
        else:
            raise ValueError(f"Unsupported browser: {browser_name}")
        
        if driver_instance is None:
            raise Exception(f"Не удалось инициализировать драйвер для {browser_name}")
        
        driver_instance.implicitly_wait(10)
        driver_instance.maximize_window()
        
        yield driver_instance
        
    except Exception as e:
        logger.error(f"Критическая ошибка при инициализации драйвера {browser_name}: {e}")
        pytest.skip(f"Драйвер {browser_name} недоступен: {e}")
    
    finally:
        if driver_instance:
            driver_instance.quit()

# Фикстура для скриншотов
@pytest.fixture(autouse=True)
def screenshot_on_failure(request):
    yield
    if request.node.rep_call.failed:
        driver = request.getfixturevalue('driver')
        allure.attach(
            driver.get_screenshot_as_png(),
            name=f"screenshot_{request.node.name}",
            attachment_type=allure.attachment_type.PNG
        )