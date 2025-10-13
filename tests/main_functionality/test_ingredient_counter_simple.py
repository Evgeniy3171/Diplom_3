import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestIngredientCounterSimple:
    
    @pytest.mark.main_functionality
    def test_ingredient_counter_simple(self, driver):
        """Упрощённый тест с прямыми локаторами"""
        
        print("=== SIMPLE INGREDIENT COUNTER TEST ===")
        
        # Переходим на главную страницу
        driver.get("https://stellarburgers.education-services.ru/")
        time.sleep(3)
        
        # Ждём загрузки
        wait = WebDriverWait(driver, 10)
        
        # Находим раздел с соусами
        print("Looking for sauce section...")
        sauce_headers = driver.find_elements(By.XPATH, "//h2[contains(text(), 'Соусы')]")
        print(f"Found {len(sauce_headers)} sauce headers")
        
        if not sauce_headers:
            # Если не нашли по тексту, ищем по структуре
            all_headers = driver.find_elements(By.XPATH, "//h2")
            print("All headers on page:")
            for header in all_headers:
                print(f"  - {header.text}")
            pytest.fail("Could not find sauce section")
        
        sauce_header = sauce_headers[0]
        print(f"Sauce header text: '{sauce_header.text}'")
        
        # Находим родительский контейнер
        sauce_section = sauce_header.find_element(By.XPATH, "./..")
        print(f"Sauce section class: '{sauce_section.get_attribute('class')}'")
        
        # Находим все ингредиенты в разделе
        sauce_ingredients = sauce_section.find_elements(By.XPATH, ".//a")
        print(f"Found {len(sauce_ingredients)} sauce ingredients")
        
        if not sauce_ingredients:
            # Пробуем альтернативный поиск
            sauce_ingredients = sauce_section.find_elements(By.XPATH, ".//div[contains(@class, 'ingredient')]")
            print(f"Found {len(sauce_ingredients)} sauce ingredients (alternative)")
        
        if not sauce_ingredients:
            pytest.fail("No sauce ingredients found")
        
        first_sauce = sauce_ingredients[0]
        print(f"First sauce class: '{first_sauce.get_attribute('class')}'")
        
        # Получаем начальный счётчик
        initial_counter = 0
        counters = first_sauce.find_elements(By.XPATH, ".//div[contains(@class, 'counter')]")
        print(f"Found {len(counters)} counters on ingredient")
        
        for counter in counters:
            counter_text = counter.text.strip()
            print(f"Counter text: '{counter_text}'")
            if counter_text and counter_text.isdigit():
                initial_counter = int(counter_text)
                break
        
        print(f"Initial counter: {initial_counter}")
        
        # Перетаскиваем (упрощённо)
        from selenium.webdriver import ActionChains
        
        # Находим зону конструктора
        constructor_areas = driver.find_elements(By.XPATH, "//section[contains(@class, 'constructor')] | //section[contains(@class, 'BurgerConstructor')]")
        print(f"Found {len(constructor_areas)} constructor areas")
        
        if constructor_areas:
            drop_zone = constructor_areas[0]
        else:
            drop_zone = driver.find_element(By.TAG_NAME, "body")
        
        # Выполняем перетаскивание
        actions = ActionChains(driver)
        actions.click_and_hold(first_sauce)
        actions.move_to_element(drop_zone)
        actions.release(drop_zone)
        actions.perform()
        
        print("Drag and drop performed")
        time.sleep(3)  # Ждём обновления
        
        # Проверяем счётчик после перетаскивания
        updated_counter = 0
        counters_after = first_sauce.find_elements(By.XPATH, ".//div[contains(@class, 'counter')]")
        print(f"Found {len(counters_after)} counters after drag")
        
        for counter in counters_after:
            counter_text = counter.text.strip()
            print(f"Counter after text: '{counter_text}'")
            if counter_text and counter_text.isdigit():
                updated_counter = int(counter_text)
                break
        
        print(f"Updated counter: {updated_counter}")
        
        # Проверяем результат
        assert updated_counter > initial_counter, (
            f"Counter didn't increase. Was: {initial_counter}, Now: {updated_counter}"
        )
        
        print("✓ Test passed! Counter increased successfully!")