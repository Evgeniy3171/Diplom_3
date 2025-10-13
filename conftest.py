import pytest
import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="browser to run tests: chrome or firefox")
    parser.addoption("--headless", action="store_true", help="run tests in headless mode")

def get_chrome_driver_path():
    """Получаем путь к ChromeDriver"""
    possible_paths = [
        "C:\\WebDriver\\bin\\chromedriver.exe",
        "C:\\Program Files\\WebDriver\\bin\\chromedriver.exe",
        os.path.join(os.getcwd(), "drivers", "chromedriver.exe"),
        "chromedriver.exe"
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    return "chromedriver"

def get_firefox_driver_path():
    """Получаем путь к GeckoDriver"""
    possible_paths = [
        "C:\\WebDriver\\bin\\geckodriver.exe",
        "C:\\Program Files\\WebDriver\\bin\\geckodriver.exe", 
        os.path.join(os.getcwd(), "drivers", "geckodriver.exe"),
        "geckodriver.exe"
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    return "geckodriver"

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
            
            try:
                # Пробуем использовать webdriver-manager
                from webdriver_manager.chrome import ChromeDriverManager
                service = ChromeService(ChromeDriverManager().install())
                driver_instance = webdriver.Chrome(service=service, options=options)
                print("✅ Chrome драйвер запущен через webdriver-manager")
            except Exception as e:
                print(f"❌ Webdriver-manager для Chrome не сработал: {e}")
                print("🔄 Пробуем ручной путь...")
                # Пробуем ручной путь
                chrome_driver_path = get_chrome_driver_path()
                service = ChromeService(executable_path=chrome_driver_path)
                driver_instance = webdriver.Chrome(service=service, options=options)
                print(f"✅ Chrome драйвер запущен через ручной путь: {chrome_driver_path}")
                
        elif browser_name == "firefox":
            from selenium.webdriver.firefox.service import Service as FirefoxService
            
            options = FirefoxOptions()
            if headless:
                options.add_argument("--headless")
            options.add_argument("--width=1920")
            options.add_argument("--height=1080")
            
            try:
                # Пробуем использовать webdriver-manager
                from webdriver_manager.firefox import GeckoDriverManager
                service = FirefoxService(GeckoDriverManager().install())
                driver_instance = webdriver.Firefox(service=service, options=options)
                print("✅ Firefox драйвер запущен через webdriver-manager")
            except Exception as e:
                print(f"❌ Webdriver-manager для Firefox не сработал: {e}")
                print("🔄 Пробуем ручной путь...")
                firefox_driver_path = get_firefox_driver_path()
                service = FirefoxService(executable_path=firefox_driver_path)
                driver_instance = webdriver.Firefox(service=service, options=options)
                print(f"✅ Firefox драйвер запущен через ручной путь: {firefox_driver_path}")
                
        else:
            raise ValueError(f"Unsupported browser: {browser_name}")
        
        if driver_instance is None:
            raise Exception(f"Не удалось инициализировать драйвер для {browser_name}")
        
        driver_instance.implicitly_wait(10)
        driver_instance.maximize_window()
        
        yield driver_instance
        
    except Exception as e:
        print(f"❌ Критическая ошибка при инициализации драйвера {browser_name}: {e}")
        pytest.skip(f"Драйвер {browser_name} недоступен: {e}")
    
    finally:
        if driver_instance:
            driver_instance.quit()