#!/usr/bin/env python3

import numpy as np
from scipy.spatial import cKDTree
# from bluesmet.met.nora3.field import Field
# from bluesmet.met.nora3.fieldpoint import FieldPoint


# def __calculate_true_lon_lat(ds):
#     dvars = ds.variables
#     rlon = dvars["rlon"]
#     rlat = dvars["rlat"]
#     proj = dvars["projection_ob_tran"]
#     rlon, rlat = np.meshgrid(rlon, rlat, sparse=False, indexing="ij")
#     tf = pyproj.Transformer.from_crs(proj.proj4, "epsg:4326", always_xy=True)
#     # pylint: disable=unpacking-non-sequence
#     lon, lat = tf.transform(rlon, rlat)
#     return lon, lat



def nearest(lat,lon, lat_pos, lon_pos):
    """Function to find index to nearest point """
    M = np.c_[np.ravel(lon), np.ravel(lat)]
    tree = cKDTree(M)
    _, ii = tree.query([lon_pos, lat_pos], k=1)
    idy, idx = np.where((lon == M[ii][0]) & (lat == M[ii][1]))
    return int(idx), int(idy)


# def find_nearest(field: Field, lat, lon):
#     """Find nearest wind hindcast coordinates"""

#     f_lon = field.longitude
#     f_lat = field.latitude

#     for (lat_pos,lon_pos) in zip(f_lat,f_lon):
#         idx,idy = nearest(lat,lon,lat_pos,lon_pos)
#         grid_lon_pkt=float(lon[idy,idx])
#         grid_lat_pkt=float(lat[idy,idx])
#         field.points.append(FieldPoint(latitude=grid_lat_pkt,longitude=grid_lon_pkt))
