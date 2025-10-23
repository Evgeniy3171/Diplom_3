import allure
import pytest
from pages.main_page import MainPage
from pages.order_feed_page import OrderFeedPage

@allure.feature('Основная функциональность')
@allure.story('Переход в конструктор')
class TestConstructorLink:
    
    @allure.title('Переход по клику на "Конструктор"')
    def test_go_to_constructor(self, driver):
        """Проверка перехода в конструктор из ленты заказов"""
        main_page = MainPage(driver)
        order_feed_page = OrderFeedPage(driver)
        
        with allure.step("Переход на главную страницу"):
            main_page.go_to_main_page()
        
        with allure.step("Переход в ленту заказов"):
            main_page.click_order_feed()
            order_feed_page.wait_for_page_load()
            assert order_feed_page.is_order_feed_page()
        
        with allure.step("Возврат в конструктор"):
            main_page.click_constructor()
            main_page.wait_for_page_load()
            assert main_page.is_constructor_page()
            assert main_page.is_constructor_visible()