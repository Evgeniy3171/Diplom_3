# tests/test_locators.py
import allure
import pytest
from selenium.webdriver.common.by import By
import time

@allure.feature('Проверка локаторов')
class TestLocators:
    
    @allure.title('Поиск основных элементов на странице')
    def test_find_main_elements(self, driver):
        """Поиск и проверка основных элементов на странице"""
        driver.get("https://stellarburgers.education-services.ru/")
        time.sleep(3)
        
        # Сохраняем HTML для отладки
        with open("page_source.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        
        print("Поиск элементов навигации:")
        nav_selectors = [
            "//a[@href='/']",
            "//a[@href='/feed']", 
            "//a[@href='/account']",
            "//a[contains(@class, 'AppHeader_header__link')]"
        ]
        
        for selector in nav_selectors:
            elements = driver.find_elements(By.XPATH, selector)
            print(f"  {selector}: {len(elements)} элементов")
            for elem in elements[:2]:  # Первые 2 элемента
                print(f"    - Текст: '{elem.text}', href: {elem.get_attribute('href')}")
        
        print("\nПоиск разделов ингредиентов:")
        section_selectors = [
            "//h2[contains(text(), 'Булки')]",
            "//h2[contains(text(), 'Соусы')]",
            "//h2[contains(text(), 'Начинки')]"
        ]
        
        for selector in section_selectors:
            elements = driver.find_elements(By.XPATH, selector)
            print(f"  {selector}: {len(elements)} элементов")
        
        print("\nПоиск ингредиентов:")
        ingredient_selectors = [
            "//h2[contains(text(), 'Булки')]/following::a[1]",
            "//h2[contains(text(), 'Соусы')]/following::a[1]",
            "//h2[contains(text(), 'Начинки')]/following::a[1]"
        ]
        
        for selector in ingredient_selectors:
            elements = driver.find_elements(By.XPATH, selector)
            print(f"  {selector}: {len(elements)} элементов")
        
        # Делаем скриншот
        driver.save_screenshot("locators_check.png")
        
        # Простая проверка - страница должна загрузиться
        assert len(driver.page_source) > 0
        
        allure.attach(
            driver.get_screenshot_as_png(),
            name="locators_check",
            attachment_type=allure.attachment_type.PNG
        )