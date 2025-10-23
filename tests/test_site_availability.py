import allure
import pytest
from pages.main_page import MainPage

@allure.feature('Доступность сайта')
class TestSiteAvailability:
    
    @allure.title('Проверка доступности главной страницы')
    def test_main_page_available(self, driver):
        """Проверка что главная страница доступна"""
        main_page = MainPage(driver)
        main_page.go_to_main_page()
        
        # Проверяем что страница загрузилась
        assert main_page.is_constructor_visible()
        
        # Проверяем что URL правильный
        current_url = main_page.get_current_url()
        expected_url = main_page.urls.MAIN_PAGE
        assert current_url == expected_url, f"Ожидался URL: {expected_url}, получен: {current_url}"