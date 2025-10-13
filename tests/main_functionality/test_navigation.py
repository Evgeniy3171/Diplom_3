import pytest
from pages.main_page import MainPage
from pages.order_feed_page import OrderFeedPage

class TestNavigation:
    
    @pytest.mark.main_functionality
    def test_constructor_navigation(self, driver):
        """Переход по клику на 'Конструктор'"""
        main_page = MainPage(driver)
        order_feed_page = OrderFeedPage(driver)
        
        # Переходим на страницу ленты заказов
        driver.get("https://stellarburgers.education-services.ru/feed")
        order_feed_page.wait_for_page_load()
        
        # Кликаем на конструктор
        main_page.click_constructor()
        
        # Проверяем, что находимся на главной странице
        assert "stellarburgers" in driver.current_url
        assert "feed" not in driver.current_url
        
        # Проверяем, что разделы ингредиентов загрузились
        main_page.wait_for_page_load()
    
    @pytest.mark.main_functionality
    def test_order_feed_navigation(self, driver):
        """Переход по клику на 'Лента заказов'"""
        main_page = MainPage(driver)
        order_feed_page = OrderFeedPage(driver)
        
        # Переходим на главную страницу
        driver.get("https://stellarburgers.education-services.ru/")
        main_page.wait_for_page_load()
        
        # Кликаем на ленту заказов
        main_page.click_order_feed()
        
        # Проверяем, что перешли на страницу ленты заказов
        order_feed_page.wait_for_page_load()
        assert "feed" in driver.current_url
        
        # Проверяем, что счётчики заказов отображаются
        total_orders = order_feed_page.get_total_orders_count()
        today_orders = order_feed_page.get_today_orders_count()
        
        assert total_orders >= 0
        assert today_orders >= 0