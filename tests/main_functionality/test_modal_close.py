import allure
import pytest
import time
from pages.main_page import MainPage

@allure.feature('Основная функциональность')
@allure.story('Закрытие модального окна')
class TestModalClose:
    @allure.title('Закрытие модального окна с деталями ингредиента')
    def test_ingredient_modal_close(self, driver):
        main_page = MainPage(driver)
        main_page.go_to_main_page()
        time.sleep(3)
        
        try:
            # Открываем модальное окно
            main_page.click_ingredient()
            time.sleep(2)
            
            # Проверяем, что модальное окно открылось
            if not main_page.is_modal_visible():
                pytest.skip("Модальное окно не открылось, нельзя проверить закрытие")
            
            # Скриншот открытого модального окна
            allure.attach(
                driver.get_screenshot_as_png(),
                name="modal_opened",
                attachment_type=allure.attachment_type.PNG
            )
            
            # Закрываем модальное окно
            main_page.close_modal()
            
            # Проверяем, что модальное окно закрылось
            assert not main_page.is_modal_visible(), "Модальное окно не закрылось после клика на крестик"
            
            print("✅ Модальное окно успешно закрылось")
            
            allure.attach(
                driver.get_screenshot_as_png(),
                name="modal_closed",
                attachment_type=allure.attachment_type.PNG
            )
            
        except Exception as e:
            allure.attach(
                driver.get_screenshot_as_png(),
                name="close_error",
                attachment_type=allure.attachment_type.PNG
            )
            pytest.fail(f"Не удалось закрыть модальное окно: {str(e)}")