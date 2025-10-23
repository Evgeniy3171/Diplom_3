# tests/debug_order_feed.py
import allure
from selenium.webdriver.common.by import By

@allure.feature('Диагностика ленты заказов')
class TestDebugOrderFeed:
    
    @allure.title('Диагностика элементов ленты заказов')
    def test_debug_order_feed_elements(self, driver):
        """Диагностика какие элементы есть на странице ленты заказов"""
        driver.get("https://stellarburgers.education-services.ru/feed")
        
        print("🔍 Поиск элементов на странице ленты заказов:")
        
        # Ищем все элементы с текстом "заказ"
        order_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'заказ')]")
        print(f"Элементов с 'заказ': {len(order_elements)}")
        for elem in order_elements[:10]:  # Первые 10
            print(f"  - '{elem.text}'")
        
        # Ищем счетчики
        counters = driver.find_elements(By.XPATH, "//p/following-sibling::p")
        print(f"Счетчиков (p+p): {len(counters)}")
        for i, counter in enumerate(counters[:5]):
            print(f"  Счетчик {i+1}: '{counter.text}'")
        
        # Ищем заголовки
        headers = driver.find_elements(By.XPATH, "//h1 | //h2")
        print(f"Заголовков: {len(headers)}")
        for header in headers:
            print(f"  - '{header.text}'")
        
        # Сохраняем скриншот
        driver.save_screenshot("order_feed_debug.png")
        print("✅ Скриншот сохранен: order_feed_debug.png")
        
        # Сохраняем HTML
        with open("order_feed_page.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print("✅ HTML сохранен: order_feed_page.html")