from datetime import datetime
from bluesmet.normet.nora3 import wave_sub_time, arome3km_3hr
import numpy as np

# Coordinates we want to get data for
lat_pos = 64.731729
lon_pos = 5.835813
start_date = datetime(1999, 10, 21)
end_date = datetime(2004, 11, 21)

requested_values = ["hs", "tp"]
values = wave_sub_time.get_values_between(
    lat_pos,
    lon_pos,
    start_date,
    end_date,
    requested_values,
)

# Coordinates we actually to get data for (nearest grid point)
alat = values.latitude
alon = values.longitude
print(f"Actual coordinates: {alat} lon: {alon}")

for requested_value in requested_values:
    value = values[requested_value].values
    print(f"{requested_value}_mean: {value.mean()}")

# Hvor blir height av??
requested_values = ["wind_speed", "wind_direction"]
values = arome3km_3hr.get_values_between(
    lat_pos,
    lon_pos,
    start_date,
    end_date,
    requested_values
)
alat = values.latitude
alon = values.longitude
print(f"Actual coordinates 2: {alat} lon: {alon}")

heights = values.height.values

for iheight,heigth in enumerate(heights):
    print(f"height: {heigth}")
    for requested_value in requested_values:
        rv = values[requested_value].values
        value = rv[:, iheight]
        print(f"{requested_value} statistics:")
        print(f"mean: {value.mean()}")
        print(f"max: {value.max()}")
        print(f"p10: {np.percentile(value, 10)}")
        print(f"p90: {np.percentile(value, 90)}")
        print()
