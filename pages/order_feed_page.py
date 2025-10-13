from .base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class OrderFeedPage(BasePage):
    # Счётчики заказов
    TOTAL_ORDERS = (By.XPATH, "//p[contains(text(), 'Выполнено за всё время')]/following-sibling::p")
    TODAY_ORDERS = (By.XPATH, "//p[contains(text(), 'Выполнено за сегодня')]/following-sibling::p")
    
    # Заказы в работе
    ORDERS_IN_PROGRESS_SECTION = (By.XPATH, "//ul[contains(@class, 'OrderFeed_orderListReady')]")
    ORDERS_IN_PROGRESS = (By.XPATH, ".//li")
    
    # Общий список заказов
    ORDERS_LIST = (By.XPATH, "//div[contains(@class, 'OrderFeed_orderList')]//a")
    
    # Заголовок страницы
    PAGE_TITLE = (By.XPATH, "//h1[contains(text(), 'Лента заказов')]")
    
    def wait_for_page_load(self, timeout=15):
        """Ожидание загрузки страницы ленты заказов"""
        try:
            self.wait.until(EC.presence_of_element_located(self.PAGE_TITLE))
            print("✓ Страница ленты заказов загружена")
        except Exception as e:
            print(f"✗ Ошибка загрузки ленты заказов: {e}")
            # Проверим альтернативные элементы
            try:
                self.wait.until(EC.presence_of_element_located(self.TOTAL_ORDERS))
                print("✓ Страница загружена (альтернативная проверка)")
            except:
                raise
    
    def get_total_orders_count(self):
        """Получение количества заказов за всё время"""
        try:
            count_text = self.find_element(self.TOTAL_ORDERS).text
            return int(count_text) if count_text.strip().isdigit() else 0
        except Exception as e:
            print(f"Ошибка получения общего количества заказов: {e}")
            return 0
    
    def get_today_orders_count(self):
        """Получение количества заказов за сегодня"""
        try:
            count_text = self.find_element(self.TODAY_ORDERS).text
            return int(count_text) if count_text.strip().isdigit() else 0
        except Exception as e:
            print(f"Ошибка получения количества заказов за сегодня: {e}")
            return 0
    
    def get_orders_in_progress(self):
        """Получение списка номеров заказов в работе"""
        try:
            section = self.find_element(self.ORDERS_IN_PROGRESS_SECTION)
            orders = section.find_elements(*self.ORDERS_IN_PROGRESS)
            return [order.text.strip() for order in orders if order.text.strip()]
        except Exception as e:
            print(f"Ошибка получения заказов в работе: {e}")
            return []
    
    # Добавляем отсутствующие методы
    def get_done_all_time_count(self):
        """Алиас для get_total_orders_count"""
        return self.get_total_orders_count()
    
    def get_done_today_count(self):
        """Алиас для get_today_orders_count"""
        return self.get_today_orders_count()