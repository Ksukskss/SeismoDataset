import matplotlib.pyplot as plt
from pathlib import Path

def create_stf_image(event_dir_path):
    script_dir = Path(__file__).parent.resolve()

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
        print(f"❌ Ошибка при чтении: {e}")
        return

    plt.figure(figsize=(10, 6))
    
    plt.plot(times, amplitudes, color='#0052cc', linewidth=2, label='Moment Rate')
    plt.fill_between(times, amplitudes, color='#0052cc', alpha=0.1)
    plt.axvline(0, color='red', linestyle='--', alpha=0.8, label='Onset (t=0)')
    plt.axhline(0, color='black', linewidth=0.8)
    plt.title(f"Source Time Function\nEvent: {event_dir.name}\n{metadata_text}", fontsize=12)
    plt.xlabel("Time (s)")
    plt.ylabel("Moment Rate (N·m/s)")
    plt.legend()
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.tight_layout()

    output_filename = f"STF_{event_dir.name}.png"
    output_path = script_dir / output_filename
    
    plt.savefig(output_path, dpi=150)
    plt.close() 

    print(f"График сохранен: {output_path}")

EVENT_DIR = "/home/ksukskss/Projects/seismic_project/data/train/FCTs_20110311_054624_NEAR_EAST_COAST_OF_HONSHU__JAPAN/" 
full_path = Path(EVENT_DIR).expanduser()
create_stf_image(full_path)