from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

def diagnose():
    print("Запуск диагностики...")
    
    options = Options()
    options.add_argument("--window-size=1920,1080")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        driver.get("https://stellarburgers.education-services.ru/")
        print("✓ Страница загружена")
        
        # Ищем ключевые элементы
        selectors = [
            "//a[@href='/']",
            "//a[@href='/feed']", 
            "//h2[contains(text(), 'Булки')]",
            "//h2[contains(text(), 'Соусы')]",
            "//h2[contains(text(), 'Начинки')]",
            "//button[contains(text(), 'Оформить заказ')]"
        ]
        
        for selector in selectors:
            elements = driver.find_elements("xpath", selector)
            print(f"{selector}: найдено {len(elements)} элементов")
            if elements:
                print(f"  Текст: {elements[0].text}")
        
    finally:
        driver.quit()

if __name__ == "__main__":
    diagnose()