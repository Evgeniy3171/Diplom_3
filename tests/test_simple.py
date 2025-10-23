# tests/test_simple.py
import allure
import time
from selenium.webdriver.common.by import By

@allure.feature('Простая проверка')
def test_basic_functionality(driver):
    """Базовая проверка функциональности"""
    print(f"🌐 Тестируем в {driver.name}")
    
    # Открываем сайт
    driver.get("https://stellarburgers.education-services.ru/")
    time.sleep(3)
    
    # Проверяем заголовок
    assert "Stellar" in driver.title or "React" in driver.title
    print(f"✅ Страница загружена: {driver.title}")
    
    # Делаем скриншот
    allure.attach(
        driver.get_screenshot_as_png(),
        name="homepage",
        attachment_type=allure.attachment_type.PNG
    )
    
    # Проверяем основные элементы
    elements_to_check = [
        "//button[contains(text(), 'Войти')]",
        "//h1[contains(text(), 'бургер') or contains(text(), 'Burger')]",
        "//section[contains(@class, 'ingredient') or contains(@class, 'Ingredient')]"
    ]
    
    found_elements = 0
    for xpath in elements_to_check:
        try:
            elements = driver.find_elements(By.XPATH, xpath)
            if elements:
                found_elements += 1
                print(f"✅ Найден: {xpath}")
        except:
            print(f"⚠️ Не найден: {xpath}")
    
    print(f"📊 Найдено элементов: {found_elements}/{len(elements_to_check)}")
    assert found_elements >= 1, "Должен быть найден хотя бы один ключевой элемент"