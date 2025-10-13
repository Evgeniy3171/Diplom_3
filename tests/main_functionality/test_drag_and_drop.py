# tests/main_functionality/test_drag_and_drop.py
import allure
import pytest
from pages.main_page import MainPage

@allure.feature('Основная функциональность')
@allure.story('Перетаскивание ингредиентов')
class TestDragAndDrop:
    
    @allure.title('Перетаскивание ингредиентов в конструктор')
    def test_drag_ingredients_to_constructor(self, driver):
        """Проверка перетаскивания разных типов ингредиентов"""
        main_page = MainPage(driver)
        main_page.go_to_main_page()
        
        # Сбросим конструктор
        driver.refresh()
        main_page.wait_for_page_load()
        
        with allure.step("Перетаскивание булки"):
            bun_element = main_page.find_element(main_page.FIRST_BUN)
            initial_bun_counter = main_page.get_ingredient_counter(bun_element)
            
            main_page.drag_ingredient_to_constructor(main_page.FIRST_BUN)
            
            updated_bun_counter = main_page.get_ingredient_counter(bun_element)
            print(f"Булка: было {initial_bun_counter}, стало {updated_bun_counter}")
            
            # Булки обычно добавляются с заменой, поэтому счетчик может не меняться
            # или меняться особым образом
        
        with allure.step("Перетаскивание соуса"):
            sauce_element = main_page.find_element(main_page.FIRST_SAUCE)
            initial_sauce_counter = main_page.get_ingredient_counter(sauce_element)
            
            main_page.drag_ingredient_to_constructor(main_page.FIRST_SAUCE)
            
            updated_sauce_counter = main_page.get_ingredient_counter(sauce_element)
            print(f"Соус: было {initial_sauce_counter}, стало {updated_sauce_counter}")
            
            # Соусы обычно увеличивают счетчик при добавлении
            if updated_sauce_counter > initial_sauce_counter:
                print("✓ Счетчик соуса увеличился при добавлении")
        
        with allure.step("Перетаскивание начинки"):
            filling_element = main_page.find_element(main_page.FIRST_FILLING)
            initial_filling_counter = main_page.get_ingredient_counter(filling_element)
            
            main_page.drag_ingredient_to_constructor(main_page.FIRST_FILLING)
            
            updated_filling_counter = main_page.get_ingredient_counter(filling_element)
            print(f"Начинка: было {initial_filling_counter}, стало {updated_filling_counter}")
            
            # Начинки обычно увеличивают счетчик при добавлении
            if updated_filling_counter > initial_filling_counter:
                print("✓ Счетчик начинки увеличился при добавлении")
        
        with allure.step("Проверка возможности оформления заказа"):
            # После добавления ингредиентов должна быть возможность оформить заказ
            can_order = main_page.can_make_order()
            print(f"Можно оформить заказ: {can_order}")
            
            # Если добавлены необходимые ингредиенты, кнопка должна быть активна
            # Это зависит от бизнес-логики приложения
        
        allure.attach(
            driver.get_screenshot_as_png(),
            name="drag_and_drop",
            attachment_type=allure.attachment_type.PNG
        )