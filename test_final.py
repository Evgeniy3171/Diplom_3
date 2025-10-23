# test_final.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import os

def test_final():
    """Финальный тест"""
    driver_path = os.path.join("drivers", "chromedriver.exe")
    
    if not os.path.exists(driver_path):
        print("❌ ChromeDriver не найден")
        return False
    
    try:
        options = Options()
        options.add_argument("--window-size=1920,1080")
        
        service = Service(driver_path)
        driver = webdriver.Chrome(service=service, options=options)
        
        driver.get("https://stellarburgers.education-services.ru/")
        print(f"✅ СТРАНИЦА ЗАГРУЖЕНА: {driver.title}")
        
        # Проверяем ключевые элементы
        checks = [
            "Конструктор",
            "Лента заказов", 
            "Войти в аккаунт",
            "Булки",
            "Соусы",
            "Начинки"
        ]
        
        page_text = driver.page_source
        found_count = 0
        
        for check in checks:
            if check in page_text:
                print(f"✅ Найден: {check}")
                found_count += 1
            else:
                print(f"⚠️ Не найден: {check}")
        
        print(f"📊 Итого найдено: {found_count}/{len(checks)}")
        
        driver.quit()
        return found_count > 0
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

if __name__ == "__main__":
    success = test_final()
    print("🎉 ТЕСТ ПРОЙДЕН!" if success else "❌ ТЕСТ НЕ ПРОЙДЕН")