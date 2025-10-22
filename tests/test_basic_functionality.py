# tests/test_basic_functionality.py
import allure
import pytest
from pages.main_page import MainPage
from pages.order_feed_page import OrderFeedPage

@allure.feature('Базовая функциональность')
class TestBasicFunctionality:
    
    @allure.title('Проверка загрузки главной страницы')
    def test_main_page_loads(self, driver):
        main_page = MainPage(driver)
        main_page.go_to_main_page()
        assert main_page.is_constructor_visible()
    
    @allure.title('Навигация между конструктором и лентой заказов')
    def test_navigation_between_constructor_and_feed(self, driver):
        main_page = MainPage(driver)
        order_feed_page = OrderFeedPage(driver)
        
        main_page.go_to_main_page()
        
        # Переходим в ленту заказов
        main_page.click_order_feed()
        order_feed_page.wait_for_page_load()
        assert order_feed_page.is_order_feed_page()
        
        # Возвращаемся в конструктор
        main_page.click_constructor()
        main_page.wait_for_page_load()
        assert main_page.is_constructor_page()