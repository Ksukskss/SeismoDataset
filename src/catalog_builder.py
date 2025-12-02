import os
import pandas as pd

BASE = "/home/ksukskss/Projects/seismic_project/data/ALL_MOY_and_OPTI_2025_MAJ_till_31122023"

rows = []

for root, dirs, files in os.walk(BASE):
    for d in dirs:
        if not d.startswith("FCTs_"):
            continue

        event_dir = os.path.join(root, d)
        files_inside = os.listdir(event_dir)

        moy = [f for f in files_inside if "moy" in f][0]
        opt = [f for f in files_inside if "opt" in f][0]
        png = [f for f in files_inside if f.endswith(".png")][0]

        path = os.path.join(event_dir, moy)
        with open(path) as f:
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
            "event_id": d,
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
            "stf_moy": os.path.join(event_dir, moy),
            "stf_opt": os.path.join(event_dir, opt),
            "focal_png": os.path.join(event_dir, png)
        })

df = pd.DataFrame(rows)

output_path = os.path.join(os.path.dirname(__file__), "scardec_catalog.csv")
df.to_csv(output_path, index=False)

print("мяу")

