# tests/test_firefox_specific.py
import allure
import pytest

@allure.feature('Firefox специфичные тесты')
class TestFirefoxSpecific:
    
    @pytest.mark.skipif(True, reason="Firefox тесты временно отключены")
    @allure.title('Проверка работы Firefox драйвера')
    def test_firefox_driver_works(self, driver):
        """Проверка что Firefox драйвер работает"""
        # Этот тест будет пропущен пока мы не включим Firefox
        assert driver.name.lower() == "firefox"