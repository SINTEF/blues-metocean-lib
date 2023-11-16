from datetime import datetime
from bluesmet.normet.nora3 import wave_sub_time
import numpy as np
import pandas as pd
from pandas import DatetimeIndex
import xarray as xr

from bluesmet.normet.metengine.extreme_stats import return_value
# Coordinates we want to get data for
lat_pos = 64.731729
lon_pos = 5.835813
start_date = datetime(1999, 1, 1)
end_date = datetime(2021, 12, 31)

requested_values = [
    "hs",
    "tp"
]

values = wave_sub_time.get_values_between(lat_pos, lon_pos, start_date, end_date, requested_values)

hs_vals = np.array(values["hs"])
ts = np.array(values["time"])

# Convert timestamps to datetime objects
time: DatetimeIndex = pd.to_datetime(ts, unit='s')
time_dim = time.values

hs =  xr.DataArray(hs_vals,name="Hs",coords={'time': time_dim},dims='time')

return_periods = [5,10,50,100]
ret = return_value(hs, return_periods=return_periods,image_path="output/return_value.png")
for rp,rv in zip(return_periods,ret.values):
    print(f"{rp} years: {rv:.2f} m")