# tests/main_functionality/test_constructor_navigation.py
import allure
import pytest
from pages.main_page import MainPage
from pages.order_feed_page import OrderFeedPage

@allure.feature('Основная функциональность')
@allure.story('Навигация конструктора')
class TestConstructorNavigation:
    
    @allure.title('Переход в конструктор из ленты заказов')
    def test_constructor_navigation(self, driver):
        """Проверка перехода в конструктор по клику на кнопку"""
        with allure.step("Переход на главную страницу"):
            main_page = MainPage(driver)
            main_page.go_to_main_page()
        
        with allure.step("Переход в ленту заказов"):
            main_page.click_order_feed()
            order_feed_page = OrderFeedPage(driver)
            assert "feed" in driver.current_url
            print("✓ Успешно перешли в ленту заказов")
        
        with allure.step("Возврат в конструктор"):
            main_page.click_constructor()
            assert "stellarburgers" in driver.current_url
            assert main_page.is_constructor_visible()
            print("✓ Успешно вернулись в конструктор")
        
        allure.attach(
            driver.get_screenshot_as_png(),
            name="constructor_navigation",
            attachment_type=allure.attachment_type.PNG
        )