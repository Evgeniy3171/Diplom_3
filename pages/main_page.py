from .base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
import time

class MainPage(BasePage):
    # Навигация - исправленные локаторы
    CONSTRUCTOR_BUTTON = (By.XPATH, "//a[@href='/'] | //a[contains(@class, 'AppHeader_header__link') and contains(@href, '/')]")
    ORDER_FEED_BUTTON = (By.XPATH, "//a[@href='/feed'] | //a[contains(@class, 'AppHeader_header__link') and contains(@href, 'feed')]")
    PERSONAL_ACCOUNT_BUTTON = (By.XPATH, "//a[@href='/account'] | //a[contains(@class, 'AppHeader_header__link') and contains(@href, 'account')]")
    
    # Разделы ингредиентов - более гибкие локаторы
    BUN_SECTION = (By.XPATH, "//h2[contains(text(), 'Булки')]/parent::div | //h2[contains(text(), 'Булки')]/..")
    SAUCE_SECTION = (By.XPATH, "//h2[contains(text(), 'Соусы')]/parent::div | //h2[contains(text(), 'Соусы')]/..")
    FILLING_SECTION = (By.XPATH, "//h2[contains(text(), 'Начинки')]/parent::div | //h2[contains(text(), 'Начинки')]/..")
    
    # Ингредиенты (первые в каждом разделе)
    FIRST_BUN = (By.XPATH, "(//h2[contains(text(), 'Булки')]/parent::div//a | //h2[contains(text(), 'Булки')]/..//a)[1]")
    FIRST_SAUCE = (By.XPATH, "(//h2[contains(text(), 'Соусы')]/parent::div//a | //h2[contains(text(), 'Соусы')]/..//a)[1]")
    FIRST_FILLING = (By.XPATH, "(//h2[contains(text(), 'Начинки')]/parent::div//a | //h2[contains(text(), 'Начинки')]/..//a)[1]")
    
    # Счётчики ингредиентов
    INGREDIENT_COUNTER = (By.XPATH, ".//div[contains(@class, 'counter')] | .//div[contains(@class, 'counter__num')]")
    
    # Конструктор
    CONSTRUCTOR_AREA = (By.XPATH, "//section[contains(@class, 'BurgerConstructor')] | //section[contains(@class, 'basket')]")
    CONSTRUCTOR_DROP_ZONE = (By.XPATH, "//div[contains(@class, 'BurgerConstructor_basket__list')] | //div[contains(@class, 'constructor-element__price')]/ancestor::section")
    
    # Модальное окно
    MODAL_OVERLAY = (By.XPATH, "//div[contains(@class, 'Modal_modal_overlay')] | //div[contains(@class, 'modal_overlay')]")
    MODAL_CONTENT = (By.XPATH, "//div[contains(@class, 'Modal_modal__')] | //div[contains(@class, 'modal_content')]")
    MODAL_CLOSE_BUTTON = (By.XPATH, "//button[contains(@class, 'Modal_modal__close')] | //button[contains(@class, 'modal_close')] | //div[contains(@class, 'close-icon')]")
    
    # Кнопка оформления заказа
    ORDER_BUTTON = (By.XPATH, "//button[contains(text(), 'Оформить заказ')]")
    
    # Логотип
    LOGO = (By.XPATH, "//div[contains(@class, 'AppHeader_header__logo')] | //div[contains(@class, 'logo')]")
    
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
            # Попробуем альтернативный подход - проверим наличие любого ингредиента
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
        self.wait.until(EC.visibility_of_element_located(self.MODAL_CONTENT))
        print("✓ Модальное окно открыто")
    
    def close_modal(self):
        """Закрытие модального окна"""
        print("Закрываем модальное окно...")
        self.click(self.MODAL_CLOSE_BUTTON)
        self.wait_for_element_to_disappear(self.MODAL_CONTENT)
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
    
    def drag_ingredient_to_constructor(self, ingredient_locator):
        """Перетаскивание ингредиента в конструктор"""
        print("Перетаскиваем ингредиент...")
        ingredient = self.find_element(ingredient_locator)
        
        # Пробуем разные локаторы для зоны сброса
        drop_zones = [
            self.CONSTRUCTOR_DROP_ZONE,
            (By.XPATH, "//div[contains(@class, 'constructor-element__price')]/ancestor::section"),
            (By.XPATH, "//section[contains(@class, 'BurgerConstructor')]")
        ]
        
        drop_zone = None
        for zone_locator in drop_zones:
            try:
                drop_zone = self.find_element(zone_locator)
                break
            except:
                continue
        
        if not drop_zone:
            raise Exception("Не найдена зона для перетаскивания")
        
        actions = ActionChains(self.driver)
        actions.drag_and_drop(ingredient, drop_zone).perform()
        time.sleep(2)
        print("✓ Ингредиент перетащен")
    
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