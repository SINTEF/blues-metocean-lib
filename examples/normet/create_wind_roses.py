import os
import shutil
import time
import calendar
from datetime import datetime
from pathlib import Path
import numpy as np

from windrose import WindroseAxes
from bluesmet.normet.nora3 import arome3km_3hr


name = "Sørlig Nordsjø II"
lat_pos = 56.758896
lon_pos = 4.903143
path = Path(f"./output/windroses/{name}")
if path.exists() and path.is_dir():
    shutil.rmtree(path)
os.makedirs(path, exist_ok=True)

# Start timing
start = time.time()

years = range(1993,1994)

syears = f"[{years.start}-{years.stop}]"

all_values = {}

requested_values=["wind_speed","wind_direction","height"]

for year in years:
    yearly = {}
    all_values[year]=yearly

    for month in range(1,13):
        start_date = datetime(year, month,1)
        mrange = calendar.monthrange(year, month)
        end_date = datetime(year, month,mrange[1])

        monthly = arome3km_3hr.get_values_between(lat_pos,lon_pos,start_date, end_date,requested_values)
        yearly[month]=monthly

all_speed = np.ndarray(0)
all_direction = np.ndarray(0)

iheight = 0

for month in range(1,13):

    speed = np.ndarray(0)
    direction = np.ndarray(0)

    for year in years:
        yearly = all_values[year]
        monthly=yearly[month]

        mspeed = monthly["wind_speed"][:,iheight]
        # Met: North West Up, wind_going_to
        # Wind rose: North East Down, wind coming from
        mdir = np.fmod(monthly["wind_direction"][:,0]+180.0, 360.0)
        speed = np.concatenate((speed,mspeed))
        direction = np.concatenate((direction,mdir))

    ax = WindroseAxes.from_ax()
    ax.bar(direction, speed,bins=9,nsector=36, opening=0.8, edgecolor="white")
    ax.set_legend()
    name=calendar.month_name[month]

    heights = monthly["height"].values
    ax.set_title(f"Monthly wind - {name} - {syears} at {heights[iheight]} m")
    ax.figure.savefig(path / f"rose_{month}.png")

    all_speed = np.concatenate((all_speed,speed))
    all_direction = np.concatenate((all_direction,direction))

ax = WindroseAxes.from_ax()
ax.bar(all_direction, all_speed,bins=9,nsector=36, opening=0.8, edgecolor="white")
ax.set_legend()
ax.set_title(f"Wind - all data at {heights[iheight]} m")

ax.figure.savefig(path / "rose_all.png")

# End timing and print elapsed time
end = time.time()
print("Elapsed time: " + str(end - start) + " seconds")
