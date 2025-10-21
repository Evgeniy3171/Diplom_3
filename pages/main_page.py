# pages/main_page.py
from .base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time

class MainPage(BasePage):
    # Навигация
    CONSTRUCTOR_BUTTON = (By.XPATH, "//a[contains(@href, '/')]")
    ORDER_FEED_BUTTON = (By.XPATH, "//a[contains(@href, '/feed')]")
    
    # Разделы ингредиентов
    BUN_SECTION = (By.XPATH, "//h2[text()='Булки']/..")
    SAUCE_SECTION = (By.XPATH, "//h2[text()='Соусы']/..")
    FILLING_SECTION = (By.XPATH, "//h2[text()='Начинки']/..")
    
    # Ингредиенты (упрощенные локаторы)
    FIRST_BUN = (By.XPATH, "(//h2[text()='Булки']/..//div[contains(@class, 'ingredient')])[1]")
    FIRST_SAUCE = (By.XPATH, "(//h2[text()='Соусы']/..//div[contains(@class, 'ingredient')])[1]")
    FIRST_FILLING = (By.XPATH, "(//h2[text()='Начинки']/..//div[contains(@class, 'ingredient')])[1]")
    
    # Счётчики ингредиентов
    INGREDIENT_COUNTER = (By.XPATH, ".//div[contains(@class, 'counter')]")
    
    # Конструктор (упрощенный локатор)
    CONSTRUCTOR_AREA = (By.XPATH, "//section[contains(@class, 'constructor') or contains(@class, 'Constructor')]")
    
    # Модальное окно
    MODAL_CONTENT = (By.XPATH, "//div[contains(@class, 'Modal_modal__') or contains(@class, 'modal')]")
    MODAL_CLOSE_BUTTON = (By.XPATH, "//button[contains(@class, 'Modal_modal__close') or contains(@class, 'close')]")
    
    # Кнопка оформления заказа
    ORDER_BUTTON = (By.XPATH, "//button[contains(text(), 'Оформить заказ')]")
    
    def go_to_main_page(self):
        """Переход на главную страницу"""
        self.driver.get("https://stellarburgers.education-services.ru/")
        self.wait_for_page_load()
    
    def wait_for_page_load(self, timeout=15):
        """Ожидание загрузки главной страницы"""
        try:
            # Ждем появления любого из ключевых элементов
            self.wait.until(EC.presence_of_element_located(self.BUN_SECTION))
            print("✓ Страница загружена успешно")
        except Exception as e:
            print(f"✗ Ошибка загрузки страницы: {e}")
            # Альтернативная проверка - ждем появления ингредиентов
            try:
                self.wait.until(EC.presence_of_element_located(self.FIRST_BUN))
                print("✓ Страница загружена (альтернативная проверка)")
            except:
                print("✗ Страница не загрузилась")
                # Делаем скриншот для отладки
                self.driver.save_screenshot("page_load_error.png")
                raise
    
    def click_constructor(self):
        """Клик на кнопку 'Конструктор'"""
        print("Кликаем на конструктор...")
        self.click(self.CONSTRUCTOR_BUTTON)
        self.wait_for_page_load()
    
    def click_order_feed(self):
        """Клик на кнопку 'Лента заказов'"""
        print("Кликаем на ленту заказов...")
        self.click(self.ORDER_FEED_BUTTON)
        from .order_feed_page import OrderFeedPage
        order_feed_page = OrderFeedPage(self.driver)
        order_feed_page.wait_for_page_load()
    
    def click_ingredient(self, ingredient_locator):
        """Клик на ингредиент для открытия модального окна"""
        print("Кликаем на ингредиент...")
        self.click(ingredient_locator)
        # Ждем появления модального окна
        time.sleep(2)
        assert self.is_modal_displayed(), "Модальное окно не открылось после клика на ингредиент"
        print("✓ Модальное окно открыто")
    
    def close_modal(self):
        """Закрытие модального окна"""
        print("Закрываем модальное окно...")
        self.click(self.MODAL_CLOSE_BUTTON)
        # Ждем исчезновения модального окна
        time.sleep(2)
        assert not self.is_modal_displayed(), "Модальное окно не закрылось"
        print("✓ Модальное окно закрыто")
    
    def is_modal_displayed(self):
        """Проверка отображения модального окна"""
        try:
            return self.find_element(self.MODAL_CONTENT).is_displayed()
        except:
            return False
    
    def get_ingredient_counter(self, ingredient_element):
        """Получение значения счётчика ингредиента"""
        try:
            counter_elements = ingredient_element.find_elements(*self.INGREDIENT_COUNTER)
            for element in counter_elements:
                counter_text = element.text.strip()
                if counter_text and counter_text.isdigit():
                    return int(counter_text)
            return 0
        except Exception as e:
            print(f"Ошибка получения счетчика: {e}")
            return 0
    
    def can_make_order(self):
        """Проверка возможности оформления заказа"""
        try:
            order_button = self.find_element(self.ORDER_BUTTON)
            return order_button.is_enabled()
        except:
            return False
    
    def is_constructor_visible(self):
        """Проверка видимости конструктора"""
        return self.is_element_visible(self.CONSTRUCTOR_AREA)
    
    def is_constructor_page(self):
        """Проверка, что находимся на странице конструктора"""
        return "stellarburgers.education-services.ru" in self.driver.current_url and "feed" not in self.driver.current_url