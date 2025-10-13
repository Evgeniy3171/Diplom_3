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
            print(f"✓ Успешно перешли в ленту заказов в {driver.name}")
        
        with allure.step("Возврат в конструктор"):
            main_page.click_constructor()
            assert "stellarburgers" in driver.current_url
            assert main_page.is_constructor_visible()
            print(f"✓ Успешно вернулись в конструктор в {driver.name}")
        
        allure.attach(
            driver.get_screenshot_as_png(),
            name=f"constructor_navigation_{driver.name}",
            attachment_type=allure.attachment_type.PNG
        )