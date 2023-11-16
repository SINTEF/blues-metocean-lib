
from datetime import datetime

from bluesmet.normet.nora3 import wave_sub_time
from bluesmet.normet.metengine.extreme_stats import joint_2D_contour


# Coordinates we want to get data for
lat_pos = 62.5365
lon_pos = 4.1770
start_date = datetime(1990, 1, 1)
end_date = datetime(2022, 12, 31)

requested_values = ["hs_swell", "tp_swell"]

values = wave_sub_time.get_values_between(
    lat_pos, lon_pos, start_date, end_date, requested_values,max_concurrent_downloads=50
)

hs_sea = values["hs_swell"]
tp_sea = values["tp_swell"]

path = "output/joint_contour.png"

joint_2D_contour(
    hs_sea, tp_sea, return_periods=[5, 10, 50, 100], image_path=path, image_title="Contour"
)