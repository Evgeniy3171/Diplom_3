import pytest
from utils.locator_helper import debug_locators

def test_debug_locators(driver):
    """Тест для отладки локаторов"""
    debug_locators(driver)