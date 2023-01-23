from pathlib import Path
import numpy as np
from dmt.dmt_writer import DMTWriter
from bluesmet.met.dataset import Dataset
from bluesmet.met.datasetcontainer import DatasetContainer
from bluesmet.met.datasetvariable import DatasetVariable


from bluesmet.normet.nora3 import read_winds
from bluesmet.normet.nora3 import read_waves
from bluesmet.normet.norkyst import read_currents


def __get_circumference(arr):
    """Elements along the circumference of the 2D array in clockwise order starting from the top-left corner."""
    step = 50
    bottom_left = arr[0, ::step]
    bottom_right = arr[::step, -1]
    top_right = np.flip(arr[-1, ::step])
    top_left = np.flip(arr[::step, 0])
    return np.concatenate((bottom_left, bottom_right, top_right, top_left))


def __create_dataset(name, lat: np.ndarray, lon: np.ndarray, metadata: dict) -> Dataset:
    ds = Dataset()
    ds.name = name
    ds.latitudes = lat
    ds.longitudes = lon

    mglobal = metadata["global"]
    ds.fromDate = mglobal["fromDate"]
    ds.description = mglobal["description"]
    ds.url = mglobal["url"]

    for vname,v in metadata["variables"].items():
        if vname in ["projection_lambert","forecast_reference_time"]:
            continue
        description = v.get("description", v.get("long_name",""))
        unit = v.get("units")
        dimensions = v.get("dimensions")
        dsvar = DatasetVariable(name=vname,description=description,unit=unit,dimensions=dimensions)
        ds.variables.append(dsvar)
    return ds




def __create_wave():
    values = {
        "longitude": None,
        "latitude": None,
    }
    read_waves.get_root_values(values)
    clat = __get_circumference(values["latitude"])
    clon = __get_circumference(values["longitude"])
    metadata = read_waves.get_metadata()
    wave = __create_dataset("Wave hindcast - 3km - 1hr", clat, clon,metadata)
    # wave.description = "WINDSURFER/NORA3, hindcast 3km hourly instantaneous wave fields"
    return wave


def __create_wind():
    values = {
        "longitude": None,
        "latitude": None,
    }

    read_winds.get_root_values(values)
    clat = __get_circumference(values["latitude"])
    clon = __get_circumference(values["longitude"])
    metadata = read_winds.get_metadata()
    wind = __create_dataset("Arome - 3km  - 3hr", clat, clon, metadata)

    return wind


def __create_current():
    # * https://thredds.met.no/thredds/fou-hi/fou-hi.html
    # ** https://thredds.met.no/thredds/fou-hi/norkyst800v2.html
    # *** https://thredds.met.no/thredds/catalog/fou-hi/norkyst800m-1h/catalog.html
    values = {
        "lon": None,
        "lat": None,
    }

    read_currents.get_root_values(values)
    clat = __get_circumference(values["lat"])
    clon = __get_circumference(values["lon"])
    md=read_currents.get_metadata()
    current = __create_dataset("Norkyst-800 - 1km - 1hr", clat, clon,md)
    current.description = "Norkyst800, hindcast 1km hourly instantaneous current fields"
    return current


def __write_entity(entity,name):
    output_path = Path("./output/entities/datasets")
    output_path.mkdir(parents=True, exist_ok=True)
    writer = DMTWriter()
    writer.datasource = "app_met_db"

    filename = output_path / f"{name}.json"
    writer.write(entity, filename)


if __name__ == "__main__":
    # https://api.met.no/product/THREDDS
    # https://thredds.met.no/thredds/catalog.html
    nora3 = DatasetContainer()
    nora3.name = "NORA3"
    nora3.description = """NORA3 is produced by running the non-hydrostatic HARMONIE-AROME model (Seity et al.,2011, Bengtsson et al.,2017 and Muller et al.,2017) with 3km horizontal resolution and 65 vertical levels.
    The model runs 9 hourly forecasts four times a day. Each forecast starts from an assimilated state of the last forecast adapted to surface observations. 
    Model levels are forced with ERA-5 (https://climate.copernicus.eu/climate-reanalysis)."""
    nora3.datasets.append(__create_wave())
    nora3.datasets.append(__create_wind())

    norkyst = DatasetContainer()
    norkyst.name = "Norkyst-800"
    norkyst.datasets.append(__create_current())

    normet = DatasetContainer()
    normet.name = "met.no"
    normet.containers.append(nora3)
    normet.containers.append(norkyst)

    __write_entity(normet,"normet")
