# tests/main_functionality/test_order_feed_navigation.py
import allure
import pytest
from pages.main_page import MainPage
from pages.order_feed_page import OrderFeedPage

@allure.feature('Основная функциональность')
@allure.story('Навигация ленты заказов')
class TestOrderFeedNavigation:
    
    @allure.title('Переход в ленту заказов из конструктора')
    def test_order_feed_navigation(self, driver):
        """Проверка перехода в ленту заказов по клику на кнопку"""
        main_page = MainPage(driver)
        main_page.go_to_main_page()
        
        # Переходим в ленту заказов
        main_page.click_order_feed()
        order_feed_page = OrderFeedPage(driver)
        
        # Проверяем, что перешли на страницу ленты заказов
        assert order_feed_page.is_order_feed_page()
        print("✅ Успешно перешли в ленту заказов")
        
        allure.attach(
            driver.get_screenshot_as_png(),
            name="order_feed_navigation",
            attachment_type=allure.attachment_type.PNG
        )