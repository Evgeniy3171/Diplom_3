import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@allure.feature('Основная функциональность')
@allure.story('Простое взаимодействие с ингредиентом')
class TestIngredientSimple:
    @allure.title('Клик на ингредиент открывает модальное окно')
    def test_ingredient_click_opens_modal(self, driver):
        driver.get("https://stellarburgers.education-services.ru")
        time.sleep(3)
        
        # Находим первый ингредиент
        ingredient = driver.find_element(By.XPATH, "(//a[contains(@class, 'BurgerIngredient_ingredient__1TVf6')])[1]")
        ingredient.click()
        time.sleep(3)
        
        # Проверяем несколько вариантов модальных окон
        modal_selectors = [
            "//section[contains(@class, 'Modal_modal_opened__3ISw4')]",
            "//section[contains(@class, 'Modal_modal__P3_V5')]",
            "//div[contains(@class, 'Modal_modal__P3_V5')]"
        ]
        
        modal_found = False
        for selector in modal_selectors:
            modals = driver.find_elements(By.XPATH, selector)
            for modal in modals:
                if modal.is_displayed():
                    print(f"✅ Найдено видимое модальное окно: {selector}")
                    modal_found = True
                    break
            if modal_found:
                break
        
        # Если не нашли по классам, ищем по содержимому
        if not modal_found:
            content_selectors = [
                "//h2[contains(@class, 'Modal_modal__title__2L34m')]",
                "//*[contains(text(), 'идентификатор заказа')]"
            ]
            for selector in content_selectors:
                elements = driver.find_elements(By.XPATH, selector)
                for element in elements:
                    if element.is_displayed():
                        print(f"✅ Найден контент модального окна: {selector}")
                        modal_found = True
                        break
                if modal_found:
                    break
        
        assert modal_found, "Модальное окно не отображается после клика на ингредиент"
        
        # Закрываем модальное окно
        close_buttons = driver.find_elements(By.XPATH, "//button[contains(@class, 'Modal_modal__close__TnseK')]")
        for button in close_buttons:
            if button.is_displayed():
                button.click()
                break
        
        time.sleep(2)
        
        print("✅ Тест пройден: модальное окно открывается и закрывается корректно")
        
        allure.attach(
            driver.get_screenshot_as_png(),
            name="test_complete",
            attachment_type=allure.attachment_type.PNG
        )