# run_tests.py
import subprocess
import sys
import os

def run_tests():
    """Запуск тестов с разными браузерами и генерацией отчетов"""
    browsers = ["chrome", "firefox"]
    
    for browser in browsers:
        print(f"\n{'='*60}")
        print(f"🚀 Запуск тестов в {browser.upper()}")
        print(f"{'='*60}")
        
        # Создаем папку для результатов
        results_dir = f"allure-results-{browser}"
        if not os.path.exists(results_dir):
            os.makedirs(results_dir)
        
        # Запускаем pytest
        result = subprocess.call([
            "pytest", 
            "-v",
            "--browser", browser,
            "--alluredir", results_dir,
            "tests/",
            "-m", "not slow"  # Исключаем медленные тесты если есть
        ])
        
        if result == 0:
            print(f"✅ Тесты в {browser} завершены успешно")
        else:
            print(f"❌ Тесты в {browser} завершены с ошибками")
    
    print(f"\n{'='*60}")
    print("📊 Для просмотра отчетов выполните:")
    print("  allure serve allure-results-chrome")
    print("  allure serve allure-results-firefox")
    print(f"{'='*60}")

if __name__ == "__main__":
    run_tests()