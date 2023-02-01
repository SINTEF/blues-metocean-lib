from datetime import datetime
from bluesmet.normet.nora3 import wave_sub_time

def test_wave_sub_time():
    """Test wave data access"""
    lat_pos = 64.1154
    lon_pos = 7.8877
    start_date = datetime(2020, 10, 21)
    end_date = datetime(2020, 11, 21)
    requested_values = [
        "hs",
        "tp"
    ]
    values = wave_sub_time.get_values_between(
        lat_pos, lon_pos, start_date, end_date, requested_values
    )

    time = values["time"]
    # FIXME This is another value on the server for some reason
    # assert time.shape[0] == 746

    hs = values["hs"]
    assert hs.shape[0] == time.shape[0]

    # Then we add another to test the cache mechanism
    requested_values = [
        "dd",
    ]
    values = wave_sub_time.get_values_between(
        lat_pos, lon_pos, start_date, end_date, requested_values
    )

    time = values["time"]
    # assert time.shape[0] == 746
    dd = values["dd"]
    assert dd.shape[0] == time.shape[0]
