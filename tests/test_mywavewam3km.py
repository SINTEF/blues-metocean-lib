from datetime import datetime
from math import isclose
from bluesmet.normet.nora3 import mywavewam3km

def test_wave_sub_time():
    """Test wave data access"""
    lat_pos = 62.5
    lon_pos = 5.7
    start_date = datetime(1990, 1, 1)
    end_date = datetime(1990, 1, 3)
    requested_values = [
        'hs','tp','thq','hs_swell'
    ]
    values = mywavewam3km.get_values_between(
        lat_pos, lon_pos, start_date, end_date, requested_values
    )

    time = values["time"]
    lat_actual = values.attrs["latitude"]
    lon_actual = values.attrs["longitude"]
    # Compared againts norway MET Metocean engine
    assert isclose(lat_actual, 62.50591, abs_tol=1e-5)
    assert isclose(lon_actual, 5.693615, abs_tol=1e-7)

    # Then we add another to test the cache mechanism
    requested_values = [
        "dd",
    ]
    values = mywavewam3km.get_values_between(
        lat_pos, lon_pos, start_date, end_date, requested_values
    )

    time = values["time"]
    dd = values["dd"]
    assert dd.shape[0] == time.shape[0]
