# check_architecture.py
import platform
import struct
import sys

print("🔍 Диагностика архитектуры:")
print(f"Операционная система: {platform.system()} {platform.release()}")
print(f"Архитектура ОС: {platform.architecture()}")
print(f"Версия Python: {platform.python_version()}")
print(f"Архитектура Python: {platform.architecture()[0]}")
print(f"Разрядность: {struct.calcsize('P') * 8}-битная")
print(f"Путь к Python: {sys.executable}")

# Проверка Chrome
import subprocess
try:
    result = subprocess.run(['reg', 'query', 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\App Paths\\chrome.exe'], 
                          capture_output=True, text=True)
    if result.returncode == 0:
        print("✅ Chrome найден в реестре")
    else:
        print("❌ Chrome не найден в реестре")
except:
    print("⚠️ Не удалось проверить Chrome в реестре")

# Проверка через where
try:
    result = subprocess.run(['where', 'chrome'], capture_output=True, text=True)
    if result.returncode == 0:
        print(f"✅ Chrome найден через where: {result.stdout.strip()}")
    else:
        print("❌ Chrome не найден через where")
except:
    print("⚠️ Не удалось выполнить where chrome")
    