import allure
import pytest
from pages.order_feed_page import OrderFeedPage

@allure.feature('Лента заказов')
@allure.story('Счетчик выполненных заказов за все время')
class TestTotalOrdersCounter:
    
    @allure.title('Проверка отображения счетчика выполненных заказов за все время')
    def test_total_orders_counter_displayed(self, driver):
        """Проверка отображения счетчика за все время"""
        order_feed = OrderFeedPage(driver)
        driver.get("https://stellarburgers.education-services.ru/feed")
        order_feed.wait_for_page_load()
        
        total_orders = order_feed.get_total_orders_count()
        
        assert total_orders >= 0, "Счетчик за все время должен быть неотрицательным числом"
        print(f"✅ Заказов за все время: {total_orders}")
        