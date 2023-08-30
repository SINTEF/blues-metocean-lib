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
    cache_location="./cache/mywavewam3km/",
    max_concurrent_downloads = 1
):
    """Return values for windsurfer/mywavewam3km dataset"""

    return get_values(
        requested_values,
        lat_pos,
        lon_pos,
        "longitude",
        "latitude",
        start_date,
        end_date,
        rrule.DAILY,
        cache_location,
        __get_url,
         max_concurrent_downloads
    )


def __get_url(day: datetime):
    url = 'https://thredds.met.no/thredds/dodsC/windsurfer/mywavewam3km_files/' + \
            day.strftime('%Y') + '/'+day.strftime('%m') +  '/' + \
            day.strftime('%Y%m%d')+'_MyWam3km_hindcast.nc'
    return url


def get_metadata():
    """Get metadata"""
    from_date = datetime(1980, 1, 1)
    to_date = datetime(2022, 12, 31)
    url = __get_url(from_date)
    ds = Dataset("./cache/mywavewam3km/", url, from_date)
    metadata = ds.get_metadata()
    metadata["global"] = {
        "fromDate": from_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "toDate": to_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "url": "https://thredds.met.no/thredds/catalog/windsurfer/mywavewam3km_files/catalog.html",
    }
    return metadata
