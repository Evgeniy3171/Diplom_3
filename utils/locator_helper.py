from selenium.webdriver.common.by import By
import time

def debug_locators(driver):
    """Функция для отладки локаторов"""
    driver.get("https://stellarburgers.education-services.ru/")
    time.sleep(3)
    
    # Попробуем найти различные элементы
    test_selectors = [
        "//a[contains(@href, 'constructor')]",
        "//a[contains(text(), 'Конструктор')]",
        "//a[contains(@href, 'feed')]",
        "//a[contains(text(), 'Лента заказов')]",
        "//div[contains(@class, 'BurgerIngredients_ingredients__')]",
        "//section[contains(@class, 'BurgerConstructor')]",
        "//div[contains(@class, 'Modal_modal')]",
        "//button[contains(@class, 'button_button')]"
    ]
    
    for selector in test_selectors:
        try:
            elements = driver.find_elements(By.XPATH, selector)
            print(f"Selector: {selector} - Found {len(elements)} elements")
            if elements:
                for i, elem in enumerate(elements[:3]):  # Покажем первые 3 элемента
                    print(f"  Element {i}: {elem.text[:50] if elem.text else 'No text'}")
        except Exception as e:
            print(f"Selector: {selector} - Error: {e}")