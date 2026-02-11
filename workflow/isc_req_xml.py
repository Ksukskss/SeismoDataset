import subprocess
import requests
import os
import argparse
import sys

SCRIPT_NAME = "isc_req_id.py"   
OUTPUT_DIR = "xml_data"

def run_search_script(start_date, end_date):
    """
    Запускает первый скрипт и парсит его вывод.
    Поддерживает форматы строк: "12345" и "evid=12345"
    """
    # Используем sys.executable для запуска того же python, что и текущий скрипт

    command = [sys.executable, SCRIPT_NAME, "-start_date", start_date, "-end_date", end_date]
    
    print(f"[Master] Запуск поиска через {SCRIPT_NAME}...")
    
    try:
        # capture_output=True перехватывает вывод в stdout
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        
        event_ids = []
        output_lines = result.stdout.splitlines()
        
        print(f"[Master] Получен ответ от {SCRIPT_NAME} (анализ строк)...")

        for line in output_lines:
            line = line.strip()
            
            
            current_id = None
            
            # 1. Если строка вида "evid=644275307"
            if "evid=" in line:
                parts = line.split("evid=")
                if len(parts) > 1:
                    candidate = parts[1].strip()
                    if candidate.isdigit():
                        current_id = candidate
            
            # 2. Если строка просто число "644275307"
            elif line.isdigit():
                current_id = line
            
            if current_id:
                event_ids.append(current_id)
                # print(f"  -> Найден ID: {current_id}") # Раскомментируйте для отладки
                
        return event_ids

    except subprocess.CalledProcessError as e:
        print(f"Ошибка при выполнении {SCRIPT_NAME}.")
        print("STDERR:", e.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print(f"Не найден файл {SCRIPT_NAME}. Проверьте, что он лежит в этой же папке.")
        sys.exit(1)

def download_event_xml(event_id):
    """Скачивает XML для конкретного event_id"""
    url = "https://www.isc.ac.uk/cgi-bin/web-db-run"
    params = {
        'event_id': event_id,
        'out_format': 'CATQuakeML',
        'request': 'COMPREHENSIVE'
    }
    
    # Создаем имя файла
    filename = os.path.join(OUTPUT_DIR, f"{event_id}.xml")
    
    # Если файл уже есть, можно пропустить (опционально)
    # if os.path.exists(filename):
    #     print(f"[Skip] Файл {filename} уже существует.")
    #     return

    try:
        print(f"[Download] Скачивание данных для ID {event_id}...")
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        
        with open(filename, "wb") as f:
            f.write(response.content)
            
        print(f"[OK] Сохранено: {filename}")
        
    except requests.exceptions.RequestException as e:
        print(f"[Error] Не удалось скачать ID {event_id}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Обертка для поиска и скачивания XML событий ISC.")
    parser.add_argument('-s', '--start_date', required=True, help='Дата начала')
    parser.add_argument('-e', '--end_date', required=True, help='Дата конца')
    
    args = parser.parse_args()
    
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    
    # 1. Получаем список ID
    ids = run_search_script(args.start_date, args.end_date)
    
    if not ids:
        print("[Master] ID событий не найдены (список пуст).")
        return

    print(f"[Master] Всего событий для обработки: {len(ids)}")
    
    # 2. Скачиваем XML для каждого
    for eid in ids:
        download_event_xml(eid)

    print("\n[Done] Работа завершена.")

if __name__ == "__main__":
    main()