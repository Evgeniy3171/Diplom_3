# test_debug.py
import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService

def test_debug_driver():
    """Простой тест для диагностики драйвера"""
    print("🔧 Начинаем диагностику Chrome драйвера...")
    
    try:
        options = ChromeOptions()
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        print("📥 Устанавливаем ChromeDriver через webdriver-manager...")
        service = ChromeService(ChromeDriverManager().install())
        
        print("🚀 Инициализируем драйвер...")
        driver = webdriver.Chrome(service=service, options=options)
        
        print("🌐 Открываем страницу...")
        driver.get("https://stellarburgers.education-services.ru/")
        
        print(f"✅ Страница загружена: {driver.title}")
        print(f"📊 URL: {driver.current_url}")
        
        # Делаем скриншот
        driver.save_screenshot("debug_screenshot.png")
        print("📸 Скриншот сохранен: debug_screenshot.png")
        
        driver.quit()
        print("✅ Тест завершен успешно!")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        print(f"🔧 Тип ошибки: {type(e)}")
        import traceback
        print(f"📋 Полный трейсбэк:\n{traceback.format_exc()}")
        pytest.fail(f"Драйвер не инициализирован: {e}")

if __name__ == "__main__":
    test_debug_driver()