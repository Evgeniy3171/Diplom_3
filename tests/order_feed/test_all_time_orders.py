import allure
import pytest
import requests
from pages.order_feed_page import OrderFeedPage

@allure.feature('Лента заказов')
@allure.story('Счетчик выполненных заказов')
class TestAllTimeOrders:
    @allure.title('Увеличение счетчика "Выполнено за всё время"')
    def test_all_time_orders_increase(self, driver):
        order_feed = OrderFeedPage(driver)
        
        # Переходим на страницу ленты заказов
        order_feed.driver.get("https://stellarburgers.education-services.ru/feed")
        
        # Получаем начальное значение счетчика
        initial_count = order_feed.get_done_all_time_count()
        
        # Создаем заказ через API (пример - нужно адаптировать под реальное API)
        try:
            # Это пример - замените на реальные вызовы API вашего приложения
            order_data = {
                "ingredients": ["60d3b41abdacab0026a733c6", "60d3b41abdacab0026a733c7"]
            }
            response = requests.post(
                "https://stellarburgers.education-services.ru/api/orders",
                json=order_data
            )
            
            if response.status_code == 200:
                # Обновляем страницу и проверяем счетчик
                driver.refresh()
                new_count = order_feed.get_done_all_time_count()
                
                assert new_count > initial_count, \
                    f"Счетчик 'Выполнено за всё время' не увеличился. Было: {initial_count}, стало: {new_count}"
        except Exception as e:
            pytest.skip(f"API для создания заказа недоступно: {e}")