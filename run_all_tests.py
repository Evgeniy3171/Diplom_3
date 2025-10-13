# run_all_tests.py
import subprocess
import sys
import os

def run_tests():
    """Запуск всех тестов с разными браузерами и генерацией отчетов"""
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
            "--tb=short"  # Короткий traceback для лучшей читаемости
        ])
        
        if result == 0:
            print(f"✅ Тесты в {browser} завершены успешно")
        else:
            print(f"❌ Тесты в {browser} завершены с ошибками")
            # Не выходим сразу, чтобы протестировать оба браузера
    
    print(f"\n{'='*60}")
    print("📊 Отчеты сгенерированы. Для просмотра выполните:")
    for browser in browsers:
        print(f"  allure serve allure-results-{browser}")
    print(f"{'='*60}")

if __name__ == "__main__":
    run_tests()