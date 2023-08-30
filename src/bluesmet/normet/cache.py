import os
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict
import netCDF4 as nc

class Cache:

    def __init__(self, location):
        self.location = Path(location).absolute()

    def __store_subset(self, src,names, file: Path):
        pdir = Path(file).parent
        if not pdir.exists():
            os.makedirs(pdir)

        intermediate = file.with_suffix(".tmp")

        if file.exists():
            shutil.copy(file, intermediate)

        try:
            with nc.Dataset(intermediate, 'w', format='NETCDF4') as dst:
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

            shutil.move(intermediate, file)
        except Exception as e:
            os.remove(intermediate)
            raise e


    def get_root_variables(self,url: str, names, dimensions=None) -> Dict:
        """Get the time independent variables from the cache or from the source url"""
        if dimensions is None:
            dimensions = {}
        filename = self.location / "root.nc"
        variables = {}
        if not os.path.exists(filename):
            # Then we must transfer these values to the cache
            with nc.Dataset(url,"r") as f0:
                self.__store_subset(f0,names, filename)
                for name in names:
                    variable = f0.variables[name]
                    variables[name]=variable[:]
                    dimensions[name]=variable.dimensions
        else:
            with nc.Dataset(filename,"r") as f0:
                missing = [name for name in names if name not in f0.variables.keys()]
                if len(missing) == 0:
                    for name in names:
                        variable = f0.variables[name]
                        variables[name]=variable[:]
                        dimensions[name]=variable.dimensions
                else:
                    # There are missing variables, so we must transfer these values to the cache
                    with nc.Dataset(url,"r") as f0:
                        self.__store_subset(f0,names, filename)
                    # Now we can return the values
                    with nc.Dataset(filename,"r") as f0:
                        for name in names:
                            variable = f0.variables[name]
                            variables[name] = variable[:]
                            dimensions[name]=variable.dimensions
        return variables

    def to_cache_path(self, ddate: datetime,dim1: Dict, dim2: Dict) -> Path:
        """Convert a date and two dimensions to a path in the cache"""
        year = ddate.strftime("%Y")
        month = ddate.strftime("%m")
        day = ddate.strftime("%d")
        hour = ddate.strftime("%H")
        idx1 = next(iter(dim1.values()))
        idx2 = next(iter(dim2.values()))
        filename = f"{idx1},{idx2}.nc"
        return Path(f"{self.location}/{year}/{month}/{day}/{hour}/{filename}")
