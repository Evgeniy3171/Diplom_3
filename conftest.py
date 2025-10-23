# conftest.py
import pytest
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", 
                    help="browser to run tests: chrome or firefox")

@pytest.fixture
def driver(request):
    browser_name = request.config.getoption("--browser").lower()
    print(f"🚀 Инициализируем драйвер для: {browser_name}")
    
    driver_instance = None
    
    try:
        if browser_name == "chrome":
            print("🔧 Настраиваем Chrome...")
            options = ChromeOptions()
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            
            # Используем локальный драйвер
            driver_path = os.path.join(os.path.dirname(__file__), "drivers", "chromedriver.exe")
            
            if os.path.exists(driver_path):
                print(f"📁 Используем локальный драйвер: {driver_path}")
                service = ChromeService(driver_path)
                driver_instance = webdriver.Chrome(service=service, options=options)
                print("✅ ChromeDriver успешно инициализирован!")
            else:
                print(f"❌ Локальный драйвер не найден по пути: {driver_path}")
                # Показываем что есть в папке
                drivers_dir = os.path.join(os.path.dirname(__file__), "drivers")
                if os.path.exists(drivers_dir):
                    print(f"📁 Содержимое папки drivers:")
                    for item in os.listdir(drivers_dir):
                        item_path = os.path.join(drivers_dir, item)
                        print(f"   - {item} ({'file' if os.path.isfile(item_path) else 'dir'})")
                pytest.skip("ChromeDriver не найден")
        
        elif browser_name == "firefox":
            # Пропускаем Firefox для простоты
            pytest.skip("Firefox тесты временно отключены")
        
        else:
            pytest.skip(f"Неподдерживаемый браузер: {browser_name}")
        
        # Общие настройки
        driver_instance.implicitly_wait(10)
        driver_instance.set_page_load_timeout(30)
        
        print(f"✅ Драйвер {driver_instance.name} готов к работе")
        
        yield driver_instance
        
    except Exception as e:
        print(f"❌ Ошибка инициализации драйвера: {e}")
        import traceback
        print(f"📋 Детали ошибки:\n{traceback.format_exc()}")
        pytest.skip(f"Не удалось инициализировать драйвер: {e}")
    
    finally:
        if driver_instance:
            try:
                driver_instance.quit()
                print("✅ Драйвер закрыт")
            except Exception as e:
                print(f"⚠️ Ошибка при закрытии драйвера: {e}")