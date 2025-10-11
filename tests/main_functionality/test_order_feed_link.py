import allure
import time
from pages.main_page import MainPage

@allure.feature('Основная функциональность')
@allure.story('Переход в ленту заказов')
class TestOrderFeedLink:
    @allure.title('Переход по клику на раздел "Лента заказов"')
    def test_go_to_order_feed(self, driver):
        main_page = MainPage(driver)
        main_page.go_to_main_page()
        time.sleep(3)
        
        # Переходим в ленту заказов
        main_page.click_order_feed_tab()
        time.sleep(2)
        
        # Проверяем, что перешли в ленту заказов
        assert "feed" in driver.current_url, "Не перешли в ленту заказов"
        
        allure.attach(
            driver.get_screenshot_as_png(),
            name="order_feed_page",
            attachment_type=allure.attachment_type.PNG
        )