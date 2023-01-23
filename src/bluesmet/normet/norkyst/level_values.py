import os
from datetime import datetime
import netCDF4 as nc
import numpy as np
from scipy.spatial import cKDTree
from ..cache import Cache


class LevelValues:
    """Get level based data"""

    def __init__(self, cache_location):
        self.cache = Cache(location=cache_location)

    def get_root_values(self,url: str, values: dict):
        """Get root variables based on dictionary keys"""
        names = values.keys()
        variables= self.cache.get_root_variables(url, names)
        for name, var in zip(names,variables):
            values[name]=var

    def get_level_values(self,date: datetime, url, values: dict):
        """Get level based data organized using lat,lon and date. Will cache data"""
        lat_pos = values["latitude"]
        lon_pos = values["longitude"]

        requested_values = values["requested_values"]
        new_values = {
            "time":None
        }
        for name in requested_values:
            new_values[name]=None

        lon_name = values["lon_name"]
        lat_name = values["lat_name"]
        level_name = values["level_name"]

        if "ilon" not in values:
            lons, lats, level = self.cache.get_root_variables(url, [lon_name,lat_name,level_name])
            ilon, ilat, lon_a, lat_a = LevelValues.__find_nearest(lons, lats,lon_pos, lat_pos)
            values["longitude_actual"] = lon_a
            values["latitude_actual"] = lat_a
            values[level_name] = level[:]
            values["ilon"] = ilon
            values["ilat"] = ilat
        else:
            ilon = values["ilon"]
            ilat = values["ilat"]

        date_cache_path = self.cache.to_cache_path(date,ilon, ilat)

        if not os.path.exists(date_cache_path):
            # Then we need to read the data into the cache
            with nc.Dataset(url,"r") as f0:
                print(f"Downloading {url}")

                hlevel = f0.dimensions[level_name]

                parent_dir = date_cache_path.parent
                if not parent_dir.exists():
                    os.makedirs(parent_dir)

                with nc.Dataset(date_cache_path, 'w', format='NETCDF4') as dst:
                    time =  f0.variables["time"][:]
                    dst.createDimension("time", len(time))
                    dst.createDimension(level_name, hlevel.size)
                    new_values["time"] = time
                    # Time is given in Unix epoch
                    dst.createVariable("time",np.float64, ["time"])[:] = time
                    for name in requested_values:
                        var_values = f0.variables[name]
                        vals = np.squeeze(var_values[:,:,ilon,ilat][:])
                        dst.createVariable(name, np.float64, ["time",level_name])[:] = vals
                        new_values[name]=vals
                    LevelValues.__concatenate_arrays(values, new_values)
        else:
            with nc.Dataset(date_cache_path,"r") as f0:
                LevelValues.__concatenate_variables(values, f0, new_values)

    @staticmethod
    def __nearest(lon, lat, lon_pos, lat_pos):
        """Find nearest point in lon lat matrix"""
        M = np.c_[np.ravel(lon), np.ravel(lat)]
        tree = cKDTree(M)
        _, ii = tree.query([lon_pos, lat_pos], k=1)
        ix,iy = np.where((lon == M[ii][0]) & (lat == M[ii][1]))
        return int(ix), int(iy)

    @staticmethod
    def __find_nearest(lons, lats, lon_pos, lat_pos):
        ix,iy = LevelValues.__nearest(lons,lats, lon_pos,lat_pos)
        lon_actual = lons[ix,iy]
        lat_actual = lats[ix,iy]
        return ix,iy, lon_actual, lat_actual

    @staticmethod
    def __concatenate_arrays(values, new):
        for name, vals in new.items():
            value = values.get(name)
            if value is None:
                values[name] = vals
            else:
                values[name] = np.ma.concatenate((value, vals))

    @staticmethod
    def __concatenate_variables(values, f, arrays):
        for key in arrays.keys():
            arrays[key] = f.variables[key][:]
        LevelValues.__concatenate_arrays(values, arrays)
