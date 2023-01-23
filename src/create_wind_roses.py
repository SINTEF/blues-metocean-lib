import os
import shutil
import time
import calendar
from datetime import datetime
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

from windrose import WindroseAxes
from bluesmet.normet.nora3 import read_winds

fields = []

# fields.append({
#     "name": "sorlige_nordsjo_2",
#     "lat_pos": 56.77859375,
#     "lon_pos": 4.8649305555555555
# })

# fields.append({
#     "name": "sorlige_nordsjo_1",
#     "lat_pos": 57.42065125,
#     "lon_pos": 3.53473625
# })

# fields.append({
#     "name": "utsira_nord",
#     "lat_pos": 59.27676125,
#     "lon_pos":4.5404045
# })

# fields.append({
#     "name": "froyagrunnene",
#     "lat_pos":61.748991249999996,
#     "lon_pos":4.6825475
# })

# fields.append({
#     "name": "sandskallen_soroya_nord",
#     "lat_pos":70.9424475,
#     "lon_pos":22.54615925
# })

fields.append({
    "name": "Mitt_punkt",
    "lat_pos":50.9424475,
    "lon_pos":12.54615925
})

for field in fields:
    felt = field["name"]
    lon_pos = field["lon_pos"]
    lat_pos = field["lat_pos"]
    path = Path(f"./output/windroses/{felt}")
    if path.exists():
        shutil.rmtree(path)
    os.makedirs(path, exist_ok=True)

    # Start timing
    start = time.time()

    years = range(1993,1994)

    all_values = {}
    for year in years:
        yearly = {}
        all_values[year]=yearly

        for month in range(1,13):
            monthly ={
                "longitude": lon_pos,
                "latitude": lat_pos,
            }
            yearly[month]=monthly

            start_date = datetime(year, month,1)
            mrange = calendar.monthrange(year, month)
            end_date = datetime(year, month,mrange[1])

            read_winds.get_values_between(start_date, end_date, monthly)


    all_speed = np.ndarray(0)
    all_direction = np.ndarray(0)

    for month in range(1,13):

        speed = np.ndarray(0)
        direction = np.ndarray(0)

        for year in years:
            yearly = all_values[year]
            monthly=yearly[month]

            mspeed = monthly["wind_speed"][:,0]
            # Met: North West Up, wind_going_to
            # Wind rose: North East Down, wind coming from
            mdir = np.fmod(monthly["wind_direction"][:,0]+180.0, 360.0)
            speed = np.concatenate((speed,mspeed))
            direction = np.concatenate((direction,mdir))

        # plt.plot(hours, speed)
        # plt.savefig(path / ("windspeed_" + datlab + ".png"))
        # plt.close()

        # plt.plot(hours, direction)
        # plt.savefig(path / ("winddir_" + datlab + ".png"))
        # plt.close()

        ax = WindroseAxes.from_ax()
        ax.bar(direction, speed,bins=9,nsector=36, opening=0.8, edgecolor="white")
        ax.set_legend()
        name=calendar.month_name[month]

        height = monthly["height"]
        ax.set_title(f"Montly wind - {name} - all years at {height[0]} m")
        ax.figure.savefig(path / f"rose_{month}.png")
        plt.close()

        all_speed = np.concatenate((all_speed,speed))
        all_direction = np.concatenate((all_direction,direction))

    ax = WindroseAxes.from_ax()
    ax.bar(all_direction, all_speed,bins=9,nsector=36, opening=0.8, edgecolor="white")
    ax.set_legend()
    ax.set_title(f"Wind - all data at {height[0]} m")
    ax.figure.savefig(path / "rose_all.png")
    plt.close()

# End timing and print elapsed time
end = time.time()
print("Elapsed time: " + str(end - start) + " seconds")
