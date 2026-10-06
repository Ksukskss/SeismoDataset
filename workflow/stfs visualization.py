import matplotlib.pyplot as plt
from pathlib import Path

# Теперь функция принимает список кортежей: [(путь, цвет), (путь, цвет), ...]
def create_stf_image(events_list):
    script_dir = Path(__file__).parent.resolve()

    # Создаем холст один раз до цикла
    plt.figure(figsize=(10, 6))

    # Проходим циклом по всем переданным директориям и их цветам
    for event_dir_path, color in events_list:
        event_dir = Path(event_dir_path).resolve()
        opt_file = next(event_dir.glob("*opt*"))

        times = []
        amplitudes = []
        metadata_text = ""

        try:
            with opt_file.open('r') as f:
                line1 = f.readline().strip().split()
                line2 = f.readline().strip().split()

                date_str = f"{line1[0]}-{line1[1]}-{line1[2]}"
                depth_val = line2[0]
                mw_val = line2[2]
                
                metadata_text = f"Date: {date_str} | Mw: {mw_val} | Depth: {depth_val} km"

                for line in f:
                    parts = line.strip().split()
                    clean_parts = [p for p in parts if not p.startswith("[") and not p.endswith("]")]
                    
                    if len(clean_parts) >= 2:
                        try:
                            t = float(clean_parts[0])
                            amp = float(clean_parts[1])
                            times.append(t)
                            amplitudes.append(amp)
                        except ValueError:
                            continue 

        except Exception as e:
            print(f"❌ Ошибка при чтении {event_dir.name}: {e}")
            continue # continue вместо return, чтобы скрипт не падал, а рисовал остальные

        # Рисуем текущий график внутри цикла, используя переданный цвет
        # Метаданные добавил в label, чтобы в легенде было видно инфу по каждому событию
        plt.plot(times, amplitudes, color=color, linewidth=2, label=f'{event_dir.name[21:]}\n{metadata_text}')
        #plt.fill_between(times, amplitudes, color=color, alpha=0.1)

    # Общие настройки графика (вне цикла)
    #plt.axvline(0, color='red', linestyle='--', alpha=0.8, label='Onset (t=0)')
    plt.axhline(0, color='black', linewidth=0.8)
    plt.title("Source Time Functions", fontsize=12)
    plt.xlabel("Time (s)")
    plt.ylabel("Moment Rate (N·m/s)")
    plt.legend(fontsize=8)
    #plt.grid(True, linestyle=':', alpha=0.6)
    plt.tight_layout()

    plt.xlim(0, 200)
    plt.ylim(0, 4.0e20)
    # Сохраняем общий файл
    output_filename = "STF_combined.png"
    output_path = script_dir / output_filename
    
    plt.savefig(output_path, dpi=150)
    plt.close() 

    print(f"График сохранен: {output_path}")


# --- Пример использования ---
# Составляем список из путей и желаемых цветов
EVENTS = [
    ("/home/ksukskss/Projects/seismic_project/data/train/FCTs_20100227_063411_NEAR_COAST_OF_CENTRAL_CHILE/", "#8bbaff"),
    ("/home/ksukskss/Projects/seismic_project/data/train/FCTs_20050328_160936_NORTHERN_SUMATRA__INDONESIA/", "#ebabff"),
    #("/home/ksukskss/Projects/seismic_project/data/train/FCTs_20010623_203314_NEAR_COAST_OF_PERU/", "#ffd08e"),
    #("/home/ksukskss/Projects/seismic_project/data/train/FCTs_20070912_111026_SOUTHERN_SUMATRA__INDONESIA/", "#ffa8e2"),
    ("/home/ksukskss/Projects/seismic_project/data/train/FCTs_20250729_232450_OFF_EAST_COAST_OF_KAMCHATKA/", "red"),
    
    # Сюда можно добавить второй, третий путь и их цвета, например:
    # ("/home/ksukskss/Projects/seismic_project/data/train/ANOTHER_EVENT_DIR/", "#2ca02c"),
    # ("/home/ksukskss/Projects/seismic_project/data/train/THIRD_EVENT_DIR/", "red"),
]

# Раскрываем ~ (если есть) прямо в списке
expanded_events = [(Path(path).expanduser(), color) for path, color in EVENTS]

create_stf_image(expanded_events)