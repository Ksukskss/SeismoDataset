import subprocess
import requests
import os
import argparse
import sys

HOME_DIR = os.path.expanduser("~")
OUTPUT_DIR = os.path.join(HOME_DIR, "Projects", "seismic_project", "data", "xml_files")
CURRENT_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SEARCH_SCRIPT_NAME = "isc_req_id.py"
SEARCH_SCRIPT_PATH = os.path.join(CURRENT_SCRIPT_DIR, SEARCH_SCRIPT_NAME)

def run_search_script(start_date, end_date):
    """
    Запускает первый скрипт и парсит его вывод.
    Ищет строки вида "evid=12345" или просто числа.
    """
    # Проверяем наличие первого скрипта
    if not os.path.exists(SEARCH_SCRIPT_PATH):
        print(f"[Error] Не найден файл поиска: {SEARCH_SCRIPT_PATH}")
        sys.exit(1)

    command = [sys.executable, SEARCH_SCRIPT_PATH, "-start_date", start_date, "-end_date", end_date]
    
    print(f"[Master] Запуск {SEARCH_SCRIPT_NAME}...")
    
    try:
        # Запускаем и перехватываем вывод
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        
        event_ids = []
        output_lines = result.stdout.splitlines()

        for line in output_lines:
            line = line.strip()
            current_id = None
            
            # Логика парсинга: ищем "evid=..." (поддерживаем варианты вроде "evid=307878.xml")
            if "evid=" in line:
                parts = line.split("evid=")
                # Берем правую часть после равно и чистим от расширения/мусора
                if len(parts) > 1:
                    candidate = parts[1].strip()
                    # например: "307878.xml" -> "307878"
                    candidate = os.path.splitext(candidate)[0]
                    if candidate.isdigit():
                        current_id = candidate
            
            # Или если строка целиком состоит из цифр
            elif line.isdigit():
                current_id = line
            
            if current_id:
                event_ids.append(current_id)
                
        return event_ids

    except subprocess.CalledProcessError as e:
        print(f"[Error] Ошибка выполнения скрипта поиска.")
        print("STDERR:", e.stderr)
        sys.exit(1)

def download_event_xml(event_id):
    """Скачивает XML и сохраняет в целевую папку"""
    url = "https://www.isc.ac.uk/cgi-bin/web-db-run"
    params = {
        'event_id': event_id,
        'out_format': 'CATQuakeML',
        'request': 'COMPREHENSIVE'
    }
    
    
    filename = os.path.join(OUTPUT_DIR, f"{event_id}.xml")
    
    try:
        print(f"[Download] ID {event_id} -> {filename}")
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        
        with open(filename, "wb") as f:
            f.write(response.content)
            
    except requests.exceptions.RequestException as e:
        print(f"[Error] Сбой загрузки ID {event_id}: {e}")
    except OSError as e:
        print(f"[Error] Ошибка записи файла {filename}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Скачивание XML событий ISC в папку project/xml_files")
    parser.add_argument('-s', '--start_date', required=True, help='Дата начала')
    parser.add_argument('-e', '--end_date', required=True, help='Дата конца')
    
    args = parser.parse_args()
    
    # Создаем папку, если её нет
    if not os.path.exists(OUTPUT_DIR):
        try:
            os.makedirs(OUTPUT_DIR)
            print(f"[Setup] Создана папка: {OUTPUT_DIR}")
        except OSError as e:
            print(f"[Error] Не удалось создать папку {OUTPUT_DIR}: {e}")
            sys.exit(1)
    
    # 1. Получаем ID
    ids = run_search_script(args.start_date, args.end_date)
    
    if not ids:
        print("[Master] Событий не найдено.")
        return

    print(f"[Master] Найдено {len(ids)} событий. Начинаем загрузку.")
    
    # 2. Скачиваем
    for eid in ids:
        download_event_xml(eid)

    print("\n[Done] Все файлы сохранены.")

if __name__ == "__main__":
    main()
