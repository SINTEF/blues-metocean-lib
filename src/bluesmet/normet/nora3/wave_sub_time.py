from datetime import datetime
from typing import Sequence

from dateutil import rrule

from bluesmet.normet.dataset import Dataset

from ..combine import get_values_between as get_values


def get_values_between(
    lat_pos: float,
    lon_pos: float,
    start_date: datetime,
    end_date: datetime,
    requested_values: Sequence[str],
    cache_location="./cache/wave_sub_time/",
):
    """Return values for wave_sub_time dataset"""

    return get_values(
        requested_values,
        lat_pos,
        lon_pos,
        "longitude",
        "latitude",
        start_date,
        end_date,
        rrule.MONTHLY,
        cache_location,
        __get_url,
    )


def __get_url(date: datetime):
    basename = "NORA3wave_sub_time_unlimited"
    base_url = "https://thredds.met.no/thredds/dodsC/nora3wavesubset_files/wave_v4/"
    dataset_name = f"_{basename}"
    datlab = date.strftime("%Y%m")
    return base_url + datlab + dataset_name + ".nc"


def get_metadata():
    """Get metadata"""
    from_date = datetime(1993, 1, 1)
    to_date = datetime(2020, 12, 31)
    url = __get_url(from_date)
    ds = Dataset("./cache/zdepths_his/", url, from_date)
    metadata = ds.get_metadata()
    metadata["global"] = {
        "fromDate": from_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "toDate": to_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "url": "https://thredds.met.no/thredds/catalog/nora3wavesubset_files/wave_v4/catalog.html",
    }
    return metadata
