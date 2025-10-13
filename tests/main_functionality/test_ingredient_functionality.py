# tests/main_functionality/test_ingredient_functionality.py
import allure
import pytest
from pages.main_page import MainPage
import time

@allure.feature('Основная функциональность')
@allure.story('Функциональность ингредиентов')
class TestIngredientFunctionality:
    
    @allure.title('Проверка отображения и взаимодействия с ингредиентами')
    def test_ingredient_display_and_interaction(self, driver):
        """Проверка отображения ингредиентов и базового взаимодействия"""
        main_page = MainPage(driver)
        main_page.go_to_main_page()
        
        print(f"🧪 Проверяем ингредиенты в {driver.name}")
        
        with allure.step("Проверка отображения разделов ингредиентов"):
            # Проверяем, что все разделы отображаются
            assert main_page.is_element_visible(main_page.BUN_SECTION)
            assert main_page.is_element_visible(main_page.SAUCE_SECTION)
            assert main_page.is_element_visible(main_page.FILLING_SECTION)
            print("✅ Все разделы ингредиентов отображаются")
        
        with allure.step("Проверка отображения ингредиентов"):
            # Проверяем, что ингредиенты отображаются
            bun = main_page.find_element(main_page.FIRST_BUN)
            sauce = main_page.find_element(main_page.FIRST_SAUCE)
            filling = main_page.find_element(main_page.FIRST_FILLING)
            
            assert bun.is_displayed()
            assert sauce.is_displayed()
            assert filling.is_displayed()
            print("✅ Все ингредиенты отображаются")
        
        with allure.step("Проверка счетчиков ингредиентов"):
            # Проверяем, что счетчики доступны для чтения
            bun_counter = main_page.get_ingredient_counter(bun)
            sauce_counter = main_page.get_ingredient_counter(sauce)
            filling_counter = main_page.get_ingredient_counter(filling)
            
            print(f"Счетчик булки: {bun_counter}")
            print(f"Счетчик соуса: {sauce_counter}")
            print(f"Счетчик начинки: {filling_counter}")
            
            # Счетчики должны быть неотрицательными числами
            assert bun_counter >= 0
            assert sauce_counter >= 0
            assert filling_counter >= 0
            print("✅ Счетчики ингредиентов отображаются корректно")
        
        with allure.step("Проверка модальных окон ингредиентов"):
            # Проверяем открытие модального окна для каждого типа ингредиента
            ingredients = [
                (main_page.FIRST_BUN, "булки"),
                (main_page.FIRST_SAUCE, "соуса"),
                (main_page.FIRST_FILLING, "начинки")
            ]
            
            for ingredient_locator, ingredient_name in ingredients:
                print(f"Проверяем модальное окно для {ingredient_name}...")
                main_page.click_ingredient(ingredient_locator)
                assert main_page.is_modal_displayed(), f"Модальное окно для {ingredient_name} не открылось"
                print(f"✅ Модальное окно для {ingredient_name} открылось")
                
                main_page.close_modal()
                assert not main_page.is_modal_displayed(), f"Модальное окно для {ingredient_name} не закрылось"
                print(f"✅ Модальное окно для {ingredient_name} закрылось")
        
        print(f"✅ Функциональность ингредиентов проверена в {driver.name}")
        
        allure.attach(
            driver.get_screenshot_as_png(),
            name=f"ingredient_functionality_{driver.name}",
            attachment_type=allure.attachment_type.PNG
        )