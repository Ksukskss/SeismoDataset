import pandas as pd
from pathlib import Path

BASE = Path("/home/ksukskss/Projects/seismic_project/data/ALL_MOY_and_OPTI_2025_MAJ_till_31122023")

rows = []
for event_dir in BASE.rglob("FCTs_*"):
    if not event_dir.is_dir():
        continue
    files_inside = list(event_dir.iterdir())

    moy_file = next(f for f in files_inside if "moy" in f.name)
    #opt_file = next(f for f in files_inside if "opt" in f.name)
    with moy_file.open("r") as f:
        line1 = f.readline().strip().split()
        line2 = f.readline().strip().split()
    year, month, day = line1[:3]
    hh, mm = line1[3], line1[4]
    ss = line1[5]
    
    lat = float(line1[6])
    lon = float(line1[7])
    depth = float(line2[0])
    M0 = float(line2[1])
    Mw = float(line2[2])
    strike1, dip1, rake1 = map(float, line2[3:6])
    strike2, dip2, rake2 = map(float, line2[6:9])
    rows.append({
        "event_id": event_dir.name,
        "date": f"{year}-{month}-{day}",
        "time": f"{hh}:{mm}:{ss}",
        "lat": lat,
        "lon": lon,
        "depth_km": depth,
        "M0": M0,
        "Mw": Mw,
        "strike1": strike1,
        "dip1": dip1,
        "rake1": rake1,
        "strike2": strike2,
        "dip2": dip2,
        "rake2": rake2,
    })

df = pd.DataFrame(rows)


df['temp_ts'] = pd.to_datetime(df['date'] + ' ' + df['time'])
df = df.sort_values(by='temp_ts')
df = df.drop(columns=['temp_ts'])

output_path = Path(__file__).parent / "scardec_catalog.csv"
df.to_csv(output_path, index=False)

print(f"Файл сохранен: {output_path}")