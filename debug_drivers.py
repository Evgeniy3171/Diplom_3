# debug_drivers.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

def test_chrome():
    print("🔧 Тестируем Chrome...")
    try:
        options = ChromeOptions()
        options.add_argument("--window-size=1920,1080")
        driver = webdriver.Chrome(options=options)
        print(f"✅ Chrome работает: {driver.name}")
        driver.quit()
        return True
    except Exception as e:
        print(f"❌ Chrome ошибка: {e}")
        return False

def test_firefox():
    print("🔧 Тестируем Firefox...")
    try:
        options = FirefoxOptions()
        options.add_argument("--width=1920")
        options.add_argument("--height=1080")
        driver = webdriver.Firefox(options=options)
        print(f"✅ Firefox работает: {driver.name}")
        driver.quit()
        return True
    except Exception as e:
        print(f"❌ Firefox ошибка: {e}")
        return False

if __name__ == "__main__":
    print("🚀 ДИАГНОСТИКА ДРАЙВЕРОВ")
    print("=" * 50)
    
    chrome_ok = test_chrome()
    firefox_ok = test_firefox()
    
    print(f"\n📊 РЕЗУЛЬТАТЫ:")
    print(f"Chrome: {'✅ РАБОТАЕТ' if chrome_ok else '❌ НЕ РАБОТАЕТ'}")
    print(f"Firefox: {'✅ РАБОТАЕТ' if firefox_ok else '❌ НЕ РАБОТАЕТ'}")