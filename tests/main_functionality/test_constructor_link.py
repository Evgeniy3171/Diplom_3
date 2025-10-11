import allure
import time
from pages.main_page import MainPage

@allure.feature('Основная функциональность')
@allure.story('Переход в конструктор')
class TestConstructorLink:
    @allure.title('Переход по клику на "Конструктор"')
    def test_go_to_constructor(self, driver):
        main_page = MainPage(driver)
        main_page.go_to_main_page()
        time.sleep(3)
        
        # Переходим в ленту заказов
        main_page.click_order_feed_tab()
        time.sleep(2)
        
        # Проверяем, что перешли в ленту заказов
        assert "feed" in driver.current_url, "Не перешли в ленту заказов"
        
        # Возвращаемся в конструктор
        main_page.click_constructor_tab()
        time.sleep(2)
        
        # Проверяем, что вернулись на главную
        assert driver.current_url == "https://stellarburgers.education-services.ru/", "Не вернулись в конструктор"
        assert main_page.is_constructor_visible(), "Конструктор не отображается"
        
        allure.attach(
            driver.get_screenshot_as_png(),
            name="constructor_navigation",
            attachment_type=allure.attachment_type.PNG
        )