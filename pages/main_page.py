# pages/main_page.py
import allure
from .base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class MainPage(BasePage):
    # Навигация
    CONSTRUCTOR_BUTTON = (By.XPATH, "//a[contains(@href, '/')]")
    ORDER_FEED_BUTTON = (By.XPATH, "//a[contains(@href, '/feed')]")
    
    # Разделы ингредиентов
    BUN_SECTION = (By.XPATH, "//h2[text()='Булки']/..")
    SAUCE_SECTION = (By.XPATH, "//h2[text()='Соусы']/..")
    FILLING_SECTION = (By.XPATH, "//h2[text()='Начинки']/..")
    
    # Ингредиенты
    FIRST_BUN = (By.XPATH, "(//h2[text()='Булки']/..//div[contains(@class, 'ingredient')])[1]")
    FIRST_SAUCE = (By.XPATH, "(//h2[text()='Соусы']/..//div[contains(@class, 'ingredient')])[1]")
    FIRST_FILLING = (By.XPATH, "(//h2[text()='Начинки']/..//div[contains(@class, 'ingredient')])[1]")
    
    # Счётчики ингредиентов
    INGREDIENT_COUNTER = (By.XPATH, ".//div[contains(@class, 'counter')]")
    
    # Конструктор
    CONSTRUCTOR_AREA = (By.XPATH, "//section[contains(@class, 'constructor') or contains(@class, 'Constructor')]")
    
    # Модальное окно
    MODAL_CONTENT = (By.XPATH, "//div[contains(@class, 'Modal_modal__') or contains(@class, 'modal')]")
    MODAL_CLOSE_BUTTON = (By.XPATH, "//button[contains(@class, 'Modal_modal__close') or contains(@class, 'close')]")
    
    # Кнопка оформления заказа
    ORDER_BUTTON = (By.XPATH, "//button[contains(text(), 'Оформить заказ')]")
    
    @allure.step("Перейти на главную страницу")
    def go_to_main_page(self):
        self.go_to_url(self.urls.MAIN_PAGE)
        self.wait_for_page_load()
    
    @allure.step("Ожидать загрузки главной страницы")
    def wait_for_page_load(self):
        self.wait.until(EC.presence_of_element_located(self.BUN_SECTION))
    
    @allure.step("Кликнуть на конструктор")
    def click_constructor(self):
        self.click(self.CONSTRUCTOR_BUTTON)
        self.wait_for_page_load()
    
    @allure.step("Кликнуть на ленту заказов")
    def click_order_feed(self):
        self.click(self.ORDER_FEED_BUTTON)
    
    @allure.step("Кликнуть на ингредиент")
    def click_ingredient(self, ingredient_locator):
        self.click(ingredient_locator)
        self.wait.until(EC.visibility_of_element_located(self.MODAL_CONTENT))
    
    @allure.step("Закрыть модальное окно")
    def close_modal(self):
        self.click(self.MODAL_CLOSE_BUTTON)
        self.wait_for_element_to_disappear(self.MODAL_CONTENT)
    
    @allure.step("Проверить отображение модального окна")
    def is_modal_displayed(self):
        return self.is_element_visible(self.MODAL_CONTENT)
    
    @allure.step("Получить значение счетчика ингредиента")
    def get_ingredient_counter(self, ingredient_element):
        try:
            counter_elements = ingredient_element.find_elements(*self.INGREDIENT_COUNTER)
            for element in counter_elements:
                counter_text = element.text.strip()
                if counter_text and counter_text.isdigit():
                    return int(counter_text)
            return 0
        except Exception:
            return 0
    
    @allure.step("Проверить возможность оформления заказа")
    def can_make_order(self):
        return self.is_element_visible(self.ORDER_BUTTON)
    
    @allure.step("Проверить видимость конструктора")
    def is_constructor_visible(self):
        return self.is_element_visible(self.CONSTRUCTOR_AREA)
    
    @allure.step("Проверить что находимся на странице конструктора")
    def is_constructor_page(self):
        current_url = self.get_current_url()
        return current_url == self.urls.MAIN_PAGE and self.is_constructor_visible()