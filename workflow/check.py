'Скрипт для проверки наличия .xml файлов в папках и наличия тегов <origin> и <phase> внутри этих файлов. Результаты сохраняются в текстовый отчет.'

import os
from pathlib import Path

def generate_seismic_report():
    # Путь к базовому каталогу
    base_dir = Path("/home/ksukskss/Projects/seismic_project/data/train/")
    
    # Имя файла для итогового отчета
    report_filename = "seismic_report.txt"
    
    # Списки для сбора информации
    missing_xml_folders = []
    missing_origin_folders =[]
    missing_phase_folders =[]

    # Проверяем, существует ли каталог
    if not base_dir.exists() or not base_dir.is_dir():
        print(f"Ошибка: Каталог '{base_dir}' не найден.")
        return

    # Получаем список всех папок внутри базового каталога
    folders = [f for f in base_dir.iterdir() if f.is_dir()]
    total_folders = len(folders)
    print(f"Найдено папок для обработки: {total_folders}")

    # Пробегаем по каждой папке
    for i, folder in enumerate(folders, 1):
        if i % 500 == 0:
            print(f"Обработано {i} / {total_folders} папок...")

        # Ищем .xml файлы в текущей папке
        xml_files = list(folder.glob("*.xml"))
        
        if not xml_files:
            missing_xml_folders.append(folder.name)
            continue
        
        # Берем первый найденный .xml файл
        xml_file = xml_files[0]
        
        has_origin = False
        has_phase = False
        
        # Читаем файл построчно для экономии памяти и ускорения процесса
        try:
            with xml_file.open('r', encoding='utf-8') as f:
                for line in f:
                    # Ищем <origin (без закрывающей скобки, так как внутри есть атрибуты)
                    if "<origin" in line:
                        has_origin = True
                    # Ищем <phase> 
                    if "<phase>" in line:
                        has_phase = True
                        
                    # Если нашли оба тега, дальше файл можно не читать
                    if has_origin and has_phase:
                        break
        except Exception as e:
            print(f"Ошибка при чтении файла {xml_file}: {e}")
            continue

        # Записываем результаты
        if not has_origin:
            missing_origin_folders.append(folder.name)
        if not has_phase:
            missing_phase_folders.append(folder.name)

    # Формируем и сохраняем отчет
    print("Формирование отчета...")
    with open(report_filename, 'w', encoding='utf-8') as report:
        report.write("=== Отчет по проверке сейсмических данных ===\n")
        report.write(f"Всего проверено папок: {total_folders}\n\n")
        
        report.write("-" * 50 + "\n")
        report.write(f"1. Папки без .xml файлов ({len(missing_xml_folders)} шт.):\n")
        if missing_xml_folders:
            for name in sorted(missing_xml_folders):
                report.write(f" - {name}\n")
        else:
            report.write(" [Все папки содержат .xml файлы]\n")
            
        report.write("\n" + "-" * 50 + "\n")
        report.write(f"2. Папки, в .xml которых нет тега <origin> ({len(missing_origin_folders)} шт.):\n")
        if missing_origin_folders:
            for name in sorted(missing_origin_folders):
                report.write(f" - {name}\n")
        else:
            report.write("[Во всех файлах найден тег <origin>]\n")
            
        report.write("\n" + "-" * 50 + "\n")
        report.write(f"3. Папки, в .xml которых нет тега <phase> ({len(missing_phase_folders)} шт.):\n")
        if missing_phase_folders:
            for name in sorted(missing_phase_folders):
                report.write(f" - {name}\n")
        else:
            report.write("[Во всех файлах найден тег <phase>]\n")

    print(f"Готово! Отчет сохранен в файл: {report_filename}")

if __name__ == "__main__":
    generate_seismic_report()