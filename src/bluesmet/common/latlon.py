import numpy as np
from scipy.spatial import cKDTree

# def calculate_true_lon_lat(ds):
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
