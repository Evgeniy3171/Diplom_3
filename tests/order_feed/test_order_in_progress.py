import allure
import pytest
from pages.order_feed_page import OrderFeedPage

@allure.feature('Лента заказов')
@allure.story('Заказы в работе')
class TestOrderInProgress:
    
    @allure.title('Проверка раздела "В работе"')
    def test_order_in_progress_section_exists(self, driver):
        """Проверка наличия раздела с заказами в работе"""
        with allure.step("Переход в ленту заказов"):
            order_feed = OrderFeedPage(driver)
            driver.get("https://stellarburgers.education-services.ru/feed")
            order_feed.wait_for_page_load()
        
        with allure.step("Проверка раздела 'В работе'"):
            orders_in_progress = order_feed.get_orders_in_progress()
            print(f"Заказов в работе: {orders_in_progress}")
            
            # Проверяем, что раздел существует (может быть пустым)
            assert orders_in_progress is not None, "Раздел 'В работе' должен существовать"
        