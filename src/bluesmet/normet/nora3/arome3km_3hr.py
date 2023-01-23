from datetime import datetime
from dateutil import rrule
import netCDF4 as nc
from numpy import ndarray
from ..values import TimeValues
from ..subset import subset

# https://thredds.met.no/thredds/projects/projects.xml
# https://thredds.met.no/thredds/projects/nora3_subsets.xml
# https://thredds.met.no/thredds/catalog/nora3wavesubset_files/catalog.xml
# https://thredds.met.no/thredds/catalog/nora3wavesubset_files/atm/catalog.xml

def get_values_between(lat_pos: float,lon_pos: float,start_date: datetime,end_date: datetime, requested_values):
    """Return values for nora3 wave subset"""
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
    add_values = ["time","latitude_actual","longitude_actual"]
    for key in add_values + requested_values:
        rvalues[key]=values[key]
    return rvalues

def get_url(date: datetime):
    basename = "arome3km_3hr"
    datlab = date.strftime("%Y%m")
    base_url = "https://thredds.met.no/thredds/dodsC/nora3wavesubset_files/atm"
    return  f"{base_url}/{basename}_{datlab}.nc"+'#fillmismatch'

def __get_values_for_date(date: datetime, values,dimensions):
    """Return values for nora3 wave subset"""
    basename = "arome3km_3hr"
    url = get_url(date)
    cache_location = f"./cache/{basename}/"

    values["lon_name"]="longitude"
    values["lat_name"]="latitude"

    lv=TimeValues(cache_location)
    lv.get_values(date, url, values,dimensions)

def get_root_values(values: dict):
    """Get root values based on dictionary keys"""
    basename = "arome3km_3hr"
    url = get_url(datetime(2020,12,1))
    cache_location = f"./cache/{basename}/"
    lv=TimeValues(cache_location)
    return lv.get_root_values(url, values)

def get_metadata():
    """Get metadata"""
    start_date = datetime(1993, 1, 1)
    url = get_url(start_date)
    print(url)
    metadata = {}

    global_meta = {
        "fromDate": start_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "url": "https://thredds.met.no/thredds/catalog/nora3wavesubset_files/atm/catalog.html",
    }

    metadata["global"]=global_meta

    with nc.Dataset(url,"r") as f0:
        gmet=dict(f0.__dict__)
        global_meta["description"]=gmet["summary"]
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
