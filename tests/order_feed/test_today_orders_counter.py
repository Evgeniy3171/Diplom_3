import allure
import pytest
from pages.order_feed_page import OrderFeedPage

@allure.feature('Лента заказов')
@allure.story('Счетчик выполненных заказов за сегодня')
class TestTodayOrdersCounter:
    
    @allure.title('Проверка отображения счетчика выполненных заказов за сегодня')
    def test_today_orders_counter_displayed(self, driver):
        """Проверка отображения счетчика за сегодня"""
        order_feed = OrderFeedPage(driver)
        driver.get("https://stellarburgers.education-services.ru/feed")
        order_feed.wait_for_page_load()
        
        today_orders = order_feed.get_today_orders_count()
        
        assert today_orders >= 0, "Счетчик за сегодня должен быть неотрицательным числом"
        print(f"✅ Заказов за сегодня: {today_orders}")
        