from datetime import datetime
from bluesmet.normet.norkyst import zdepths_his

def test_norkyst():
    """Test Norkyst data access"""
    lat_pos = 64.1154
    lon_pos = 7.8877
    # This data is stored 
    start_date = datetime(2020, 10, 21,2)
    end_date = datetime(2020, 10, 22,1)
    requested_values = [
        "u_eastward",
        "depth"
    ]
    values = zdepths_his.get_values_between(
        lat_pos, lon_pos, start_date, end_date, requested_values
    )

    time = values["time"]
    assert time.shape[0] == 24

    depth = values["depth"]
    assert depth.shape[0] == 16
    u_eastward = values["u_eastward"]
    assert u_eastward.shape[0] == 24
    assert u_eastward.shape[1] == 16

    # Then we add another to test the cache mechanism
    requested_values = [
        "v_northward",
    ]
    values = zdepths_his.get_values_between(
        lat_pos, lon_pos, start_date, end_date, requested_values
    )

    time = values["time"]
    assert time.shape[0] == 24
    u_eastward = values["v_northward"]
    assert u_eastward.shape[0] == 24
    assert u_eastward.shape[1] == 16
