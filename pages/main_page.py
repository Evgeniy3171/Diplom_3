from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage
import time

class MainPage(BasePage):
    # Локаторы
    CONSTRUCTOR_TAB = (By.XPATH, "//a[@href='/']")
    ORDER_FEED_TAB = (By.XPATH, "//a[@href='/feed']")
    INGREDIENT_ITEM = (By.XPATH, "(//a[contains(@class, 'BurgerIngredient_ingredient__1TVf6')])[1]")
    MODAL_CLOSE_BUTTON = (By.XPATH, "//button[contains(@class, 'Modal_modal__close__TnseK')]")
    CONSTRUCTOR_TITLE = (By.XPATH, "//h1[text()='Соберите бургер']")

    def click_constructor_tab(self):
        self.click_element(self.CONSTRUCTOR_TAB)
        time.sleep(2)

    def click_order_feed_tab(self):
        self.click_element(self.ORDER_FEED_TAB)
        time.sleep(2)

    def click_ingredient(self):
        """Кликает на ингредиент"""
        self.wait_for_ingredients_load()
        
        ingredient = self.find_element_visible(self.INGREDIENT_ITEM)
        print(f"Кликаем на ингредиент: {ingredient.text}")
        ingredient.click()
        time.sleep(2)

    def close_modal(self):
        """Закрывает модальное окно"""
        close_button = self.find_element_visible(self.MODAL_CLOSE_BUTTON)
        close_button.click()
        time.sleep(2)

    def is_modal_visible(self):
        """Проверяет видимость модального окна - улучшенная версия"""
        try:
            # Пробуем несколько вариантов локаторов для модального окна
            modal_selectors = [
                "//section[contains(@class, 'Modal_modal_opened__3ISw4')]",
                "//section[contains(@class, 'Modal_modal__P3_V5') and contains(@class, 'opened')]",
                "//section[contains(@class, 'Modal_modal__P3_V5')]",
                "//div[contains(@class, 'Modal_modal__P3_V5')]",
                "//*[contains(@class, 'modal') and contains(@class, 'opened')]"
            ]
            
            for selector in modal_selectors:
                try:
                    modal = WebDriverWait(self.driver, 2).until(
                        EC.visibility_of_element_located((By.XPATH, selector))
                    )
                    if modal.is_displayed():
                        print(f"✅ Модальное окно найдено по селектору: {selector}")
                        return True
                except:
                    continue
            
            # Если не нашли по классам, ищем по содержимому
            content_selectors = [
                "//h2[contains(@class, 'Modal_modal__title__2L34m')]",
                "//*[contains(text(), 'идентификатор заказа')]",
                "//img[contains(@src, 'tick')]"
            ]
            
            for selector in content_selectors:
                try:
                    element = WebDriverWait(self.driver, 1).until(
                        EC.visibility_of_element_located((By.XPATH, selector))
                    )
                    if element.is_displayed():
                        print(f"✅ Контент модального окна найден: {selector}")
                        return True
                except:
                    continue
                    
            return False
            
        except Exception as e:
            print(f"❌ Ошибка при проверке модального окна: {e}")
            return False
    
    def wait_for_ingredients_load(self, timeout=10):
        """Ждет загрузки ингредиентов"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.XPATH, "//a[contains(@class, 'BurgerIngredient_ingredient__1TVf6')]"))
            )
        except Exception as e:
            print(f"Ингредиенты не загрузились: {e}")

    def is_constructor_visible(self):
        return self.is_element_visible(self.CONSTRUCTOR_TITLE)
    
    def get_ingredient_count(self, index=0):
        try:
            # Локатор для счетчика конкретного ингредиента
            count_locator = (By.XPATH, f"(//a[contains(@class, 'BurgerIngredient_ingredient__1TVf6')]//p[contains(@class, 'counter_counter__num__3nue1')])[{index + 1}]")
            count_text = self.get_text(count_locator)
            return int(count_text) if count_text and count_text.isdigit() else 0
        except:
            return 0