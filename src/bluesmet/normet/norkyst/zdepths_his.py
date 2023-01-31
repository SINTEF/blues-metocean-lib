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
    cache_location = "./cache/zdepths_his/"
):
    """Return values for norkyst current subset"""

    return get_values(requested_values, lat_pos, lon_pos, "lon", "lat", start_date,end_date,rrule.DAILY,cache_location, __get_url)

def __get_url(date: datetime):
    # * https://thredds.met.no/thredds/fou-hi/fou-hi.html
    # ** https://thredds.met.no/thredds/fou-hi/norkyst800v2.html
    # *** https://thredds.met.no/thredds/catalog/fou-hi/norkyst800m-1h/catalog.html
    basename = "NorKyst-800m_ZDEPTHS_his.an"
    datlab = date.strftime("%Y%m%d")
    hour = "00"
    base_url = "https://thredds.met.no/thredds/dodsC/fou-hi/norkyst800m-1h"
    return f"{base_url}/{basename}.{datlab}{hour}.nc"


def get_metadata():
    """Get metadata"""
    start_date = datetime(2017, 2, 20)
    url = __get_url(start_date)
    ds = Dataset("./cache/zdepths_his/", url, start_date)
    metadata = ds.get_metadata()
    global_meta = {
        "fromDate": start_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "url": "https://thredds.met.no/thredds/catalog/fou-hi/norkyst800m-1h/catalog.html",
    }
    metadata["global"] = global_meta
    return metadata
