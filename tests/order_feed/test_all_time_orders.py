# tests/order_feed/test_all_time_orders.py
import allure
import pytest
from pages.order_feed_page import OrderFeedPage

@allure.feature('Лента заказов')
@allure.story('Счетчик выполненных заказов')
class TestAllTimeOrders:
    
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
            print(f"Заказов за все время: {total_orders}")
        
        allure.attach(
            driver.get_screenshot_as_png(),
            name="all_time_orders",
            attachment_type=allure.attachment_type.PNG
        )