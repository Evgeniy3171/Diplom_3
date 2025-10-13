# tests/main_functionality/test_ingredient_modal.py
import allure
import pytest
from pages.main_page import MainPage

@allure.feature('Основная функциональность')
@allure.story('Модальное окно ингредиента')
class TestIngredientModal:
    
    @allure.title('Открытие и закрытие модального окна с деталями ингредиента')
    def test_ingredient_modal_open_close(self, driver):
        """Проверка открытия и закрытия модального окна"""
        with allure.step("Переход на главную страницу"):
            main_page = MainPage(driver)
            main_page.go_to_main_page()
        
        with allure.step("Открытие модального окна ингредиента"):
            main_page.click_ingredient(main_page.FIRST_BUN)
            assert main_page.is_modal_displayed(), "Модальное окно должно отображаться"
            print("✓ Модальное окно успешно открыто")
            
            allure.attach(
                driver.get_screenshot_as_png(),
                name="modal_opened",
                attachment_type=allure.attachment_type.PNG
            )
        
        with allure.step("Закрытие модального окна"):
            main_page.close_modal()
            assert not main_page.is_modal_displayed(), "Модальное окно должно закрыться"
            print("✓ Модальное окно успешно закрыто")
            
            allure.attach(
                driver.get_screenshot_as_png(),
                name="modal_closed",
                attachment_type=allure.attachment_type.PNG
            )
    
    @allure.title('Проверка модальных окон для разных типов ингредиентов')
    def test_different_ingredients_modals(self, driver):
        """Проверка модальных окон для булок, соусов и начинок"""
        main_page = MainPage(driver)
        main_page.go_to_main_page()
        
        # Проверяем для булки
        with allure.step("Проверка модального окна для булки"):
            main_page.click_ingredient(main_page.FIRST_BUN)
            assert main_page.is_modal_displayed()
            main_page.close_modal()
            print("✓ Модальное окно для булки работает")
        
        # Проверяем для соуса
        with allure.step("Проверка модального окна для соуса"):
            main_page.click_ingredient(main_page.FIRST_SAUCE)
            assert main_page.is_modal_displayed()
            main_page.close_modal()
            print("✓ Модальное окно для соуса работает")
        
        # Проверяем для начинки
        with allure.step("Проверка модального окна для начинки"):
            main_page.click_ingredient(main_page.FIRST_FILLING)
            assert main_page.is_modal_displayed()
            main_page.close_modal()
            print("✓ Модальное окна для начинки работает")