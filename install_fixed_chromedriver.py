# install_fixed_chromedriver.py
import os
import requests
import zipfile
import subprocess

def get_chrome_version():
    """Получаем версию Chrome из реестра"""
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
    
    return "114.0.5735.90"  # Запасная версия

def download_and_install_chromedriver():
    """Скачиваем и устанавливаем 64-битный ChromeDriver"""
    chrome_version = get_chrome_version()
    major_version = chrome_version.split('.')[0]  # Берем только мажорную версию
    
    print(f"🔧 Мажорная версия Chrome: {major_version}")
    
    # Скачиваем информацию о последней версии ChromeDriver
    try:
        latest_url = f"https://chromedriver.storage.googleapis.com/LATEST_RELEASE_{major_version}"
        response = requests.get(latest_url)
        if response.status_code == 200:
            chromedriver_version = response.text.strip()
            print(f"✅ Совместимая версия ChromeDriver: {chromedriver_version}")
        else:
            chromedriver_version = chrome_version
            print(f"⚠️ Используем версию Chrome: {chromedriver_version}")
    except:
        chromedriver_version = chrome_version
        print(f"⚠️ Используем версию Chrome: {chromedriver_version}")
    
    # Скачиваем 64-битную версию
    download_url = f"https://chromedriver.storage.googleapis.com/{chromedriver_version}/chromedriver_win64.zip"
    print(f"📥 Скачиваем из: {download_url}")
    
    try:
        response = requests.get(download_url)
        if response.status_code == 200:
            # Сохраняем zip файл
            zip_path = "chromedriver_win64.zip"
            with open(zip_path, "wb") as f:
                f.write(response.content)
            print("✅ ChromeDriver скачан")
            
            # Распаковываем
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall("drivers")
            print("✅ ChromeDriver распакован в папку drivers/")
            
            # Переименовываем если нужно
            chromedriver_exe = os.path.join("drivers", "chromedriver.exe")
            if os.path.exists(chromedriver_exe):
                print(f"✅ ChromeDriver готов: {chromedriver_exe}")
                
                # Проверяем размер файла
                file_size = os.path.getsize(chromedriver_exe)
                print(f"📊 Размер файла: {file_size} байт")
                
                return True
            else:
                # Проверяем что распаковалось
                for file in os.listdir("drivers"):
                    print(f"📁 В папке: {file}")
                
        else:
            print(f"❌ Ошибка скачивания: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка скачивания: {e}")
        return False
    finally:
        # Удаляем временный файл
        if os.path.exists("chromedriver_win64.zip"):
            os.remove("chromedriver_win64.zip")

def test_chromedriver():
    """Тестируем установленный ChromeDriver"""
    chromedriver_path = os.path.join("drivers", "chromedriver.exe")
    
    if not os.path.exists(chromedriver_path):
        print("❌ ChromeDriver не найден")
        return False
    
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.chrome.service import Service
        
        print("🧪 Тестируем ChromeDriver...")
        
        options = Options()
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        service = Service(chromedriver_path)
        driver = webdriver.Chrome(service=service, options=options)
        
        driver.get("https://www.google.com")
        print(f"✅ УСПЕХ! ChromeDriver работает!")
        print(f"📄 Заголовок: {driver.title}")
        print(f"🌐 URL: {driver.current_url}")
        
        driver.quit()
        return True
        
    except Exception as e:
        print(f"❌ Ошибка тестирования: {e}")
        import traceback
        print(f"📋 Детали:\n{traceback.format_exc()}")
        return False

if __name__ == "__main__":
    print("🚀 Установка 64-битного ChromeDriver...")
    print("=" * 50)
    
    # Создаем папку drivers если её нет
    if not os.path.exists("drivers"):
        os.makedirs("drivers")
        print("📁 Создана папка drivers/")
    
    # Скачиваем и устанавливаем
    if download_and_install_chromedriver():
        print("✅ ChromeDriver установлен")
        print("=" * 50)
        # Тестируем
        test_chromedriver()
    else:
        print("❌ Не удалось установить ChromeDriver")