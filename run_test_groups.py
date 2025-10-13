# run_test_groups.py
import subprocess
import sys

def run_main_functionality_tests(browser="chrome"):
    """Запуск тестов основной функциональности"""
    print(f"\n🔧 Запуск тестов основной функциональности в {browser}")
    
    result = subprocess.call([
        "pytest",
        "-v",
        "--browser", browser,
        "--alluredir", f"allure-results-main-{browser}",
        "tests/main_functionality/",
        "-m", "main_functionality"
    ])
    
    return result

def run_order_feed_tests(browser="chrome"):
    """Запуск тестов ленты заказов"""
    print(f"\n📋 Запуск тестов ленты заказов в {browser}")
    
    result = subprocess.call([
        "pytest", 
        "-v",
        "--browser", browser,
        "--alluredir", f"allure-results-feed-{browser}",
        "tests/order_feed/",
        "-m", "order_feed"
    ])
    
    return result

if __name__ == "__main__":
    browser = sys.argv[1] if len(sys.argv) > 1 else "chrome"
    
    print(f"🎯 Запуск тестов в {browser.upper()}")
    
    # Запускаем группы тестов
    run_main_functionality_tests(browser)
    run_order_feed_tests(browser)
    
    print(f"\n📊 Для просмотра отчетов выполните:")
    print(f"  allure serve allure-results-main-{browser}")
    print(f"  allure serve allure-results-feed-{browser}")