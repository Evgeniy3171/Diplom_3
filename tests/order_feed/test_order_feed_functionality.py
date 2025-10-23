# tests/order_feed/test_order_feed_functionality.py
import allure
import pytest
import time
from pages.order_feed_page import OrderFeedPage
from pages.main_page import MainPage

@allure.feature('Лента заказов')
@allure.story('Функциональность ленты заказов')
class TestOrderFeedFunctionality:
    
    @allure.title('Проверка счетчиков заказов')
    def test_order_counters(self, driver):
        """Проверка отображения счетчиков заказов"""
        order_feed = OrderFeedPage(driver)
        
        with allure.step("Переход в ленту заказов"):
            driver.get("https://stellarburgers.education-services.ru/feed")
            order_feed.wait_for_page_load()
        
        with allure.step("Проверка счетчика за все время"):
            total_orders = order_feed.get_total_orders_count()
            assert total_orders >= 0
            print(f"✅ Заказов за все время: {total_orders}")
            
            allure.attach(
                driver.get_screenshot_as_png(),
                name="total_orders_counter",
                attachment_type=allure.attachment_type.PNG
            )
        
        with allure.step("Проверка счетчика за сегодня"):
            today_orders = order_feed.get_today_orders_count()
            assert today_orders >= 0
            print(f"✅ Заказов за сегодня: {today_orders}")
            
            allure.attach(
                driver.get_screenshot_as_png(),
                name="today_orders_counter",
                attachment_type=allure.attachment_type.PNG
            )
    
    @allure.title('Проверка раздела "В работе"')
    def test_orders_in_progress(self, driver):
        """Проверка раздела с заказами в работе"""
        order_feed = OrderFeedPage(driver)
        
        with allure.step("Переход в ленту заказов"):
            driver.get("https://stellarburgers.education-services.ru/feed")
            order_feed.wait_for_page_load()
        
        with allure.step("Проверка раздела заказов в работе"):
            orders_in_progress = order_feed.get_orders_in_progress()
            print(f"Заказов в работе: {orders_in_progress}")
            
            # Раздел может быть пустым, но должен существовать
            assert orders_in_progress is not None
            print("✅ Раздел 'В работе' существует")
            
            allure.attach(
                driver.get_screenshot_as_png(),
                name="orders_in_progress",
                attachment_type=allure.attachment_type.PNG
            )