# tests/order_feed/test_order_feed_counters.py
import allure
import pytest
from pages.order_feed_page import OrderFeedPage

@allure.feature('Лента заказов')
@allure.story('Счетчики заказов')
class TestOrderFeedCounters:
    
    @allure.title('Проверка отображения счетчика "Выполнено за всё время"')
    def test_all_time_orders_displayed(self, driver):
        """Проверка, что счетчик за все время отображается и содержит число"""
        with allure.step("Переход в ленту заказов"):
            order_feed = OrderFeedPage(driver)
            driver.get("https://stellarburgers.education-services.ru/feed")
            order_feed.wait_for_page_load()
        
        with allure.step("Проверка счетчика за все время"):
            total_orders = order_feed.get_total_orders_count()
            assert total_orders >= 0, "Счетчик за все время должен быть неотрицательным числом"
            print(f"✓ Заказов за все время: {total_orders}")
        
        allure.attach(
            driver.get_screenshot_as_png(),
            name="all_time_orders",
            attachment_type=allure.attachment_type.PNG
        )
    
    @allure.title('Проверка отображения счетчика "Выполнено за сегодня"')
    def test_today_orders_displayed(self, driver):
        """Проверка, что счетчик за сегодня отображается и содержит число"""
        with allure.step("Переход в ленту заказов"):
            order_feed = OrderFeedPage(driver)
            driver.get("https://stellarburgers.education-services.ru/feed")
            order_feed.wait_for_page_load()
        
        with allure.step("Проверка счетчика за сегодня"):
            today_orders = order_feed.get_today_orders_count()
            assert today_orders >= 0, "Счетчик за сегодня должен быть неотрицательным числом"
            print(f"✓ Заказов за сегодня: {today_orders}")
        
        allure.attach(
            driver.get_screenshot_as_png(),
            name="today_orders",
            attachment_type=allure.attachment_type.PNG
        )