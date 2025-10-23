# tests/test_driver_diagnostic.py
import allure
import pytest

@allure.feature('Диагностика драйверов')
class TestDriverDiagnostic:
    
    @allure.title('Проверка работы Chrome драйвера')
    def test_chrome_driver_works(self, driver):
        """Проверка что Chrome драйвер работает"""
        print(f"🔍 Проверяем драйвер: {driver.name}")
        
        # Проверяем базовую функциональность
        assert driver is not None
        assert driver.name.lower() == "chrome"
        
        # Открываем тестовую страницу
        test_url = "https://stellarburgers.education-services.ru/"
        driver.get(test_url)
        
        # Проверяем что страница загрузилась
        assert "stellarburgers" in driver.current_url
        assert driver.title is not None
        
        print(f"✅ Драйвер {driver.name} работает корректно")
        print(f"📄 Заголовок страницы: {driver.title}")
        print(f"🌐 Текущий URL: {driver.current_url}")
        
        # Проверяем основные элементы
        page_source = driver.page_source
        required_elements = ["Конструктор", "Лента заказов", "Булки"]
        found_elements = [elem for elem in required_elements if elem in page_source]
        
        print(f"📊 Найдено элементов: {len(found_elements)}/{len(required_elements)}")
        for elem in found_elements:
            print(f"   ✅ {elem}")
        
        # Делаем скриншот для отчета
        allure.attach(
            driver.get_screenshot_as_png(),
            name="chrome_driver_working",
            attachment_type=allure.attachment_type.PNG
        )
    
    @allure.title('Проверка типа браузера')
    def test_browser_type(self, driver, request):
        """Проверка что используется правильный браузер"""
        browser_name = request.config.getoption("--browser").lower()
        print(f"🔧 Ожидаемый браузер: {browser_name}")
        print(f"🔧 Фактический драйвер: {driver.name}")
        
        # Проверяем соответствие
        assert driver.name.lower() == browser_name, f"Ожидался {browser_name}, получен: {driver.name}"
        print(f"✅ Браузер соответствует ожидаемому: {browser_name}")