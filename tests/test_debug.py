import allure
import time
from selenium.webdriver.common.by import By

@allure.feature('Отладка')
class TestDebug:
    
    def test_debug_page(self, driver):
        """Простой тест для отладки структуры страницы"""
        driver.get("https://stellarburgers.education-services.ru/")
        time.sleep(3)
        
        # Сохраняем HTML для анализа
        page_source = driver.page_source
        with open("debug_page.html", "w", encoding="utf-8") as f:
            f.write(page_source)
        
        # Ищем все элементы с классами
        elements = driver.find_elements(By.XPATH, "//*[@class]")
        classes = set()
        for element in elements[:100]:  # Первые 100 элементов
            class_name = element.get_attribute("class")
            if class_name:
                classes.add(class_name)
        
        print("Найденные классы:")
        for class_name in sorted(classes):
            print(f"  {class_name}")
        
        # Проверяем основные элементы
        nav_links = driver.find_elements(By.XPATH, "//a")
        print(f"\nНайдено ссылок: {len(nav_links)}")
        for link in nav_links[:5]:
            print(f"  Ссылка: {link.text} -> {link.get_attribute('href')}")
        
        assert True