import os
from datetime import datetime
import netCDF4 as nc
import numpy as np
from scipy.spatial import cKDTree
from .cache import Cache


class TimeValues:
    """Get time based data"""

    def __init__(self, cache_location):
        self.cache = Cache(location=cache_location)

    def get_root_values(self, url: str, values: dict):
        """Get root variables based on dictionary keys"""
        names = values.keys()
        variables = self.cache.get_root_variables(url, names, dimensions={})
        for name, var in zip(names, variables):
            values[name] = var

    def get_values(self, date: datetime, url, values, dimensions):
        """Get  data organized using lat,lon and date. Will cache data"""
        lat_pos = values["latitude"]
        lon_pos = values["longitude"]

        requested_values = values["requested_values"]
        new_values = {"time": None}
        for name in requested_values:
            new_values[name] = None

        lon_name = values["lon_name"]
        lat_name = values["lat_name"]

        reduction_dims = {}

        if "longitude_actual" not in values:
            names = [lon_name, lat_name]
            latlondims = {}
            root_vars = self.cache.get_root_variables(url, names,latlondims)

            lons = root_vars[lon_name]
            lats = root_vars[lat_name]

            ix, iy, lon_a, lat_a = TimeValues.__find_nearest(
                lons, lats, lon_pos, lat_pos
            )
            dims = latlondims[lon_name]
            reduction_dims[dims[0]] = ix
            reduction_dims[dims[1]] = iy

            values["longitude_actual"] = lon_a
            values["latitude_actual"] = lat_a
            values["ix"] = ix
            values["iy"] = iy
            values["reduce_dims"] = reduction_dims
        else:
            ix = values["ix"]
            iy = values["iy"]
            reduction_dims = values["reduce_dims"]

        date_cache_path = self.cache.to_cache_path(date, ix, iy)

        if not os.path.exists(date_cache_path):
            # Then we need to read the data into the cache
            self.__download(
                url,
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
                self.__append(url, missing, reduction_dims, date_cache_path, dimensions)
                new_values.update(missing)

        TimeValues.__concatenate_time_arrays(values, new_values, dimensions)

    def __reduce_dims(self, var, reduction_dims):
        newdims = {}
        shape = var.shape
        name = var.name
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

    @staticmethod
    def __nearest(lon, lat, lon_pos, lat_pos):
        """Find nearest point in lon lat matrix"""
        M = np.c_[np.ravel(lon), np.ravel(lat)]
        tree = cKDTree(M)
        _, ii = tree.query([lon_pos, lat_pos], k=1)
        ix, iy = np.where((lon == M[ii][0]) & (lat == M[ii][1]))
        return int(ix), int(iy)

    @staticmethod
    def __find_nearest(lons, lats, lon_pos, lat_pos):
        ix, iy = TimeValues.__nearest(lons, lats, lon_pos, lat_pos)
        lon_actual = lons[ix, iy]
        lat_actual = lats[ix, iy]
        return ix, iy, lon_actual, lat_actual

    @staticmethod
    def __concatenate_time_arrays(values, new, dimensions):
        for name, vals in new.items():
            value = values.get(name)
            if value is None:
                values[name] = vals
            elif "time" in dimensions[name]:
                cced = np.ma.concatenate((value, vals))
                values[name] = cced
