# install_chromedriver.py
import os
import platform
import zipfile
import requests
import subprocess
from selenium import webdriver

def get_chrome_version():
    """Получаем версию Chrome"""
    try:
        # Способ 1: через реестр
        result = subprocess.run(
            ['reg', 'query', 'HKEY_CURRENT_USER\\Software\\Google\\Chrome\\BLBeacon', '/v', 'version'],
            capture_output=True, text=True, encoding='utf-8'
        )
        if result.returncode == 0:
            for line in result.stdout.split('\n'):
                if 'version' in line.lower():
                    version = line.split()[-1]
                    print(f"✅ Версия Chrome из реестра: {version}")
                    return version
        
        # Способ 2: через where и --version
        chrome_paths = [
            "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
            "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
            "chrome.exe"
        ]
        
        for path in chrome_paths:
            try:
                result = subprocess.run([path, '--version'], capture_output=True, text=True)
                if result.returncode == 0:
                    version = result.stdout.strip().split()[-1]
                    print(f"✅ Версия Chrome: {version}")
                    return version
            except:
                continue
                
    except Exception as e:
        print(f"❌ Ошибка получения версии Chrome: {e}")
    
    return None

def download_chromedriver(version):
    """Скачиваем правильный ChromeDriver"""
    # Базовый URL для скачивания
    base_url = "https://chromedriver.storage.googleapis.com"
    
    # Получаем основную версию (первые три числа)
    major_version = '.'.join(version.split('.')[:3])
    
    # Получаем список доступных версий
    try:
        response = requests.get(f"{base_url}/LATEST_RELEASE_{major_version}")
        if response.status_code == 200:
            chromedriver_version = response.text.strip()
            print(f"✅ Найдена версия ChromeDriver: {chromedriver_version}")
        else:
            # Используем ту же версию что и Chrome
            chromedriver_version = version
            print(f"⚠️ Используем версию Chrome: {chromedriver_version}")
    except:
        chromedriver_version = version
        print(f"⚠️ Используем версию Chrome: {chromedriver_version}")
    
    # Определяем архитектуру
    architecture = "win32"  # По умолчанию для Windows
    if platform.architecture()[0] == "64bit":
        architecture = "win64"
    
    print(f"🔧 Архитектура: {architecture}")
    
    # URL для скачивания
    download_url = f"{base_url}/{chromedriver_version}/chromedriver_{architecture}.zip"
    print(f"📥 URL для скачивания: {download_url}")
    
    # Скачиваем
    try:
        response = requests.get(download_url)
        if response.status_code == 200:
            with open("chromedriver.zip", "wb") as f:
                f.write(response.content)
            print("✅ ChromeDriver скачан")
            
            # Распаковываем
            with zipfile.ZipFile("chromedriver.zip", "r") as zip_ref:
                zip_ref.extractall("drivers")
            print("✅ ChromeDriver распакован в папку drivers/")
            
            # Удаляем zip файл
            os.remove("chromedriver.zip")
            print("✅ Временные файлы удалены")
            
            return True
        else:
            print(f"❌ Ошибка скачивания: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Ошибка скачивания: {e}")
        return False

def test_chromedriver():
    """Тестируем ChromeDriver"""
    driver_path = os.path.join("drivers", "chromedriver.exe")
    
    if not os.path.exists(driver_path):
        print("❌ ChromeDriver не найден")
        return False
    
    try:
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.chrome.service import Service
        
        options = Options()
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        service = Service(driver_path)
        driver = webdriver.Chrome(service=service, options=options)
        
        driver.get("https://www.google.com")
        print(f"✅ ChromeDriver работает! Заголовок: {driver.title}")
        
        driver.quit()
        return True
        
    except Exception as e:
        print(f"❌ Ошибка тестирования ChromeDriver: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Установка правильного ChromeDriver...")
    
    # Создаем папку drivers если её нет
    if not os.path.exists("drivers"):
        os.makedirs("drivers")
    
    # Получаем версию Chrome
    version = get_chrome_version()
    if not version:
        print("❌ Не удалось определить версию Chrome")
        print("🔧 Используем версию 114.0.5735.90 как запасной вариант")
        version = "114.0.5735.90"
    
    # Скачиваем ChromeDriver
    if download_chromedriver(version):
        # Тестируем
        test_chromedriver()
    else:
        print("❌ Не удалось установить ChromeDriver")