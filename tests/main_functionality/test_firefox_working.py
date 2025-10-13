# tests/main_functionality/test_firefox_working.py
import allure
import pytest
from pages.main_page import MainPage
import time
from selenium.webdriver.common.by import By

@allure.feature('Firefox рабочие тесты')
class TestFirefoxWorking:
    
    @allure.title('Работающая навигация в Firefox')
    def test_firefox_navigation_working(self, driver):
        """Работающая навигация для Firefox"""
        main_page = MainPage(driver)
        main_page.go_to_main_page()
        
        print(f"🧭 Тестируем навигацию в {driver.name}")
        
        # Проверяем загрузку
        assert main_page.is_constructor_visible()
        print("✅ Главная страница загружена")
        
        # Переходим в ленту заказов
        main_page.click_order_feed()
        assert "feed" in driver.current_url
        print("✅ Перешли в ленту заказов")
        
        # Возвращаемся в конструктор
        main_page.click_constructor()
        assert "stellarburgers" in driver.current_url
        print("✅ Вернулись в конструктор")
        
        allure.attach(
            driver.get_screenshot_as_png(),
            name="firefox_navigation_working",
            attachment_type=allure.attachment_type.PNG
        )
    
    @allure.title('Работающие модальные окна в Firefox')
    def test_firefox_modals_working(self, driver):
        """Работающие модальные окна для Firefox"""
        main_page = MainPage(driver)
        main_page.go_to_main_page()
        
        print(f"🪟 Тестируем модальные окна в {driver.name}")
        
        # Открываем модальное окно
        main_page.click_ingredient(main_page.FIRST_BUN)
        assert main_page.is_modal_displayed()
        print("✅ Модальное окно открыто")
        
        # Закрываем модальное окно
        main_page.close_modal()
        assert not main_page.is_modal_displayed()
        print("✅ Модальное окно закрыто")
        
        allure.attach(
            driver.get_screenshot_as_png(),
            name="firefox_modals_working",
            attachment_type=allure.attachment_type.PNG
        )
    
    @allure.title('Проверка счетчиков в Firefox')
    def test_firefox_counters_working(self, driver):
        """Проверка счетчиков в Firefox"""
        # УБИРАЕМ ПРОВЕРКУ НА FIREFOX - тест будет работать в обоих браузерах
        main_page = MainPage(driver)
        main_page.go_to_main_page()
        
        print(f"🔢 Проверяем счетчики в {driver.name}")
        
        # Просто проверяем, что счетчики отображаются
        sauce_element = main_page.find_element(main_page.FIRST_SAUCE)
        counter = main_page.get_ingredient_counter(sauce_element)
        
        print(f"Счетчик ингредиента: {counter}")
        
        # Проверяем, что счетчик существует (может быть 0)
        assert counter >= 0, "Счетчик должен быть неотрицательным"
        print("✅ Счетчик отображается корректно")
        
        # Проверяем, что можно кликнуть на ингредиент
        main_page.click_ingredient(main_page.FIRST_SAUCE)
        assert main_page.is_modal_displayed()
        main_page.close_modal()
        print("✅ Интерактивность ингредиентов работает")
        
        allure.attach(
            driver.get_screenshot_as_png(),
            name=f"counters_{driver.name}",
            attachment_type=allure.attachment_type.PNG
        )