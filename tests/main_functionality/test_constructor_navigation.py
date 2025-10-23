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
        main_page = MainPage(driver)
        main_page.go_to_main_page()
        
        # Переходим в ленту заказов
        main_page.click_order_feed()
        order_feed_page = OrderFeedPage(driver)
        assert order_feed_page.is_order_feed_page()
        print("✅ Успешно перешли в ленту заказов")
        
        # Возвращаемся в конструктор
        main_page.click_constructor()
        assert main_page.is_constructor_page()
        assert main_page.is_constructor_visible()
        print("✅ Успешно вернулись в конструктор")
        
        