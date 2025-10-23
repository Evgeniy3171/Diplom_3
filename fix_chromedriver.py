# fix_chromedriver.py
import os
import zipfile
import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType

def fix_chromedriver_issue():
    print("🔧 Исправляем проблему с ChromeDriver...")
    
    try:
        # Очистка кэша
        os.system("webdriver-manager clean")
        print("✅ Кэш очищен")
        
        # Установка через webdriver-manager с явным указанием версии
        driver_path = ChromeDriverManager().install()
        print(f"✅ ChromeDriver установлен в: {driver_path}")
        
        # Проверяем работу
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        driver = webdriver.Chrome(executable_path=driver_path, options=options)
        driver.get("https://google.com")
        print(f"✅ ChromeDriver работает! Заголовок: {driver.title}")
        driver.quit()
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        print("🔄 Пробуем альтернативный метод...")
        manual_chromedriver_install()

def manual_chromedriver_install():
    """Ручная установка ChromeDriver"""
    import platform
    system = platform.system().lower()
    
    # Определяем версию Chrome
    try:
        import subprocess
        if system == "windows":
            result = subprocess.run(['reg', 'query', 'HKEY_CURRENT_USER\\Software\\Google\\Chrome\\BLBeacon', '/v', 'version'], 
                                  capture_output=True, text=True)
            version = result.stdout.split()[-1]
        else:
            result = subprocess.run(['google-chrome', '--version'], capture_output=True, text=True)
            version = result.stdout.split()[-1]
        
        major_version = version.split('.')[0]
        print(f"🎯 Версия Chrome: {version}, Major: {major_version}")
        
        # Скачиваем соответствующую версию
        download_chromedriver(major_version, system)
        
    except Exception as e:
        print(f"❌ Не удалось определить версию Chrome: {e}")
        # Устанавливаем последнюю стабильную версию
        download_chromedriver("114", system)

def download_chromedriver(version, system):
    """Скачивание ChromeDriver"""
    base_url = f"https://storage.googleapis.com/chrome-for-testing-public/{version}/win64/chromedriver-win64.zip"
    
    print(f"📥 Скачивание ChromeDriver {version} для {system}...")
    
    try:
        response = requests.get(base_url)
        if response.status_code == 200:
            zip_path = "chromedriver.zip"
            with open(zip_path, 'wb') as f:
                f.write(response.content)
            
            # Распаковываем
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall("drivers")
            
            os.remove(zip_path)
            print("✅ ChromeDriver успешно установлен в папку drivers/")
        else:
            print(f"❌ Не удалось скачать ChromeDriver. Status: {response.status_code}")
    except Exception as e:
        print(f"❌ Ошибка при установке ChromeDriver: {e}")

if __name__ == "__main__":
    fix_chromedriver_issue()