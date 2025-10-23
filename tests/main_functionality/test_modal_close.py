import allure
import pytest
from pages.main_page import MainPage

@allure.feature('Основная функциональность')
@allure.story('Закрытие модального окна')
class TestModalClose:
    
    @allure.title('Закрытие модального окна с деталями ингредиента')
    def test_ingredient_modal_close(self, driver):
        with allure.step("Переход на главную страницу"):
            main_page = MainPage(driver)
            main_page.go_to_main_page()
        
        with allure.step("Открытие модального окна"):
            main_page.click_ingredient(main_page.FIRST_BUN)
            assert main_page.is_modal_displayed(), "Модальное окно должно отображаться"
                    
        with allure.step("Закрытие модального окна"):
            main_page.close_modal()
            assert not main_page.is_modal_displayed(), "Модальное окно должно закрыться"
            
            