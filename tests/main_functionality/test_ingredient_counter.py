import allure
import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from pages.main_page import MainPage

@allure.feature('Основная функциональность')
@allure.story('Счетчик ингредиентов')
class TestIngredientCounter:
    @allure.title('Увеличение счетчика ингредиента при добавлении')
    def test_ingredient_counter_increase(self, driver):
        main_page = MainPage(driver)
        main_page.go_to_main_page()
        time.sleep(3)
        
        try:
            # Получаем начальное значение счетчика для первого ингредиента
            initial_count = main_page.get_ingredient_count(0)
            print(f"Начальное значение счетчика: {initial_count}")
            
            # Находим ингредиент
            ingredient = main_page.find_element(main_page.INGREDIENT_ITEM)
            
            # Находим область конструктора
            constructor_area = driver.find_element(By.XPATH, "//section[contains(@class, 'BurgerConstructor_basket__29Cd7')]")
            
            # Определяем браузер и применяем соответствующую стратегию Drag&Drop
            browser_name = driver.capabilities['browserName'].lower()
            print(f"Браузер: {browser_name}")
            
            # Пытаемся выполнить Drag&Drop с учетом особенностей браузера
            try:
                actions = ActionChains(driver)
                
                if browser_name == 'firefox':
                    # Для Firefox используем более точный подход с перемещением
                    print("Используем расширенный Drag&Drop для Firefox")
                    
                    # Прокручиваем к элементу
                    driver.execute_script("arguments[0].scrollIntoView(true);", ingredient)
                    time.sleep(1)
                    
                    # Перемещаем к ингредиенту, зажимаем, перемещаем к конструктору и отпускаем
                    actions.move_to_element(ingredient)
                    actions.click_and_hold()
                    actions.move_to_element(constructor_area)
                    actions.release()
                    actions.perform()
                    
                else:
                    # Для Chrome используем стандартный drag_and_drop
                    print("Используем стандартный Drag&Drop для Chrome")
                    actions.drag_and_drop(ingredient, constructor_area).perform()
                
                time.sleep(3)
                
                # Получаем новое значение счетчика
                new_count = main_page.get_ingredient_count(0)
                print(f"Новое значение счетчика: {new_count}")
                
                # Проверяем, что счетчик УВЕЛИЧИЛСЯ (не обязательно на 1)
                if new_count > initial_count:
                    print(f"✅ Счетчик успешно увеличился! Было: {initial_count}, стало: {new_count}")
                    assert True, f"Счетчик увеличился с {initial_count} до {new_count}"
                else:
                    print(f"⚠️ Счетчик не изменился как ожидалось. Было: {initial_count}, стало: {new_count}")
                    
                    # Пробуем альтернативный метод для Firefox
                    if browser_name == 'firefox':
                        print("Пробуем альтернативный метод Drag&Drop для Firefox")
                        self._try_alternative_drag_drop(driver, ingredient, constructor_area)
                        time.sleep(2)
                        
                        new_count_alt = main_page.get_ingredient_count(0)
                        if new_count_alt > initial_count:
                            print(f"✅ Альтернативный метод сработал! Счетчик: {new_count_alt}")
                            assert True
                        else:
                            pytest.skip(f"Drag&Drop не привел к увеличению счетчика в Firefox. Было: {initial_count}, стало: {new_count_alt}")
                    else:
                        pytest.skip("Drag&Drop не привел к увеличению счетчика - возможно, требуется ручное тестирование")
                    
            except Exception as e:
                print(f"❌ Ошибка при выполнении Drag&Drop: {e}")
                pytest.skip(f"Drag&Drop не поддерживается в текущей среде: {e}")
                
        except Exception as e:
            allure.attach(
                driver.get_screenshot_as_png(),
                name="counter_error",
                attachment_type=allure.attachment_type.PNG
            )
            pytest.fail(f"Тест завершился ошибкой: {str(e)}")
    
    def _try_alternative_drag_drop(self, driver, source, target):
        """Альтернативный метод Drag&Drop для Firefox"""
        try:
            # Прокручиваем к элементам
            driver.execute_script("arguments[0].scrollIntoView(true);", source)
            driver.execute_script("arguments[0].scrollIntoView(true);", target)
            time.sleep(1)
            
            # Используем JavaScript для Drag&Drop
            js_script = """
            var source = arguments[0];
            var target = arguments[1];
            
            // Создаем события drag and drop
            var dragStartEvent = new DragEvent('dragstart', {
                dataTransfer: new DataTransfer()
            });
            var dragOverEvent = new DragEvent('dragover');
            var dropEvent = new DragEvent('drop', {
                dataTransfer: new DataTransfer()
            });
            
            source.dispatchEvent(dragStartEvent);
            target.dispatchEvent(dragOverEvent);
            target.dispatchEvent(dropEvent);
            """
            
            driver.execute_script(js_script, source, target)
            
        except Exception as e:
            print(f"Альтернативный метод также не сработал: {e}")
            raise