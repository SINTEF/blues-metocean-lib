import os
from datetime import datetime
from dateutil import rrule
import netCDF4 as nc
from numpy import ndarray

from ..values import TimeValues
from ..subset import subset

def get_values_between(lat_pos: float,lon_pos: float,start_date: datetime,end_date: datetime, requested_values):
    """Return values for norkyst current subset"""
    values = {}
    values["latitude"]=lat_pos
    values["longitude"]=lon_pos
    values["requested_values"]= requested_values

    dimensions = {}

    for date in rrule.rrule(rrule.MONTHLY, dtstart=start_date, until=end_date):
        __get_values_for_date(date, values,dimensions)

    # FIXME: Move to internal
    subset(values,start_date, end_date,requested_values,dimensions)

    rvalues = {}
    # add_values = ["time","latitude_actual","longitude_actual","depth"]
    add_values = ["time","latitude_actual","longitude_actual"]
    for key in add_values + requested_values:
        rvalues[key]=values[key]
    return rvalues


def __get_url(date: datetime):
    # * https://thredds.met.no/thredds/fou-hi/fou-hi.html
    # ** https://thredds.met.no/thredds/fou-hi/norkyst800v2.html
    # *** https://thredds.met.no/thredds/catalog/fou-hi/norkyst800m-1h/catalog.html
    basename = "NorKyst-800m_ZDEPTHS_his.an"
    datlab = date.strftime("%Y%m%d")
    hour = "00"
    base_url = "https://thredds.met.no/thredds/dodsC/fou-hi/norkyst800m-1h"
    return f"{base_url}/{basename}.{datlab}{hour}.nc"

def __create_cache():
    """Return values for nora3 wave subset"""
    cache_name = os.path.splitext(os.path.basename(__file__))[0]
    cache_location = f"./cache/{cache_name}/"
    return TimeValues(cache_location)

def __get_values_for_date(date: datetime, values,dimensions):
    """Return values for nora3 wave subset"""
    url = __get_url(date)
    lv=__create_cache()
    values["lon_name"] = "lon"
    values["lat_name"] = "lat"
    lv.get_values(date, url, values,dimensions)

def get_root_values(values: dict):
    """Get root values based on dictionary keys"""
    lv=__create_cache()
    url = __get_url(datetime(2020,12,1))
    return lv.get_root_values(url, values)

def get_metadata():
    """Get metadata"""
    start_date = datetime(2017,2,20)
    url = __get_url(start_date)
    metadata = {}
    global_meta = {
        "fromDate" : start_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "url": "https://thredds.met.no/thredds/catalog/fou-hi/norkyst800m-1h/catalog.html",
    }
    metadata["global"]=global_meta

    with nc.Dataset(url,"r") as f0:
        gmet=dict(f0.__dict__)
        global_meta["description"]=gmet["title"]
        variables = {}
        metadata["variables"]=variables
        for name,var in f0.variables.items():
            var_meta = {}
            variables[name]=var_meta
            for key,value in var.__dict__.items():
                if key.startswith("_"):
                    continue
                if isinstance(value,ndarray):
                    var_meta[key]=str(value.tolist())
                elif isinstance(value,str):
                    var_meta[key]=value
                else:
                    var_meta[key]=str(value)
            dims = var.dimensions
            if len(dims) > 0:
                if len(dims) == 1 and dims[0] == name:
                    continue
                var_meta["dimensions"]=",".join(dims)
    return metadata