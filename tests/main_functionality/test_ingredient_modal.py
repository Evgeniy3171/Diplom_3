import allure
import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.main_page import MainPage

@allure.feature('Основная функциональность')
@allure.story('Модальное окно ингредиента')
class TestIngredientModal:
    @allure.title('Открытие модального окна с деталями ингредиента')
    def test_ingredient_modal_open(self, driver):
        main_page = MainPage(driver)
        main_page.go_to_main_page()
        time.sleep(3)
        
        try:
            # Скриншот до клика
            allure.attach(
                driver.get_screenshot_as_png(),
                name="before_click",
                attachment_type=allure.attachment_type.PNG
            )
            
            # Кликаем на ингредиент
            main_page.click_ingredient()
            
            # Даем время на открытие модального окна
            time.sleep(3)
            
            # Скриншот после клика
            allure.attach(
                driver.get_screenshot_as_png(),
                name="after_click",
                attachment_type=allure.attachment_type.PNG
            )
            
            # Проверяем модальное окно несколькими способами
            modal_found = main_page.is_modal_visible()
            
            if not modal_found:
                # Дополнительная проверка - ищем любые видимые модальные окна
                modals = driver.find_elements(By.XPATH, "//*[contains(@class, 'modal') or contains(@class, 'Modal')]")
                visible_modals = [modal for modal in modals if modal.is_displayed()]
                
                if visible_modals:
                    print(f"✅ Найдено видимых модальных окон: {len(visible_modals)}")
                    modal_found = True
                    
                    for i, modal in enumerate(visible_modals):
                        print(f"  Модальное окно {i}: {modal.get_attribute('class')}")
            
            assert modal_found, "Модальное окно не открылось после клика на ингредиент"
            
            print("✅ Тест пройден: модальное окно успешно открылось")
            
            allure.attach(
                driver.get_screenshot_as_png(),
                name="modal_success",
                attachment_type=allure.attachment_type.PNG
            )
            
        except Exception as e:
            # Делаем скриншот при ошибке
            allure.attach(
                driver.get_screenshot_as_png(),
                name="error_state",
                attachment_type=allure.attachment_type.PNG
            )
            pytest.fail(f"Тест завершился ошибкой: {str(e)}")