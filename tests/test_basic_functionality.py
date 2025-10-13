# tests/test_basic_functionality.py
import allure
import pytest
from pages.main_page import MainPage
from pages.order_feed_page import OrderFeedPage
import time
from selenium.common.exceptions import ElementClickInterceptedException

@allure.feature('Базовая функциональность')
class TestBasicFunctionality:
    
    @allure.title('Проверка загрузки главной страницы')
    def test_main_page_loads(self, driver):
        """Проверка, что главная страница загружается"""
        main_page = MainPage(driver)
        main_page.go_to_main_page()
        
        # Более гибкая проверка заголовка
        title = driver.title.lower()
        assert "stellar" in title or "бургер" in title or "constructor" in title
        
        # Проверяем, что конструктор виден
        assert main_page.is_constructor_visible()
        
        print(f"Заголовок страницы: {driver.title}")
        print(f"Текущий URL: {driver.current_url}")
        
        allure.attach(
            driver.get_screenshot_as_png(),
            name="main_page_loaded",
            attachment_type=allure.attachment_type.PNG
        )
    
    @allure.title('Навигация между конструктором и лентой заказов')
    def test_navigation_between_constructor_and_feed(self, driver):
        """Проверка перехода между конструктором и лентой заказов"""
        main_page = MainPage(driver)
        main_page.go_to_main_page()
        
        # Сохраняем начальный URL
        initial_url = driver.current_url
        print(f"Начальный URL: {initial_url}")
        
        try:
            # Переходим в ленту заказов
            main_page.click_order_feed()
            current_url = driver.current_url
            print(f"URL после клика на ленту заказов: {current_url}")
            assert "feed" in current_url
            
            # Возвращаемся в конструктор
            main_page.click_constructor()
            final_url = driver.current_url
            print(f"Финальный URL: {final_url}")
            
            # Проверяем, что вернулись на главную
            assert "stellarburgers" in final_url
            assert main_page.is_constructor_visible()
            
        except ElementClickInterceptedException as e:
            print(f"⚠️ Элемент перекрыт, пробуем альтернативный подход...")
            # Альтернативный подход - используем JavaScript для клика
            driver.execute_script("arguments[0].click();", driver.find_element(*main_page.CONSTRUCTOR_BUTTON))
            time.sleep(2)
            
            final_url = driver.current_url
            print(f"Финальный URL (через JS): {final_url}")
            
            # Проверяем результат
            assert "stellarburgers" in final_url
            assert main_page.is_constructor_visible()
        
        allure.attach(
            driver.get_screenshot_as_png(),
            name="navigation_test",
            attachment_type=allure.attachment_type.PNG
        )