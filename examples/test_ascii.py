from datetime import datetime

import xarray as xr
import pandas as pd

from bluesmet.normet.nora3 import wave_sub_time, arome3km_3hr

lat_pos = 64.1154
lon_pos = 7.8877
start_date = datetime(2020, 10, 21)
end_date = datetime(2020, 11, 21)
requested_values = ["height", "wind_speed", "wind_direction"]
wind_data = arome3km_3hr.get_values_between(
    lat_pos, lon_pos, start_date, end_date, requested_values
)

wind_time =  wind_data["time"]

requested_values = [
    "hs",
    "tp",
    "thq",
    "ff",
    "Pdir",
    "hs_sea",
    "tp_sea",
    "hs_swell",
    "tp_swell",
]
wave_data: xr.Dataset = wave_sub_time.get_values_between(
    lat_pos, lon_pos, start_date, end_date, requested_values
)

column_names = ["YEAR", "M", "D", "H"]

heights = wind_data["height"]

for h in heights:
    column_names.append(f"W{h:.0f}")

for h in heights:
    column_names.append(f"D{h:.0f}")


column_names.extend(["HS", "TP", "TM", "DIRP", "HS", "TP", "HS", "TP"])

description = f"Hourly Nora 3 data from {start_date} to {end_date}"

lines = []

lines.append(description)
lines.append(f"LATITUDE: {lat_pos}, LONGITUDE:   {lon_pos}")
lines.append("\t\t\t\t\tWIND SPEED\t\t\t\t\t\t\tWIND DIRECTION\t\t\t\t\t\tTOTAL SEA\t\t\tWIND SEA\tSWELL")
lines.append("\t".join([str(x) for x in column_names]))

wind_speeds = wind_data["wind_speed"].values
wind_directions = wind_data["wind_direction"].values

# Total
hs_total = wave_data["hs"].values
tp_total = wave_data["tp"].values
dirp_total = wave_data["Pdir"].values
dirm_total = wave_data["thq"].values
# Wind sea
hs_wind = wave_data["hs_sea"].values
tp_wind = wave_data["tp_sea"].values
#  Swell
hs_swell = wave_data["hs_swell"].values
tp_swell = wave_data["tp_swell"].values

wave_time = pd.to_datetime(wave_data["time"].values)

for i, dt in enumerate(wave_time):
    # Print year, month, day, hour from datetime64
    row = []
    row.append(dt.year)
    row.append(dt.month)
    row.append(dt.day)
    row.append(dt.hour)
    # The wind data is given each 3d hour, so we need to reuse the last previous 2 values
    idx = int(i / 3)
    if len(wind_speeds) <= idx:
        # data is missing, reuse last value
        idx = len(wind_speeds) - 1
    for j, h in enumerate(heights):
        ws = wind_speeds[idx][j]
        row.append(f"{ws:.2f}")
    for j, h in enumerate(heights):
        wd = wind_directions[idx][j]
        row.append(f"{wd:.2f}")
    # Total sea
    row.append(f"{hs_total[i]:.2f}")
    row.append(f"{tp_total[i]:.2f}")
    row.append(f"{dirm_total[i]:.2f}")
    row.append(f"{dirp_total[i]:.2f}")
    # Wind sea
    row.append(f"{hs_wind[i]:.2f}")
    row.append(f"{tp_wind[i]:.2f}")
    # Swell
    row.append(f"{hs_swell[i]:.2f}")
    row.append(f"{tp_swell[i]:.2f}")

    lines.append("\t".join([str(x) for x in row]))

with open("output/output.txt", mode="wt", encoding="utf8") as f:
    f.writelines("\n".join(lines))
