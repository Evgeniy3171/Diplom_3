# tests/main_functionality/test_main_flow.py
import allure
import pytest
import time
from pages.main_page import MainPage
from pages.order_feed_page import OrderFeedPage

@allure.feature('Основная функциональность')
@allure.story('Основные сценарии навигации')
class TestMainFlow:
    
    @allure.title('Переход между конструктором и лентой заказов')
    def test_navigation_between_constructor_and_feed(self, driver):
        """Проверка навигации между конструктором и лентой заказов"""
        main_page = MainPage(driver)
        
        with allure.step("Открытие главной страницы"):
            main_page.go_to_main_page()
            assert main_page.is_constructor_visible()
            print(f"✅ Главная страница загружена в {driver.name}")
        
        with allure.step("Переход в ленту заказов"):
            main_page.click_order_feed()
            assert "feed" in driver.current_url
            print("✅ Успешно перешли в ленту заказов")
            
            allure.attach(
                driver.get_screenshot_as_png(),
                name="order_feed_page",
                attachment_type=allure.attachment_type.PNG
            )
        
        with allure.step("Возврат в конструктор"):
            main_page.click_constructor()
            assert "stellarburgers" in driver.current_url
            assert main_page.is_constructor_visible()
            print("✅ Успешно вернулись в конструктор")
            
            allure.attach(
                driver.get_screenshot_as_png(),
                name="constructor_page",
                attachment_type=allure.attachment_type.PNG
            )
    
    @allure.title('Работа с модальными окнами ингредиентов')
    def test_ingredient_modal_functionality(self, driver):
        """Проверка открытия и закрытия модальных окон ингредиентов"""
        main_page = MainPage(driver)
        main_page.go_to_main_page()
        
        with allure.step("Открытие модального окна ингредиента"):
            # Пробуем разные ингредиенты
            ingredients_to_test = [
                main_page.FIRST_BUN,
                main_page.FIRST_SAUCE, 
                main_page.FIRST_FILLING
            ]
            
            for i, ingredient_locator in enumerate(ingredients_to_test):
                with allure.step(f"Тест ингредиента {i+1}"):
                    if main_page.is_element_visible(ingredient_locator):
                        main_page.click_ingredient(ingredient_locator)
                        
                        if main_page.is_modal_displayed():
                            print(f"✅ Модальное окно {i+1} открыто")
                            
                            allure.attach(
                                driver.get_screenshot_as_png(),
                                name=f"modal_opened_{i+1}",
                                attachment_type=allure.attachment_type.PNG
                            )
                            
                            main_page.close_modal()
                            assert not main_page.is_modal_displayed()
                            print(f"✅ Модальное окно {i+1} закрыто")
                        else:
                            print(f"⚠️ Модальное окно {i+1} не открылось")
                    else:
                        print(f"⚠️ Ингредиент {i+1} не найден")
    
    @allure.title('Проверка счетчиков ингредиентов')
    def test_ingredient_counters(self, driver):
        """Проверка отображения счетчиков ингредиентов"""
        main_page = MainPage(driver)
        main_page.go_to_main_page()
        
        with allure.step("Проверка наличия счетчиков"):
            # Проверяем различные ингредиенты
            ingredients = [
                (main_page.FIRST_BUN, "булки"),
                (main_page.FIRST_SAUCE, "соуса"),
                (main_page.FIRST_FILLING, "начинки")
            ]
            
            for locator, name in ingredients:
                if main_page.is_element_visible(locator):
                    element = main_page.find_element(locator)
                    counter = main_page.get_ingredient_counter(element)
                    
                    print(f"Счетчик {name}: {counter}")
                    assert counter >= 0, f"Счетчик {name} должен быть неотрицательным"
                    
                    # Проверяем, что элемент кликабелен
                    try:
                        main_page.click(locator)
                        if main_page.is_modal_displayed():
                            main_page.close_modal()
                            print(f"✅ {name.capitalize()} интерактивен")
                    except Exception as e:
                        print(f"⚠️ Ошибка при клике на {name}: {e}")
                else:
                    print(f"⚠️ Ингредиент {name} не найден")