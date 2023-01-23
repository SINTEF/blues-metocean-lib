from datetime import datetime
from dateutil import rrule
import netCDF4 as nc
from numpy import ndarray
from .values import TimeValues
from ..subset import subset

def get_values_between(start_date: datetime,end_date: datetime, values):
    """Return values for nora3 wave subset
       North West Up coordinate system
       Wave going to
       Wing going to
    """

    requested_values = [
        "thq",
        "hs",
        "tp",
        "hs_sea",
        "tp_sea",
        "thq_sea",
        "hs_swell",
        "tp_swell",
        "thq_swell",
        "dd",
        "ff",
    ]
    values["requested_values"]=requested_values

    for date in rrule.rrule(rrule.MONTHLY, dtstart=start_date, until=end_date):
        __get_values_For_date(date, values)

    # FIXME: Move to internal
    subset(values,start_date, end_date,requested_values)

def __get_url(date: datetime):
    basename = "NORA3wave_sub_time_unlimited"
    base_url = "https://thredds.met.no/thredds/dodsC/nora3wavesubset_files/wave_v4/"
    dataset_name = f"_{basename}"
    datlab = date.strftime("%Y%m")
    return base_url+ datlab+ dataset_name + ".nc"

def __get_values_For_date(date: datetime, values):
    basename = "NORA3wave_sub_time_unlimited"
    url = __get_url(date)
    cache_location = f"./cache/{basename}/"
    values["lon_name"]="longitude"
    values["lat_name"]="latitude"
    values["level_name"]="height"
    lv=TimeValues(cache_location)
    lv.get_values(date, url, values)

def get_root_values(values: dict):
    """Get root values based on dictionary keys"""
    basename = "NORA3wave_sub_time_unlimited"
    url = __get_url(datetime(2020,12,1))
    cache_location = f"./cache/{basename}/"
    lv=TimeValues(cache_location)
    return lv.get_root_values(url, values)

def get_metadata():
    """Get metadata"""
    start_date = datetime(1993, 1, 1)
    url = __get_url(start_date)
    metadata = {}

    global_meta = {
        "fromDate": start_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "url": "https://thredds.met.no/thredds/catalog/nora3wavesubset_files/wave_v4/catalog.html",
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
