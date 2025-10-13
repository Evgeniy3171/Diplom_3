# run_final_tests.py
import subprocess
import sys
import os
import time

def run_final_tests():
    """Финальный запуск всех тестов в обоих браузерах"""
    browsers = ["chrome", "firefox"]
    total_passed = 0
    total_failed = 0
    
    print(f"\n{'='*70}")
    print("🎯 ФИНАЛЬНЫЙ ЗАПУСК ТЕСТОВ STELLAR BURGERS")
    print(f"{'='*70}")
    
    for browser in browsers:
        print(f"\n🚀 Запуск тестов в {browser.upper()}")
        print("-" * 50)
        
        # Создаем папку для результатов
        results_dir = f"allure-results-{browser}"
        if not os.path.exists(results_dir):
            os.makedirs(results_dir)
        
        # Запускаем pytest
        start_time = time.time()
        result = subprocess.call([
            "pytest", 
            "-v",
            "--browser", browser,
            "--alluredir", results_dir,
            "tests/",
            "--tb=short",
            "--strict-markers",
            "--color=yes"
        ])
        end_time = time.time()
        
        execution_time = end_time - start_time
        minutes = int(execution_time // 60)
        seconds = int(execution_time % 60)
        
        if result == 0:
            print(f"✅ Тесты в {browser} завершены УСПЕШНО")
            total_passed += 1
        else:
            print(f"❌ Тесты в {browser} завершены С ОШИБКАМИ")
            total_failed += 1
        
        print(f"⏱️  Время выполнения: {minutes} мин {seconds} сек")
    
    # Итоговая статистика
    print(f"\n{'='*70}")
    print("📊 ИТОГОВАЯ СТАТИСТИКА")
    print(f"{'='*70}")
    print(f"✅ Успешных прогонов: {total_passed}/2")
    print(f"❌ Неудачных прогонов: {total_failed}/2")
    
    if total_failed == 0:
        print(f"\n🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
    else:
        print(f"\n⚠️  Есть проблемы в {total_failed} браузере(ах)")
    
    print(f"\n📋 Для просмотра отчетов выполните:")
    for browser in browsers:
        print(f"   allure serve allure-results-{browser}")
    print(f"{'='*70}")

if __name__ == "__main__":
    run_final_tests()