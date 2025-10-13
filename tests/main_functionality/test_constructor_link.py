# tests/main_functionality/test_constructor_link.py
import allure
import pytest
from pages.main_page import MainPage
from pages.order_feed_page import OrderFeedPage

@allure.feature('Основная функциональность')
@allure.story('Переход в конструктор')
class TestConstructorLink:
    
    @allure.title('Переход по клику на "Конструктор"')
    def test_go_to_constructor(self, driver):
        """Проверка перехода в конструктор из ленты заказов"""
        with allure.step("Переход на главную страницу"):
            main_page = MainPage(driver)
            main_page.go_to_main_page()
        
        with allure.step("Переход в ленту заказов"):
            main_page.click_order_feed()
            order_feed_page = OrderFeedPage(driver)
            assert "feed" in driver.current_url, "Не перешли в ленту заказов"
            print("✅ Успешно перешли в ленту заказов")
        
        with allure.step("Возврат в конструктор"):
            main_page.click_constructor()
            assert driver.current_url == "https://stellarburgers.education-services.ru/", "Не вернулись в конструктор"
            assert main_page.is_constructor_visible(), "Конструктор не отображается"
            print("✅ Успешно вернулись в конструктор")
        
        allure.attach(
            driver.get_screenshot_as_png(),
            name="constructor_navigation",
            attachment_type=allure.attachment_type.PNG
        )