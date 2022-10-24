import cv2
import numpy as np
from PIL import Image
import sys
import scipy
import scipy.ndimage
from skimage.morphology import skeletonize, skeletonize_3d
from scipy.ndimage.morphology import generate_binary_structure
import sknw
import networkx as nx
from scipy import ndimage
import gdal
from osgeo import gdal_array
from affine import Affine
import matplotlib.pyplot as plt
import glob
from pathlib import Path
from datetime import datetime

startTime = datetime.now()

def write_geotiff(out_ds_path, arr, in_ds):
    ''' takes an np.array with pixel coordinates and
    gives it the projection of another raster.
    np.array must have same extent as georeferenced
    raster.

    :param out_ds_path: string of path and filename
    where to save the newly georeferenced raster (tif).
    :param arr: the array to georeference
    :param in_ds: the already georeferenced dataset
    that serves as reference for the arr to geore-
    ference.
    :return NA: function just for saving
    '''
    if arr.dtype == np.float32:
        arr_type = gdal.GDT_Float32
    else:
        arr_type = gdal.GDT_Int32

    driver = gdal.GetDriverByName("GTiff")
    out_ds = driver.Create(out_ds_path, arr.shape[1], arr.shape[0], 1, arr_type)
    # print(in_ds.GetProjection())
    # print(arr)
    proj = in_ds.GetProjection()
    out_ds.SetProjection(proj)
    out_ds.SetGeoTransform(in_ds.GetGeoTransform())
    band = out_ds.GetRasterBand(1)
    band.WriteArray(arr)
    band.FlushCache()


def fill_outliers(raster_ds_path, trend_size):
    # read in digital terrain model. once as georeferenced
    # raster, once as spatial-less np.array.
    dtm = gdal.Open(raster_ds_path)
    dtm_np = gdal_array.LoadFile(raster_ds_path)
    fname = (Path(raster_ds_path).stem)
    print(fname)

    # plt.Figure()
    # plt.imshow(dtm_np)
    # plt.show()

    subset = dtm_np[:, :]
    reg_trend = ndimage.median_filter(subset, size=trend_size)

    # plt.Figure()
    # plt.imshow(reg_trend)
    # plt.show()

    write_geotiff('E:/02_macs_fire_sites/00_working/01_processed-data/01_study_area_raster/cut_to_aoi_filled/' + fname + '_filled3.tif', reg_trend, dtm)


if __name__ == "__main__":
    for raster_ds_path in glob.iglob(r'E:\02_macs_fire_sites\00_working\00_orig-data\03_lidar\product-dem\dtm_1m\cut_to_aoi\*.tif'):
        fill_outliers(raster_ds_path, 3)
    # raster_ds_path = r"E:\02_macs_fire_sites\00_working\00_orig-data\03_lidar\product-dem\dtm_1m\cut_to_aoi\PERMAX_1_epsg32603_to_sa_csp_025_54_32603.tif"


    # print time needed for script execution
    print(datetime.now() - startTime)
