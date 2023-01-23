import os
from pathlib import Path
from datetime import datetime
import netCDF4 as nc

class Cache:

    def __init__(self, location):
        self.location = Path(location).absolute()

    def __store_subset(self, src,names, fn):
        pdir = Path(fn).parent
        if not pdir.exists():
            os.makedirs(pdir)
        with nc.Dataset(fn, 'w', format='NETCDF4') as dst:
            # copy attributes
            for name in src.ncattrs():
                dst.setncattr(name, src.getncattr(name))
            dimensions = {}
            for name in names:
                variable = src.variables[name]
                for dim in variable.dimensions:
                    dimensions[dim]=src.dimensions[dim]

            for name, dimension in dimensions.items():
                dst.createDimension(name, len(dimension) if not dimension.isunlimited() else None)

            for name in names:
                variable = src.variables[name]
                x = dst.createVariable(name, variable.datatype, variable.dimensions)
                x[:] = variable[:]


    def get_root_variables(self,url: str, names):
        filename = self.location / "root.nc"
        if not os.path.exists(filename):
            # Then we must transfer these values to the cache
            with nc.Dataset(url,"r") as f0:
                self.__store_subset(f0,names, filename)
                return [f0.variables[name][:] for name in names]
        else:

            with nc.Dataset(filename,"r") as f0:
                missing = [name for name in names if name not in f0.variables.keys()]
                if len(missing) == 0:
                    return [f0.variables[name][:] for name in names]
            # There are missing variables, so we must transfer these values to the cache
            with nc.Dataset(url,"r") as f0:
                self.__store_subset(f0,names, filename)
            # Now we can return the values 
            with nc.Dataset(filename,"r") as f0:
                return [f0.variables[name][:] for name in names]


    def to_cache_path(self, ddate: datetime,ilon, ilat) -> Path:
        year = ddate.strftime("%Y")
        month = ddate.strftime("%m")
        day = ddate.strftime("%d")
        hour = ddate.strftime("%H")
        return Path(f"{self.location}/{year}/{month}/{day}/{hour}/{ilon},{ilat}.nc")
