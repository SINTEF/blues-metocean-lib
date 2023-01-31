import os
from datetime import datetime
from typing import Dict, Sequence

import netCDF4 as nc
import numpy as np
from numpy import ndarray
from scipy.spatial import cKDTree

from .cache import Cache


class Dataset:
    """Met.no dataset for a given date"""

    def __init__(self, cache_location: str, url: str, date: datetime):
        self.cache = Cache(location=cache_location)
        self.url = url
        self.date = date

    def get_actual_coordinates(
        self,
        lat_pos: float,
        lon_pos: float,
        lon_name="longitude",
        lat_name="latitude",
    ) -> Dict:
        """Find actual coordinates and dimensions to reduce on"""
        coordinates = {}
        latlondims = {}
        root_vars = self.cache.get_root_variables(self.url, [lon_name, lat_name], latlondims)

        lons = root_vars[lon_name]
        lats = root_vars[lat_name]

        dim1, dim2, lon_a, lat_a = Dataset.__find_nearest(lons, lats, lon_pos, lat_pos)
        dims = latlondims[lon_name]
        coordinates["longitude_actual"] = lon_a
        coordinates["latitude_actual"] = lat_a

        coordinates["dim1"] = {dims[0]: dim1}
        coordinates["dim2"] = {dims[1]: dim2}
        return coordinates

    def __update_coordinates(
        self,
        coordinates: Dict
    ) -> Dict:
        """Find actual coordinates and dimensions to reduce on"""
        lon_pos = coordinates["longitude"]
        lat_pos = coordinates["latitude"]
        lon_name = coordinates.get("lon_name", "longitude")
        lat_name = coordinates.get("lat_name", "latitude")
        latlondims = {}
        root_vars = self.cache.get_root_variables(self.url, [lon_name, lat_name], latlondims)

        lons = root_vars[lon_name]
        lats = root_vars[lat_name]

        dim1, dim2, lon_a, lat_a = Dataset.__find_nearest(lons, lats, lon_pos, lat_pos)
        dims = latlondims[lon_name]
        coordinates["longitude_actual"] = lon_a
        coordinates["latitude_actual"] = lat_a

        coordinates["dim1"] = {dims[0]: dim1}
        coordinates["dim2"] = {dims[1]: dim2}
        return coordinates

    def get_root_values(self, values: dict):
        """Get root variables based on dictionary keys"""
        names = values.keys()
        variables = self.cache.get_root_variables(self.url, names, dimensions={})
        for name, var in zip(names, variables):
            values[name] = var

    def get_values(
        self,
        coordinates: Dict,
        requested_values: Sequence[str],
        dimensions: Dict,
    ) -> Dict:
        """Get  data organized using lat,lon and date. Will cache data"""
        new_values = {"time": None}
        for name in requested_values:
            new_values[name] = None

        if "dim1" not in coordinates:
            # Then we need to read the root variables
            self.__update_coordinates(coordinates)

        dim1 = coordinates["dim1"]
        dim2 = coordinates["dim2"]

        reduction_dims = {}
        reduction_dims.update(dim1)
        reduction_dims.update(dim2)

        date_cache_path = self.cache.to_cache_path(self.date, dim1, dim2)

        if not os.path.exists(date_cache_path):
            # Then we need to read the data into the cache
            self.__download(
                self.url,
                requested_values,
                new_values,
                reduction_dims,
                date_cache_path,
                dimensions,
            )
        else:
            missing = {}
            with nc.Dataset(date_cache_path, "r") as fcache:
                for key in new_values:
                    if key not in fcache.variables:
                        missing[key] = None
                    else:
                        var = fcache.variables[key]
                        new_values[key] = var[:]
                        dimensions[key] = var.dimensions
            if len(missing) > 0:
                self.__append(self.url, missing, reduction_dims, date_cache_path, dimensions)
                new_values.update(missing)

        return new_values

    def __reduce_dims(self, var, reduction_dims):
        newdims = {}
        shape = var.shape
        dims = var.dimensions
        for dim in dims - reduction_dims.keys():
            newdims[dim] = range(0, shape[dims.index(dim)])
        for dim in reduction_dims:
            newdims[dim] = reduction_dims[dim]
        thedims = [newdims[dim] for dim in dims]
        return var[tuple(thedims)]

    def __download(
        self,
        url,
        requested_values,
        new_values,
        reduction_dims,
        date_cache_path,
        dimensions,
    ):
        with nc.Dataset(url, "r") as fonline:
            print(f"Downloading {url}")

            parent_dir = date_cache_path.parent
            if not parent_dir.exists():
                os.makedirs(parent_dir)

            time = fonline.variables["time"][:]
            new_values["time"] = time

            filedims = fonline.dimensions
            for dim in reduction_dims:
                if dim not in filedims:
                    raise Exception(f"Reducing dimension {dim} not found in file {url}")

            variables = fonline.variables

            with nc.Dataset(date_cache_path, "w", format="NETCDF4") as dst:
                remaining_dims = filedims.keys() - reduction_dims.keys()
                for name, dim in filedims.items():
                    if name in remaining_dims:
                        dst.createDimension(name, dim.size)
                for var_name in requested_values + ["time"]:
                    var = variables[var_name]
                    vals = self.__reduce_dims(var, reduction_dims)
                    var_dims = [
                        dim for dim in var.dimensions if dim not in reduction_dims
                    ]
                    new_var = dst.createVariable(var_name, var.dtype, var_dims)
                    new_var.setncatts(var.__dict__)
                    new_var[:] = vals
                    new_values[var_name] = vals
                    dimensions[var_name] = var_dims

    def __append(self, url, missing, reduction_dims, date_cache_path, dimensions):
        with nc.Dataset(url, "r") as fonline:
            print(f"Downloading {url}")

            with nc.Dataset(date_cache_path, "a", format="NETCDF4") as dst:
                for var_name in missing.keys():
                    var = fonline.variables[var_name]
                    vals = self.__reduce_dims(var, reduction_dims)
                    var_dims = [
                        dim for dim in var.dimensions if dim not in reduction_dims
                    ]
                    new_var = dst.createVariable(var_name, var.dtype, var_dims)
                    new_var.setncatts(var.__dict__)
                    new_var[:] = vals
                    missing[var_name] = vals
                    dimensions[var_name] = var_dims


    def get_metadata(self):
        """Get metadata"""
        # TODO: USE CACHE
        metadata = {}
        with nc.Dataset(self.url, "r") as f0:
            metadata["global"] = dict(f0.__dict__)
            variables = {}
            metadata["variables"] = variables
            for name, var in f0.variables.items():
                var_meta = {}
                variables[name] = var_meta
                for key, value in var.__dict__.items():
                    if key.startswith("_"):
                        continue
                    if isinstance(value, ndarray):
                        var_meta[key] = str(value.tolist())
                    elif isinstance(value, str):
                        var_meta[key] = value
                    else:
                        var_meta[key] = str(value)
                dims = var.dimensions
                if len(dims) > 0:
                    if len(dims) == 1 and dims[0] == name:
                        continue
                    var_meta["dimensions"] = ",".join(dims)
        return metadata

    @staticmethod
    def __nearest(lon, lat, lon_pos, lat_pos):
        """Find nearest point in lon lat matrix"""
        M = np.c_[np.ravel(lon), np.ravel(lat)]
        tree = cKDTree(M)
        _, ii = tree.query([lon_pos, lat_pos], k=1)
        d1, d2 = np.where((lon == M[ii][0]) & (lat == M[ii][1]))
        return int(d1), int(d2)

    @staticmethod
    def __find_nearest(lons, lats, lon_pos, lat_pos):
        dim1, dim2 = Dataset.__nearest(lons, lats, lon_pos, lat_pos)
        lon_actual = lons[dim1, dim2]
        lat_actual = lats[dim1, dim2]
        return dim1, dim2, lon_actual, lat_actual


    @staticmethod
    def __concatenate_time_arrays(values, new, dimensions):
        for name, vals in new.items():
            value = values.get(name)
            if value is None:
                values[name] = vals
            elif "time" in dimensions[name]:
                cced = np.ma.concatenate((value, vals))
                values[name] = cced
