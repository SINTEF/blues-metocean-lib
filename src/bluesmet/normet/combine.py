from datetime import datetime
from pathlib import Path
from typing import Callable, Sequence

import concurrent.futures
import pandas as pd
import xarray as xr
from dateutil import rrule

from .dataset import Dataset


def get_values_between(
    requested_values: Sequence[str],
    lat_pos: float,
    lon_pos: float,
    lon_name: str,
    lat_name: str,
    start_date: datetime,
    end_date: datetime,
    frequency: int,
    cache_location: str,
    url_converter: Callable[[datetime], str],
    max_concurrent_downloads = 1
):
    """Return values beween the given dates for the given coordinates"""

    coordinates = {
        "latitude": lat_pos,
        "longitude": lon_pos,
        "lon_name": lon_name,
        "lat_name": lat_name,
    }

    # The list of required values might be altered in lower layers if dependent values are required
    all_values = list(requested_values)

    dates = rrule.rrule(frequency, dtstart=start_date, until=end_date)
    paths = []

    def process_date(date):
        dimensions = {}
        path = __get_values_for_date(
            date, coordinates, all_values, dimensions, cache_location, url_converter
        )
        return path


    if max_concurrent_downloads > 1:
        # Use ThreadPoolExecutor for parallel processing
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_concurrent_downloads) as executor:
            # Submit tasks for each date and get the results as they complete
            future_to_date = {executor.submit(process_date, date): date for date in dates}
            # Wait for all to complete
            try:
                concurrent.futures.wait(future_to_date)
                for future in future_to_date:
                    path = future.result()
                    paths.append(path)
            # pylint: disable=broad-except
            except Exception as e:
                print(f"Error processing dates: {e}")
    else:
        # No concurrent processing
        for date in dates:
            path = process_date(date)
            paths.append(path)
        

    values = xr.Dataset()
    uninitialized = True

    # Open and combine the datasets
    for file_path in paths:
        ds = xr.open_dataset(file_path)
        if uninitialized:
            uninitialized = False
            values = ds
        else:
            values = xr.concat([values, ds], dim='time')
        ds.close()

    attributes = values.attrs
    attributes["latitude"] = coordinates["latitude_actual"]
    attributes["longitude"] = coordinates["longitude_actual"]

    # Now convert the time to datetime before we return the dataset
    values["time"] = pd.to_datetime(values["time"].values, unit='s')
    return values.sel(time=slice(start_date, end_date))


def __create_dataset(date: datetime, cache_location, url_converter):
    """Create dataset"""
    url = url_converter(date)
    ds = Dataset(cache_location, url, date)
    return ds


def __get_values_for_date(
    date: datetime,
    coordinates,
    requested_values,
    dimensions,
    cache_location,
    url_converter,
) -> Path:
    """Return values for nora3 wave subset"""
    ds = __create_dataset(date, cache_location, url_converter)
    return ds.get_values(coordinates, requested_values, dimensions)