# fix_chromedriver_v3.py
import os
import sys
import requests
import zipfile
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService

def cleanup_drivers():
    """Очистка старых драйверов"""
    print("🧹 Очищаем старые драйверы...")
    try:
        # Закрываем все процессы chromedriver
        if os.name == 'nt':  # Windows
            os.system('taskkill /f /im chromedriver.exe 2>nul')
        else:  # Linux/Mac
            os.system('pkill -f chromedriver')
    except:
        pass

def get_chrome_version():
    """Получаем версию Chrome"""
    try:
        if os.name == 'nt':  # Windows
            result = subprocess.run([
                'reg', 'query', 
                'HKEY_CURRENT_USER\\Software\\Google\\Chrome\\BLBeacon', 
                '/v', 'version'
            ], capture_output=True, text=True, shell=True)
            if result.returncode == 0:
                version = result.stdout.split()[-1]
                return version
    except:
        pass
    
    try:
        # Альтернативный способ для Windows
        paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
        ]
        for path in paths:
            if os.path.exists(path):
                result = subprocess.run([path, '--version'], capture_output=True, text=True)
                version = result.stdout.strip().split()[-1]
                return version
    except:
        pass
    
    return "141.0.7163.0"  # Версия по умолчанию

def download_chromedriver_simple():
    """Простая загрузка ChromeDriver"""
    print("📥 Простая установка ChromeDriver...")
    
    # Создаем папку drivers если её нет
    drivers_dir = "drivers"
    os.makedirs(drivers_dir, exist_ok=True)
    
    # Для Windows
    chromedriver_url = "https://storage.googleapis.com/chrome-for-testing-public/141.0.7163.0/win64/chromedriver-win64.zip"
    
    try:
        print(f"Скачиваем из: {chromedriver_url}")
        response = requests.get(chromedriver_url, timeout=30)
        
        if response.status_code == 200:
            zip_path = os.path.join(drivers_dir, "chromedriver.zip")
            with open(zip_path, 'wb') as f:
                f.write(response.content)
            print("✅ Файл скачан")
            
            # Распаковываем
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(drivers_dir)
            print("✅ Файл распакован")
            
            # Ищем chromedriver.exe
            for root, dirs, files in os.walk(drivers_dir):
                for file in files:
                    if "chromedriver" in file.lower() and file.endswith('.exe'):
                        chromedriver_path = os.path.join(root, file)
                        print(f"✅ Найден ChromeDriver: {chromedriver_path}")
                        return chromedriver_path
            
            os.remove(zip_path)
            
        else:
            print(f"❌ Ошибка скачивания: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    
    return None

def install_webdriver_manager():
    """Установка webdriver-manager"""
    print("📦 Устанавливаем webdriver-manager...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "webdriver-manager"])
        print("✅ webdriver-manager установлен")
        return True
    except Exception as e:
        print(f"❌ Ошибка установки: {e}")
        return False

def test_chromedriver():
    """Тестируем ChromeDriver"""
    print("🧪 Тестируем ChromeDriver...")
    
    try:
        # Способ 1: Через webdriver-manager
        from webdriver_manager.chrome import ChromeDriverManager
        from selenium.webdriver.chrome.service import Service as ChromeService
        
        driver_path = ChromeDriverManager().install()
        service = ChromeService(driver_path)
        
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        driver = webdriver.Chrome(service=service, options=options)
        driver.get("https://stellarburgers.education-services.ru/")
        print(f"✅ ChromeDriver работает! Страница: {driver.title}")
        driver.quit()
        return True
        
    except Exception as e:
        print(f"❌ ChromeDriver не работает: {e}")
        return False

def main():
    print("🔧 Исправляем проблему с ChromeDriver...")
    cleanup_drivers()
    
    # Получаем версию Chrome
    chrome_version = get_chrome_version()
    print(f"🎯 Версия Chrome: {chrome_version}")
    
    # Устанавливаем webdriver-manager если нужно
    try:
        import webdriver_manager
    except ImportError:
        install_webdriver_manager()
    
    # Пробуем установить через webdriver-manager
    if test_chromedriver():
        print("🎉 ChromeDriver успешно настроен!")
        return
    
    # Если не сработало, пробуем ручную установку
    print("🔄 Пробуем ручную установку...")
    chromedriver_path = download_chromedriver_simple()
    
    if chromedriver_path and os.path.exists(chromedriver_path):
        print(f"✅ Ручная установка успешна: {chromedriver_path}")
        
        # Тестируем ручной драйвер
        try:
            service = ChromeService(chromedriver_path)
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")
            
            driver = webdriver.Chrome(service=service, options=options)
            driver.get("https://google.com")
            print(f"✅ Ручной ChromeDriver работает! Заголовок: {driver.title}")
            driver.quit()
        except Exception as e:
            print(f"❌ Ручной ChromeDriver не работает: {e}")
    else:
        print("❌ Все способы не сработали")
        print("💡 Рекомендации:")
        print("1. Установите ChromeDriver вручную в папку drivers/")
        print("2. Скачайте с https://chromedriver.chromium.org/")
        print("3. Убедитесь, что версия соответствует вашему Chrome")

if __name__ == "__main__":
    main()