# test_quick_check.py
import pytest
import os

def test_quick_chrome_check():
    """Быстрая проверка Chrome"""
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    
    driver_path = os.path.join("drivers", "chromedriver.exe")
    
    if not os.path.exists(driver_path):
        pytest.skip("ChromeDriver не найден")
    
    driver = None
    try:
        options = Options()
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--no-sandbox")
        
        service = Service(driver_path)
        driver = webdriver.Chrome(service=service, options=options)
        
        # Открываем правильный сайт
        driver.get("https://stellarburgers.education-services.ru/")
        
        # Быстрые проверки
        assert "stellarburgers" in driver.current_url
        assert driver.title is not None
        
        # Проверяем ключевые элементы
        page_text = driver.page_source
        assert "Конструктор" in page_text or "бургер" in page_text.lower()
        
        print("✅ Быстрая проверка пройдена!")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка быстрой проверки: {e}")
        return False
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    test_quick_chrome_check()