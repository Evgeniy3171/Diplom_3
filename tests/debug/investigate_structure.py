from selenium.webdriver.common.by import By
import time

def investigate_structure(driver):
    """Детальное исследование структуры сайта"""
    driver.get("https://stellarburgers.education-services.ru/")
    time.sleep(3)
    
    print("=== INVESTIGATING PAGE STRUCTURE ===")
    
    # Ищем все возможные элементы
    search_patterns = [
        # Навигация
        ("Navigation links", "//a"),
        ("Buttons", "//button"),
        
        # Ингредиенты
        ("Ingredient sections", "//section"),
        ("Ingredient items", "//div[contains(@class, 'ingredient')]"),
        ("Ingredient links", "//a[contains(@class, 'ingredient')]"),
        
        # Счётчики
        ("Counters", "//div[contains(@class, 'counter')]"),
        
        # Конструктор
        ("Constructor area", "//section[contains(@class, 'constructor')]"),
        ("Drop zones", "//div[contains(@class, 'basket')]"),
        
        # Модальные окна
        ("Modal elements", "//div[contains(@class, 'modal')]"),
    ]
    
    for name, pattern in search_patterns:
        print(f"\n--- {name} ({pattern}) ---")
        try:
            elements = driver.find_elements(By.XPATH, pattern)
            print(f"Found {len(elements)} elements")
            
            for i, elem in enumerate(elements[:5]):  # Покажем первые 5
                try:
                    text = elem.text.replace('\n', ' ')[:100] if elem.text else "No text"
                    classes = elem.get_attribute('class') or "No class"
                    href = elem.get_attribute('href') or "No href"
                    print(f"  {i}: class='{classes}', text='{text}', href='{href}'")
                except:
                    print(f"  {i}: Could not get element info")
                    
        except Exception as e:
            print(f"Error: {e}")
    
    # Специальный поиск ингредиентов
    print("\n=== INGREDIENT SPECIFIC SEARCH ===")
    ingredient_selectors = [
        "//h2[contains(text(), 'Булки')]",
        "//h2[contains(text(), 'Соусы')]",
        "//h2[contains(text(), 'Начинки')]",
    ]
    
    for selector in ingredient_selectors:
        try:
            elements = driver.find_elements(By.XPATH, selector)
            print(f"\n{selector}: {len(elements)} elements found")
            for elem in elements:
                print(f"  Text: {elem.text}")
                # Найдём родительский контейнер
                parent = elem.find_element(By.XPATH, "./..")
                print(f"  Parent class: {parent.get_attribute('class')}")
                # Найдём все ссылки в этом разделе
                links = parent.find_elements(By.XPATH, ".//a")
                print(f"  Links in section: {len(links)}")
                for link in links[:2]:
                    print(f"    Link class: {link.get_attribute('class')}")
        except Exception as e:
            print(f"Error with {selector}: {e}")

def test_investigate(driver):
    investigate_structure(driver)