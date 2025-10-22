# pages/order_feed_page.py
import allure
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
    
    # Заголовок страницы
    PAGE_TITLE = (By.XPATH, "//h1[contains(text(), 'Лента заказов')]")
    
    @allure.step("Перейти на страницу ленты заказов")
    def go_to_order_feed(self):
        self.go_to_url(self.urls.ORDER_FEED)
        self.wait_for_page_load()
    
    @allure.step("Ожидать загрузки страницы ленты заказов")
    def wait_for_page_load(self):
        self.wait.until(EC.presence_of_element_located(self.PAGE_TITLE))
    
    @allure.step("Получить количество заказов за всё время")
    def get_total_orders_count(self):
        count_text = self.find_element(self.TOTAL_ORDERS).text
        return int(count_text) if count_text.strip().isdigit() else 0
    
    @allure.step("Получить количество заказов за сегодня")
    def get_today_orders_count(self):
        count_text = self.find_element(self.TODAY_ORDERS).text
        return int(count_text) if count_text.strip().isdigit() else 0
    
    @allure.step("Получить список заказов в работе")
    def get_orders_in_progress(self):
        try:
            section = self.find_element(self.ORDERS_IN_PROGRESS_SECTION)
            orders = section.find_elements(*self.ORDERS_IN_PROGRESS)
            return [order.text.strip() for order in orders if order.text.strip()]
        except Exception:
            return []
    
    @allure.step("Проверить что находимся на странице ленты заказов")
    def is_order_feed_page(self):
        current_url = self.get_current_url()
        return self.urls.ORDER_FEED in current_url and self.is_element_visible(self.PAGE_TITLE)