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
    max_concurrent_downloads = 1
):
    """Return values for wave_sub_time dataset
    
    Pdir
    standard_name: sea_surface_wave_to_direction_at_variance_spectral_density_maximu
    long_name: peak direction
    units: degree

    dd
    standard_name: wind_to_direction
    long_name: Wind direction
    units: degree

    ff
    standard_name: wind_speed
    long_name: Wind speed
    units: m s-1

    fpl
    standard_name: interpolated_peak_frequency
    long_name: interpolated peak frequency
    units: s

    hs
    standard_name: sea_surface_wave_significant_height
    long_name: Total significant wave height
    units: m

    hs_sea
    standard_name: sea_surface_wind_wave_significant_height
    long_name: Sea significant wave height
    units: m

    hs_swell
    standard_name: sea_surface_swell_wave_significant_height
    long_name: Swell significant wave height
    units: m

    model_depth
    standard_name: sea_floor_depth_below_sea_level
    long_name: water depth
    units: m

    thq
    standard_name: sea_surface_wave_to_direction
    long_name: Total mean wave direction
    units: degree

    thq_sea
    standard_name: sea_surface_wind_wave_to_direction
    long_name: Sea mean wave direction
    units: degree

    thq_swell
    standard_name: sea_surface_swell_wave_to_direction
    long_name: Swell mean wave direction
    units: degree

    tm1
    standard_name: sea_surface_wave_mean_period_from_variance_spectral_density_first_frequency_moment
    long_name: Total m1-period
    units: s

    tm2
    standard_name: sea_surface_wave_mean_period_from_variance_spectral_density_second_frequency_moment
    long_name: Total m2-period
    units: s

    tmp
    standard_name: sea_surface_wave_mean_period_from_variance_spectral_density_inverse_frequency_moment
    long_name: Total mean period
    units: s

    tp
    standard_name: sea_surface_wave_period_at_variance_spectral_density_maximum
    long_name: Total peak period
    units: s

    tp_sea
    standard_name: sea_surface_wind_wave_peak_period_from_variance_spectral_density
    long_name: Sea peak period
    units: s

    tp_swell
    standard_name: sea_surface_swell_wave_peak_period_from_variance_spectral_density
    long_name: Swell peak period
    units: s

    """

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
        max_concurrent_downloads
    )


def __get_url(date: datetime):
    basename = "NORA3wave_sub_time_unlimited"
    base_url = "https://thredds.met.no/thredds/dodsC/nora3wavesubset_files/wave_v4/"
    dataset_name = f"_{basename}"
    datlab = date.strftime("%Y%m")
    return base_url + datlab + dataset_name + ".nc"


def get_metadata():
    """Get metadata"""
    from_date = datetime(1989, 1, 1)
    to_date = datetime(2022, 12, 31)
    url = __get_url(from_date)
    ds = Dataset("./cache/wave_sub_time/", url, from_date)
    metadata = ds.get_metadata()
    metadata["global"] = {
        "fromDate": from_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "toDate": to_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "url": "https://thredds.met.no/thredds/catalog/nora3wavesubset_files/wave_v4/catalog.html",
    }
    return metadata
