# simple_diagnose.py
import os
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def simple_diagnose():
    print("Простая диагностика...")
    
    # Пробуем разные способы инициализации драйвера
    
    # Способ 1: Прямое использование Chrome
    try:
        print("Способ 1: Прямое использование Chrome...")
        driver = webdriver.Chrome()
        test_page(driver)
        return
    except Exception as e:
        print(f"Способ 1 не сработал: {e}")
    
    # Способ 2: С указанием пути к драйверу
    try:
        print("Способ 2: С указанием пути...")
        from selenium.webdriver.chrome.service import Service
        service = Service('chromedriver.exe')
        driver = webdriver.Chrome(service=service)
        test_page(driver)
        return
    except Exception as e:
        print(f"Способ 2 не сработал: {e}")
    
    # Способ 3: С webdriver-manager
    try:
        print("Способ 3: С webdriver-manager...")
        from webdriver_manager.chrome import ChromeDriverManager
        from selenium.webdriver.chrome.service import Service
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)
        test_page(driver)
        return
    except Exception as e:
        print(f"Способ 3 не сработал: {e}")
    
    print("Все способы не сработали. Проверьте установку Chrome и драйверов.")

def test_page(driver):
    try:
        print("Тестируем загрузку страницы...")
        driver.get("https://stellarburgers.education-services.ru/")
        time.sleep(3)
        
        print(f"Заголовок страницы: {driver.title}")
        print(f"URL: {driver.current_url}")
        
        # Проверяем основные элементы
        elements_to_check = [
            ("Конструктор", "//a[contains(text(), 'Конструктор') or contains(@href, '/')]"),
            ("Лента заказов", "//a[contains(text(), 'Лента заказов') or contains(@href, 'feed')]"),
            ("Булки", "//h2[contains(text(), 'Булки')]"),
            ("Соусы", "//h2[contains(text(), 'Соусы')]"),
            ("Начинки", "//h2[contains(text(), 'Начинки')]"),
        ]
        
        for name, xpath in elements_to_check:
            elements = driver.find_elements(By.XPATH, xpath)
            print(f"{name}: найдено {len(elements)} элементов")
            if elements:
                print(f"  - Текст: {elements[0].text}")
        
        print("✓ Диагностика завершена успешно!")
        
    except Exception as e:
        print(f"✗ Ошибка при тестировании: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    simple_diagnose()