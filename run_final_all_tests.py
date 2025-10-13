# run_final_all_tests.py
import subprocess
import os
import time
from datetime import datetime

def run_final_all_tests():
    """Финальный запуск ВСЕХ тестов в обоих браузерах"""
    browsers = ["chrome", "firefox"]
    results = {}
    
    print(f"\n{'='*70}")
    print("🎯 ФИНАЛЬНЫЙ ЗАПУСК ВСЕХ ТЕСТОВ STELLAR BURGERS")
    print(f"{'='*70}")
    print(f"⏰ Время начала: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    for browser in browsers:
        print(f"\n🚀 Запуск ВСЕХ тестов в {browser.upper()}")
        print("-" * 50)
        
        # Создаем папку для результатов
        results_dir = f"allure-results-{browser}-final"
        if not os.path.exists(results_dir):
            os.makedirs(results_dir)
        
        # Запускаем ВСЕ тесты
        start_time = time.time()
        result = subprocess.call([
            "pytest", 
            "tests/",
            "--browser", browser,
            "--alluredir", results_dir,
            "-v",
            "--tb=short",
            "--strict-markers",
            "--color=yes"
        ])
        end_time = time.time()
        
        execution_time = end_time - start_time
        minutes = int(execution_time // 60)
        seconds = int(execution_time % 60)
        
        results[browser] = {
            'result': result,
            'time': execution_time,
            'results_dir': results_dir
        }
        
        if result == 0:
            print(f"✅ ВСЕ тесты в {browser} завершены УСПЕШНО!")
        else:
            print(f"❌ Тесты в {browser} завершены С ОШИБКАМИ")
        
        print(f"⏱️  Время выполнения: {minutes} мин {seconds} сек")
    
    # Итоговая статистика
    print(f"\n{'='*70}")
    print("📊 ФИНАЛЬНАЯ СТАТИСТИКА")
    print(f"{'='*70}")
    print(f"⏰ Время окончания: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    total_passed = sum(1 for r in results.values() if r['result'] == 0)
    total_failed = len(results) - total_passed
    
    print(f"✅ Успешных прогонов: {total_passed}/{len(browsers)}")
    print(f"❌ Неудачных прогонов: {total_failed}/{len(browsers)}")
    
    for browser, data in results.items():
        status = "✅ УСПЕХ" if data['result'] == 0 else "❌ ОШИБКИ"
        print(f"   {browser.upper()}: {status} ({data['time']:.1f} сек)")
    
    if total_failed == 0:
        print(f"\n🎉 ВСЕ ТЕСТЫ ВО ВСЕХ БРАУЗЕРАХ ПРОЙДЕНЫ УСПЕШНО!")
        print("   🏆 Проект тестирования завершен!")
    else:
        print(f"\n⚠️  Есть проблемы в {total_failed} браузере(ах)")
    
    print(f"\n📋 Для просмотра отчетов выполните:")
    for browser in browsers:
        print(f"   allure serve allure-results-{browser}-final")
    print(f"{'='*70}")

if __name__ == "__main__":
    run_final_all_tests()