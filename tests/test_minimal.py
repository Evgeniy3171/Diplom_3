# tests/test_minimal.py
import pytest
from selenium.webdriver.common.by import By
import time

def test_minimal_page_load(driver):
    """Минимальный тест для проверки загрузки страницы"""
    driver.get("https://stellarburgers.education-services.ru/")
    time.sleep(3)
    
    # Просто проверяем, что страница загрузилась
    assert "Stellar Burgers" in driver.title or "бургер" in driver.title.lower()
    
    # Сохраняем скриншот
    driver.save_screenshot("page_loaded.png")
    print("✓ Страница успешно загружена")