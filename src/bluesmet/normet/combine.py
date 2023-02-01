from datetime import datetime
from typing import Callable, Sequence
from dateutil import rrule
import numpy as np
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
):
    """Return values for norkyst current subset"""
    values = {}

    # FIXME: The rrule.constant is not a good api
    # Should we instead use a list of dates with the according url?

    coordinates = {
        "latitude": lat_pos,
        "longitude": lon_pos,
        "lon_name": lon_name,
        "lat_name": lat_name,
    }

    all_values = requested_values
    # if "time" not in all_values:
    #     all_values.append("time")

    dates = rrule.rrule(frequency, dtstart=start_date, until=end_date)
    for date in dates:
        dimensions = {}
        new_values = __get_values_for_date(
            date, coordinates, all_values, dimensions, cache_location, url_converter
        )
        __concatenate_time_arrays(values, new_values, dimensions)

    __subset(values, start_date, end_date, all_values, dimensions)

    values["latitude_actual"] = coordinates["latitude_actual"]
    values["longitude_actual"] = coordinates["longitude_actual"]

    return values


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
):
    """Return values for nora3 wave subset"""
    ds = __create_dataset(date, cache_location, url_converter)
    return ds.get_values(coordinates, requested_values, dimensions)


def __concatenate_time_arrays(values, new, dimensions):
    for name, vals in new.items():
        value = values.get(name)
        if value is None:
            values[name] = vals
        elif "time" in dimensions[name]:
            cced = np.ma.concatenate((value, vals))
            values[name] = cced

def __subset(values, start_date: datetime, end_date: datetime,requested_values,dimensions):
    """Reshape the values to lie between the given dates"""
    start_time = start_date.timestamp()
    end_time = end_date.timestamp()
    time =  values["time"].astype(np.long)
    ts=time[0]
    te=time[-1]
    if ts < start_time or te > end_time:
        indices = (time >= start_time) & (time <= end_time)
        subidx = [idx for idx in range(len(indices)) if indices[idx]]
        values["time"] = time[subidx]
        for name in requested_values:
            if name == "time":
                continue
            if "time" in dimensions[name]:
                idx = dimensions[name].index("time")
                tvals = values[name]
                try:
                    subvalues = tvals.take(subidx, axis=idx)
                    values[name]=subvalues
                except IndexError:
                    print(f"IndexError: name: {name}, idx: {idx}, subidx: {subidx}, tvals: {tvals}, dimensions[name]: {dimensions[name]}")
                    raise