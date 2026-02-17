import os
import glob
import time
import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

# --- КОНФИГУРАЦИЯ ---
BASE_PATH = "/home/ksukskss/Projects/seismic_project/data/ALL_MOY_and_OPTI_2025_MAJ_till_31122023/"
ISC_URL = "https://www.isc.ac.uk/cgi-bin/web-db-run"

# Задержка между запросами, чтобы не заблокировали IP (вежливость к серверу)
REQUEST_DELAY = 1.0 

def parse_fct_file(filepath):
    """Считывает дату, время и координаты из файла."""
    try:
        with open(filepath, 'r') as f:
            line = f.readline()
            parts = line.split()
            if len(parts) < 8:
                return None
            
            year, month, day = int(parts[0]), int(parts[1]), int(parts[2])
            hour, minute = int(parts[3]), int(parts[4])
            seconds_float = float(parts[5])
            lat, lon = float(parts[6]), float(parts[7])
            
            sec = int(seconds_float)
            microsec = int((seconds_float - sec) * 1_000_000)
            dt = datetime(year, month, day, hour, minute, sec, microsec)
            
            return dt, lat, lon
    except Exception as e:
        print(f"[ERROR] Ошибка чтения {filepath}: {e}")
        return None

def search_event_ids(dt, lat, lon):
    """
    Шаг 1: Поиск event_id по параметрам времени и места.
    Возвращает список найденных ID.
    """
    start_dt = dt - timedelta(seconds=1)
    end_dt = dt + timedelta(seconds=1)
    
    params = {
        'request': 'COMPREHENSIVE',
        'out_format': 'CATQuakeML',
        'searchshape': 'RECT',
        'bot_lat': lat - 1.0,
        'top_lat': lat + 1.0,
        'left_lon': lon - 1.0,
        'right_lon': lon + 1.0,
        'start_year': start_dt.year,
        'start_month': start_dt.month,
        'start_day': start_dt.day,
        'start_time': start_dt.strftime('%H:%M:%S'),
        'end_year': end_dt.year,
        'end_month': end_dt.month,
        'end_day': end_dt.day,
        'end_time': end_dt.strftime('%H:%M:%S'),
        'min_mag': 5,
        'include_links': 'on' # Нужно для получения ID
    }
    
    try:
        response = requests.get(ISC_URL, params=params, timeout=30)
        response.raise_for_status()
        
        # Парсинг XML для поиска ID
        root = ET.fromstring(response.content)
        events = root.findall('.//{*}event')
        
        found_ids = []
        for event in events:
            public_id = event.get('publicID')
            if public_id:
                # publicID: "smi:isc.ac.uk/event/636373471" -> берем 636373471
                eid = public_id.split('/')[-1]
                found_ids.append(eid)
        
        return list(set(found_ids)) # Убираем дубликаты, если есть

    except Exception as e:
        print(f"[SEARCH ERROR] Не удалось найти события: {e}")
        return []

def download_isc_xml(event_id, output_folder):
    """
    Шаг 2: Скачивание XML для конкретного event_id и сохранение в папку.
    """
    params = {
        'event_id': event_id,
        'out_format': 'CATQuakeML',
        'request': 'COMPREHENSIVE'
    }
    
    save_path = os.path.join(output_folder, f"{event_id}.xml")
    
    # Если файл уже есть, пропускаем (чтобы экономить время при повторном запуске)
    if os.path.exists(save_path):
        print(f"   [SKIP] Файл уже существует: {os.path.basename(save_path)}")
        return

    try:
        print(f"   [DOWNLOADING] Скачивание данных для ID {event_id}...")
        response = requests.get(ISC_URL, params=params, timeout=60)
        response.raise_for_status()
        
        # Проверка, что пришел валидный XML
        if b"No events were found" in response.content:
            print(f"   [WARN] ISC вернул пустой ответ для ID {event_id}")
            return

        with open(save_path, 'wb') as f:
            f.write(response.content)
        
        print(f"   [OK] Сохранено: {os.path.basename(save_path)}")
        
    except Exception as e:
        print(f"   [DOWNLOAD ERROR] Ошибка при скачивании ID {event_id}: {e}")

def main():
    if not os.path.exists(BASE_PATH):
        print(f"Путь не найден: {BASE_PATH}")
        return

    # Ищем папки FCTs
    dirs = [d for d in os.listdir(BASE_PATH) if os.path.isdir(os.path.join(BASE_PATH, d)) and d.startswith("FCTs_")]
    dirs.sort()

    print(f"Найдено папок: {len(dirs)}")
    
    for i, folder in enumerate(dirs, 1):
        folder_path = os.path.join(BASE_PATH, folder)
        print(f"\nProcessing {i}/{len(dirs)}: {folder}")
        
        # 1. Поиск файла fctoptsource
        search_pattern = os.path.join(folder_path, "fctoptsource*")
        files = glob.glob(search_pattern)
        
        if not files:
            print("   [SKIP] Файл данных не найден внутри папки.")
            continue
            
        # 2. Парсинг параметров
        result = parse_fct_file(files[0])
        if not result:
            continue
        dt, lat, lon = result
        
        # 3. Поиск event_id (Поисковой запрос)
        event_ids = search_event_ids(dt, lat, lon)
        
        if not event_ids:
            print("   [INFO] События не найдены в каталоге ISC.")
            continue
        
        print(f"   Найдено ID: {event_ids}")
        
        # 4. Скачивание XML для каждого найденного ID
        for eid in event_ids:
            # Делаем паузу перед запросом
            time.sleep(REQUEST_DELAY) 
            download_isc_xml(eid, folder_path)

if __name__ == "__main__":
    main()