from datetime import datetime
from bluesmet.normet.nora3 import arome3km_3hr


def test_arome3km():
    """Test Arome 3km wind data access"""
    lat_pos = 64.1154
    lon_pos = 7.8877
    start_date = datetime(2020, 10, 21)
    end_date = datetime(2020, 11, 21)
    requested_values = ["wind_speed", "height"]
    values = arome3km_3hr.get_values_between(
        lat_pos, lon_pos, start_date, end_date, requested_values
    )

    time = values["time"]

    height = values["height"]
    assert height.shape[0] == 5
    u_eastward = values["wind_speed"]
    assert u_eastward.shape[0] == time.shape[0]
    assert u_eastward.shape[1] == height.shape[0]

    # Then we add another to test the cache mechanism
    requested_values = [
        "wind_direction",
    ]
    values = arome3km_3hr.get_values_between(
        lat_pos, lon_pos, start_date, end_date, requested_values
    )

    time = values["time"]
    u_eastward = values["wind_direction"]
    assert u_eastward.shape[0] == time.shape[0]
    assert u_eastward.shape[1] == height.shape[0]
