import pytest
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="browser to run tests: chrome or firefox")
    parser.addoption("--headless", action="store_true", help="run tests in headless mode")
    parser.addoption("--base-url", action="store", default="https://stellarburgers.education-services.ru", help="base URL for the application")

@pytest.fixture
def driver(request):
    browser_name = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")
    base_url = request.config.getoption("--base-url")
    
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
            driver = webdriver.Chrome(service=service, options=options)
        except Exception as e:
            print(f"Webdriver-manager failed: {e}. Trying manual driver...")
            # Пробуем ручной путь
            chrome_driver_path = get_chrome_driver_path()
            service = ChromeService(executable_path=chrome_driver_path)
            driver = webdriver.Chrome(service=service, options=options)
            
    elif browser_name == "firefox":
        from selenium.webdriver.firefox.service import Service as FirefoxService
        
        options = FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        options.add_argument("--width=1920")
        options.add_argument("--height=1080")
        
        try:
            from webdriver_manager.firefox import GeckoDriverManager
            service = FirefoxService(GeckoDriverManager().install())
            driver = webdriver.Firefox(service=service, options=options)
        except Exception as e:
            print(f"Webdriver-manager failed: {e}. Trying manual driver...")
            firefox_driver_path = get_firefox_driver_path()
            service = FirefoxService(executable_path=firefox_driver_path)
            driver = webdriver.Firefox(service=service, options=options)
    else:
        raise ValueError(f"Unsupported browser: {browser_name}")
    
    driver.implicitly_wait(10)
    driver.maximize_window()
    
    # Сохраняем base_url как отдельную переменную
    driver._base_url = base_url
    
    yield driver
    
    driver.quit()

@pytest.fixture
def base_url(request):
    return request.config.getoption("--base-url")

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