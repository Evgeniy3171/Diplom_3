# install_chromedriver_new.py
import os
import requests
import zipfile
import json
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

def get_chrome_version():
    """Получаем точную версию Chrome"""
    try:
        result = subprocess.run(
            ['reg', 'query', 'HKEY_CURRENT_USER\\Software\\Google\\Chrome\\BLBeacon', '/v', 'version'],
            capture_output=True, text=True, encoding='utf-8', errors='ignore'
        )
        if result.returncode == 0:
            for line in result.stdout.split('\n'):
                if 'version' in line.lower():
                    version = line.split()[-1].strip()
                    print(f"✅ Версия Chrome: {version}")
                    return version
    except Exception as e:
        print(f"❌ Ошибка чтения реестра: {e}")
    
    return None

def get_chromedriver_version(chrome_version):
    """Получаем совместимую версию ChromeDriver"""
    try:
        # Новый endpoint для получения совместимой версии
        url = f"https://googlechromelabs.github.io/chrome-for-testing/latest-versions-per-milestone-with-downloads.json"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            
            # Ищем версию по мажорному номеру
            major_version = chrome_version.split('.')[0]
            if major_version in data['milestones']:
                version_info = data['milestones'][major_version]
                print(f"✅ Найдена версия ChromeDriver: {version_info['version']}")
                return version_info['version']
    except Exception as e:
        print(f"❌ Ошибка получения версии ChromeDriver: {e}")
    
    # Если не нашли, используем стабильную версию
    return "122.0.6261.69"

def download_chromedriver(version):
    """Скачиваем ChromeDriver с нового сервера"""
    # Новый URL для скачивания
    url = f"https://storage.googleapis.com/chrome-for-testing-public/{version}/win64/chromedriver-win64.zip"
    print(f"📥 Скачиваем из: {url}")
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            zip_path = "chromedriver_new.zip"
            with open(zip_path, "wb") as f:
                f.write(response.content)
            print("✅ ChromeDriver скачан")
            
            # Распаковываем
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall("drivers_temp")
            print("✅ ChromeDriver распакован")
            
            # Находим chromedriver.exe (может быть во вложенной папке)
            chromedriver_path = None
            for root, dirs, files in os.walk("drivers_temp"):
                for file in files:
                    if file == "chromedriver.exe":
                        chromedriver_path = os.path.join(root, file)
                        break
                if chromedriver_path:
                    break
            
            if chromedriver_path and os.path.exists(chromedriver_path):
                # Копируем в основную папку drivers
                if not os.path.exists("drivers"):
                    os.makedirs("drivers")
                
                final_path = os.path.join("drivers", "chromedriver.exe")
                with open(chromedriver_path, "rb") as src_file:
                    with open(final_path, "wb") as dst_file:
                        dst_file.write(src_file.read())
                
                print(f"✅ ChromeDriver установлен: {final_path}")
                
                # Очистка
                import shutil
                if os.path.exists("drivers_temp"):
                    shutil.rmtree("drivers_temp")
                if os.path.exists(zip_path):
                    os.remove(zip_path)
                
                return True
            else:
                print("❌ chromedriver.exe не найден в архиве")
                return False
        else:
            print(f"❌ Ошибка скачивания: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка скачивания: {e}")
        return False

def download_fallback_chromedriver():
    """Запасной вариант - скачиваем стабильную версию"""
    stable_version = "122.0.6261.69"
    print(f"🔄 Используем стабильную версию: {stable_version}")
    return download_chromedriver(stable_version)

def test_chromedriver():
    """Тестируем ChromeDriver"""
    chromedriver_path = os.path.join("drivers", "chromedriver.exe")
    
    if not os.path.exists(chromedriver_path):
        print("❌ ChromeDriver не найден")
        return False
    
    try:
        print("🧪 Тестируем ChromeDriver...")
        
        options = Options()
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        service = Service(chromedriver_path)
        driver = webdriver.Chrome(service=service, options=options)
        
        driver.get("https://stellarburgers.education-services.ru/")
        print(f"✅ УСПЕХ! ChromeDriver работает!")
        print(f"📄 Заголовок: {driver.title}")
        print(f"🌐 URL: {driver.current_url}")
        
        # Проверяем основные элементы
        page_source = driver.page_source
        if "Конструктор" in page_source or "бургер" in page_source.lower():
            print("✅ Основные элементы страницы найдены")
        else:
            print("⚠️ Основные элементы не найдены, но страница загружена")
        
        driver.quit()
        return True
        
    except Exception as e:
        print(f"❌ Ошибка тестирования: {e}")
        import traceback
        print(f"📋 Детали:\n{traceback.format_exc()}")
        return False

def main():
    print("🚀 Установка ChromeDriver для новых версий Chrome")
    print("=" * 60)
    
    # Получаем версию Chrome
    chrome_version = get_chrome_version()
    if not chrome_version:
        print("❌ Не удалось определить версию Chrome")
        print("🔧 Используем запасной вариант...")
        if download_fallback_chromedriver():
            test_chromedriver()
        return
    
    print(f"🔍 Chrome версия: {chrome_version}")
    
    # Получаем совместимую версию ChromeDriver
    chromedriver_version = get_chromedriver_version(chrome_version)
    print(f"🔧 Совместимая версия ChromeDriver: {chromedriver_version}")
    
    # Скачиваем
    if download_chromedriver(chromedriver_version):
        print("✅ ChromeDriver успешно установлен")
        print("=" * 60)
        test_chromedriver()
    else:
        print("❌ Не удалось установить ChromeDriver, пробуем запасной вариант...")
        if download_fallback_chromedriver():
            test_chromedriver()

if __name__ == "__main__":
    main()