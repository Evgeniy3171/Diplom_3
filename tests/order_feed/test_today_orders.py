import allure
import pytest
from pages.order_feed_page import OrderFeedPage

@allure.feature('Лента заказов')
@allure.story('Счетчик заказов за сегодня')
class TestTodayOrders:
    
    @allure.title('Проверка счетчика заказов за сегодня')
    def test_today_orders_counter(self, driver):
        """Проверка отображения счетчика заказов за сегодня"""
        with allure.step("Переход в ленту заказов"):
            order_feed = OrderFeedPage(driver)
            driver.get("https://stellarburgers.education-services.ru/feed")
            order_feed.wait_for_page_load()
        
        with allure.step("Проверка счетчика за сегодня"):
            today_orders = order_feed.get_today_orders_count()
            assert today_orders >= 0, "Счетчик за сегодня должен быть неотрицательным числом"
            print(f"✓ Заказов за сегодня: {today_orders}")
        