# run_chrome_tests.py
import os
import pytest

if __name__ == "__main__":
    # Устанавливаем переменную окружения
    os.environ["BROWSER"] = "chrome"
    
    # Запускаем pytest напрямую
    pytest.main([
        "tests/test_driver_diagnostic.py", 
        "-v",
        "--tb=short"
    ])