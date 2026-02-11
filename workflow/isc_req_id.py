#!/usr/bin/env python3
import requests
import xml.etree.ElementTree as ET
from datetime import datetime
import argparse
import sys

def get_isc_earthquakes(start_dt_str, end_dt_str):
    """
    Отправляет запрос в каталог ISC и выводит eventid найденных землетрясений.
    """
    base_url = "https://www.isc.ac.uk/cgi-bin/web-db-run"

    # Валидация формата даты перед запросом
    try:
        s_dt = datetime.strptime(start_dt_str, "%Y-%m-%d %H:%M:%S")
        e_dt = datetime.strptime(end_dt_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        print(f"Ошибка: Неверный формат даты. Ожидается 'YYYY-MM-DD HH:MM:SS'.")
        print(f"Получено: start='{start_dt_str}', end='{end_dt_str}'")
        sys.exit(1)

    params = {
        'request': 'COMPREHENSIVE',
        'out_format': 'CATQuakeML',
        'searchshape': 'GLOBAL',
        'start_year': s_dt.year,
        'start_month': s_dt.month,
        'start_day': s_dt.day,
        'start_time': s_dt.strftime('%H:%M:%S'),
        'end_year': e_dt.year,
        'end_month': e_dt.month,
        'end_day': e_dt.day,
        'end_time': e_dt.strftime('%H:%M:%S'),
        'bot_lat': '', 'top_lat': '', 'left_lon': '', 'right_lon': '',
        'ctr_lat': '', 'ctr_lon': '', 'radius': '', 'max_dist_units': 'deg',
        'srn': '', 'grn': '', 'min_dep': '', 'max_dep': '',
        'min_mag': '', 'max_mag': '', 'req_mag_type': '', 'req_mag_agcy': '',
        'include_links': 'on'
    }

    print(f"Запрос данных с {start_dt_str} по {end_dt_str}...")

    try:
        response = requests.get(base_url, params=params, timeout=30)
        response.raise_for_status()

        if b'No events were found' in response.content:
            print("Событий не найдено.")
            return

        root = ET.fromstring(response.content)
        
        found_ids = []
        for elem in root.iter():
            if elem.tag.endswith('event') and not elem.tag.endswith('eventParameters'):
                public_id = elem.get('publicID')
                if public_id:
                    event_id = public_id.split('/')[-1]
                    found_ids.append(event_id)
        
        if found_ids:
            print(f"Найдено событий: {len(found_ids)}")
            print("-" * 20)
            for eid in found_ids:
                print(eid)
        else:
            print("XML получен, но ID событий не найдены.")

    except requests.exceptions.RequestException as e:
        print(f"Ошибка сети: {e}")
        sys.exit(1)
    except ET.ParseError:
        print("Ошибка обработки XML ответа.")
        sys.exit(1)

if __name__ == "__main__":
    # Создаем парсер аргументов
    parser = argparse.ArgumentParser(
        description="Поиск Event ID в каталоге ISC (International Seismological Centre)"
    )
    
    # Добавляем аргументы. 
    # Поддерживаем и -start_date, и --start_date для удобства
    parser.add_argument(
        '-s', '-start_date', '--start_date', 
        required=True, 
        help='Дата начала в формате "YYYY-MM-DD HH:MM:SS"'
    )
    parser.add_argument(
        '-e', '-end_date', '--end_date', 
        required=True, 
        help='Дата конца в формате "YYYY-MM-DD HH:MM:SS"'
    )

    args = parser.parse_args()

    # Запускаем основную функцию
    get_isc_earthquakes(args.start_date, args.end_date)