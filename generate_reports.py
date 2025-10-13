# generate_reports.py
import os
import subprocess
import webbrowser

def generate_html_reports():
    """Генерация HTML отчетов из Allure результатов"""
    browsers = ["chrome", "firefox"]
    
    print(f"\n{'='*60}")
    print("📊 ГЕНЕРАЦИЯ HTML ОТЧЕТОВ")
    print(f"{'='*60}")
    
    for browser in browsers:
        results_dir = f"allure-results-{browser}"
        report_dir = f"allure-report-{browser}"
        
        if os.path.exists(results_dir):
            print(f"\n🔧 Генерация отчета для {browser}...")
            
            # Генерируем HTML отчет
            result = subprocess.call([
                "allure", "generate",
                results_dir,
                "-o", report_dir,
                "--clean"
            ])
            
            if result == 0:
                print(f"✅ HTML отчет для {browser} создан: {report_dir}/index.html")
                
                # Автоматически открываем отчет в браузере
                report_path = os.path.abspath(f"{report_dir}/index.html")
                print(f"🌐 Открываю отчет в браузере...")
                webbrowser.open(f"file://{report_path}")
            else:
                print(f"❌ Ошибка генерации отчета для {browser}")
        else:
            print(f"⚠️  Нет результатов тестов для {browser}")
    
    print(f"\n{'='*60}")
    print("📋 РУКОВОДСТВО ПО ОТЧЕТАМ:")
    print("   - Allure отчеты содержат детальную информацию о тестах")
    print("   - Можно просматривать шаги, скриншоты, логи")
    print("   - Отчеты сохраняются в папках allure-report-*")
    print(f"{'='*60}")

if __name__ == "__main__":
    generate_html_reports()