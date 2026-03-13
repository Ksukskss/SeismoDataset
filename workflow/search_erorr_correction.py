'Скрипт делает запрос из файла seismic_report.txt, который содержит список папок с данными. При возникновении SEARCH ERROR, скрипт делает поветорный запрос с расширенным временным окном и без ограничения по минимальной магнитуде'

import os
import glob
import time
import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

# --- КОНФИГУРАЦИЯ ---
BASE_PATH = "/home/ksukskss/Projects/seismic_project/data/train/"
REPORT_PATH = "/home/ksukskss/Projects/seismic_project/seismic_report.txt"
ISC_URL = "https://www.isc.ac.uk/cgi-bin/web-db-run"

# Задержка между запросами, чтобы не заблокировали IP (вежливость к серверу)
REQUEST_DELAY = 1.0 
UNSEARCHED =[]

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
    Если первая попытка неудачна или вернула пустой список, выполняется 
    вторая попытка с расширенными временными рамками и без min_mag.
    """
    start_dt = dt - timedelta(seconds=5)
    end_dt = dt + timedelta(seconds=5)
    
    # --- Запрос №1 (стандартный, с min_mag=5.8) ---
    params_1 = {
        'request': 'REVIEWED',
        'out_format': 'CATQuakeML',
        'searchshape': 'GLOBAL',
        'start_year': start_dt.year,
        'start_month': start_dt.month,
        'start_day': start_dt.day,
        'start_time': start_dt.strftime('%H:%M:%S'),
        'end_year': end_dt.year,
        'end_month': end_dt.month,
        'end_day': end_dt.day,
        'end_time': end_dt.strftime('%H:%M:%S'),
        'min_mag': 5.8,
        'include_links': 'on'
    }
    
    # Функция выполнения запроса и парсинга ответа
    def fetch_ids(params):
        response = requests.get(ISC_URL, params=params, timeout=30)
        response.raise_for_status()
        
        root = ET.fromstring(response.content)
        events = root.findall('.//{*}event')
        
        found_ids =[]
        for event in events:
            public_id = event.get('publicID')
            if public_id:
                eid = public_id.split('/')[-1]
                found_ids.append(eid)
        return list(set(found_ids))

    try:
        ids = fetch_ids(params_1)
        if ids:
            return ids
    except Exception as e:
        print(f"   [SEARCH WARN] Ошибка при первом запросе: {e}")
    
    # --- Запрос №2 (если ничего не нашлось или выскочила ошибка) ---
    print("   [INFO] Ничего не найдено. Выполняется второй запрос (±10s, без min_mag)...")
    time.sleep(REQUEST_DELAY) # Задержка перед вторым запросом
    
    # Расширяем временное окно еще на 5 секунд
    start_dt_2 = start_dt - timedelta(seconds=5)
    end_dt_2 = end_dt + timedelta(seconds=5)
    
    params_2 = {
        'request': 'REVIEWED',
        'out_format': 'CATQuakeML',
        'searchshape': 'GLOBAL',
        'start_year': start_dt_2.year,
        'start_month': start_dt_2.month,
        'start_day': start_dt_2.day,
        'start_time': start_dt_2.strftime('%H:%M:%S'),
        'end_year': end_dt_2.year,
        'end_month': end_dt_2.month,
        'end_day': end_dt_2.day,
        'end_time': end_dt_2.strftime('%H:%M:%S'),
        'include_links': 'on'
    }
    
    try:
        ids_2 = fetch_ids(params_2)
        if ids_2:
            return ids_2
        else:
            UNSEARCHED.append(dt)
            return []
    except Exception as e:
        print(f"   [SEARCH ERROR] Ошибка при втором запросе: {e}")
        UNSEARCHED.append(dt)
        return[]

def download_isc_xml(event_id, output_folder):
    """
    Шаг 2: Скачивание XML для конкретного event_id и сохранение в папку.
    """
    event_id = event_id.replace('evid', '').replace('=', '').strip()
    params = {
        'event_id': event_id,
        'out_format': 'QuakeML',
        'request': 'REVIEWED',
        'include_phases': 'on',
    }

    save_path = os.path.join(output_folder, f"{event_id}.xml")
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
        
        print(f"[OK] Сохранено: {os.path.basename(save_path)}")
        
    except Exception as e:
        print(f"   [DOWNLOAD ERROR] Ошибка при скачивании ID {event_id}: {e}")

def get_folders_from_report(report_path):
    """Считывает список папок из файла seismic_report.txt."""
    folders =[]
    if not os.path.exists(report_path):
        print(f"[ERROR] Файл отчета не найден: {report_path}")
        return folders
    
    with open(report_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            # Берем только строки, которые начинаются как элементы списка с FCTs_
            if line.startswith("- FCTs_"):
                folder_name = line.replace("- ", "").strip()
                folders.append(folder_name)
    return folders

def main():
    if not os.path.exists(BASE_PATH):
        print(f"Путь к данным не найден: {BASE_PATH}")
        return

    # Получаем папки только из отчета, а не все подряд
    dirs = get_folders_from_report(REPORT_PATH)

    if not dirs:
        print("В отчете не найдено папок для обработки.")
        return

    print(f"Найдено папок для обработки из отчета: {len(dirs)}")
    
    for i, folder in enumerate(dirs, 1):
        folder_path = os.path.join(BASE_PATH, folder)
        print(f"\nProcessing {i}/{len(dirs)}: {folder}")
        
        if not os.path.exists(folder_path):
            print("   [SKIP] Папка не существует на диске.")
            continue
        
        # 1. Поиск файла fctoptsource
        search_pattern = os.path.join(folder_path, "fctoptsource*")
        files = glob.glob(search_pattern)
        
        if not files:
            print("   [SKIP] Файл данных fctoptsource не найден внутри папки.")
            continue
            
        # 2. Парсинг параметров
        result = parse_fct_file(files[0])
        if not result:
            continue
        dt, lat, lon = result
        
        # 3. Поиск event_id (Поисковые запросы)
        event_ids = search_event_ids(dt, lat, lon)
        
        if not event_ids:
            print("   [INFO] События не найдены в каталоге ISC.")
            continue
        
        print(f"   Найдено ID: {event_ids}")
        
        # 4. Скачивание XML для каждого найденного ID
        for eid in event_ids:
            time.sleep(REQUEST_DELAY) 
            download_isc_xml(eid, folder_path)

    if UNSEARCHED:
        print(f"\n[ИТОГ] Не удалось найти события для {len(UNSEARCHED)} дат.")

if __name__ == "__main__":
    main()