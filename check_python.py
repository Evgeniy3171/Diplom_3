# check_python.py
import platform
import sys

print(f"Python version: {sys.version}")
print(f"Architecture: {platform.architecture()}")
print(f"Platform: {platform.platform()}")