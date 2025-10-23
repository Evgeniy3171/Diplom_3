# run_tests.py
import os
import subprocess
import sys

def run_tests(browser="chrome", test_path="tests/"):
    """Запуск тестов с указанием браузера"""
    env = os.environ.copy()
    env["BROWSER"] = browser
    
    command = [
        "pytest", 
        test_path,
        "-v",
        "--tb=short",
        "--alluredir", f"allure-results-{browser}"
    ]
    
    print(f"🚀 Запуск тестов в браузере: {browser}")
    print(f"📋 Команда: {' '.join(command)}")
    
    result = subprocess.run(command, env=env)
    return result.returncode

if __name__ == "__main__":
    browser = sys.argv[1] if len(sys.argv) > 1 else "chrome"
    test_path = sys.argv[2] if len(sys.argv) > 2 else "tests/"
    
    exit_code = run_tests(browser, test_path)
    sys.exit(exit_code)