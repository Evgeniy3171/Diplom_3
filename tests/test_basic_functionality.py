# tests/test_basic_functionality.py
import allure
import pytest
from pages.main_page import MainPage
from pages.order_feed_page import OrderFeedPage

@allure.feature('Базовая функциональность')
class TestBasicFunctionality:
    
    @allure.title('Проверка загрузки главной страницы')
    def test_main_page_loads(self, driver):
        """Проверка, что главная страница загружается"""
        main_page = MainPage(driver)
        main_page.go_to_main_page()
        
        # Проверяем, что конструктор виден
        assert main_page.is_constructor_visible()
        
        print(f"Заголовок страницы: {driver.title}")
        print(f"Текущий URL: {driver.current_url}")
        
        allure.attach(
            driver.get_screenshot_as_png(),
            name="main_page_loaded",
            attachment_type=allure.attachment_type.PNG
        )
    
    @allure.title('Навигация между конструктором и лентой заказов')
    def test_navigation_between_constructor_and_feed(self, driver):
        """Проверка перехода между конструктором и лентой заказов"""
        main_page = MainPage(driver)
        main_page.go_to_main_page()
        
        # Переходим в ленту заказов
        main_page.click_order_feed()
        order_feed_page = OrderFeedPage(driver)
        
        # Проверяем, что перешли на страницу ленты заказов
        assert order_feed_page.is_order_feed_page()
        print("✅ Успешно перешли в ленту заказов")
        
        # Возвращаемся в конструктор
        main_page.click_constructor()
        
        # Проверяем, что вернулись в конструктор
        assert main_page.is_constructor_page()
        assert main_page.is_constructor_visible()
        print("✅ Успешно вернулись в конструктор")
        
        allure.attach(
            driver.get_screenshot_as_png(),
            name="navigation_test",
            attachment_type=allure.attachment_type.PNG
        )