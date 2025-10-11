from selenium.webdriver.common.by import By
from .base_page import BasePage
import time

class OrderFeedPage(BasePage):
    # Локаторы для ленты заказов
    ORDER_FEED_HEADER = (By.XPATH, "//h1[contains(text(), 'Лента заказов')]")
    
    # Счетчики (на основе структуры, нужно уточнить при переходе на страницу)
    ORDERS_DONE_ALL_TIME = (By.XPATH, "//p[contains(text(), 'Выполнено за все время')]/following-sibling::p")
    ORDERS_DONE_TODAY = (By.XPATH, "//p[contains(text(), 'Выполнено за сегодня')]/following-sibling::p")
    
    def wait_for_feed_load(self, timeout=10):
        """Ждем загрузки ленты заказов"""
        self.find_element(self.ORDER_FEED_HEADER, timeout)

    def get_done_all_time_count(self):
        self.wait_for_feed_load()
        try:
            return int(self.get_text(self.ORDERS_DONE_ALL_TIME))
        except:
            return 0

    def get_done_today_count(self):
        self.wait_for_feed_load()
        try:
            return int(self.get_text(self.ORDERS_DONE_TODAY))
        except:
            return 0