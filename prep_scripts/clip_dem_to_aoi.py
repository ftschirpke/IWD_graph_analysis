import fiona
import rasterio
import rasterio.mask
# from osgeo import gdal, ogr
from datetime import datetime
import glob


startTime = datetime.now()


def clip_raster_to_aoi(path_aoi, path_dem):
    # print(path_aoi)
    # print(path_dem)
    name_aoi = path_aoi[89:93] + path_aoi[97:-12] + path_aoi[-6:-4]
    print(name_aoi)

    # OutTile = gdal.Warp(r'E:\02_macs_fire_sites\00_working\00_orig-data\03_lidar\product-dem\dtm_1m\cut_to_aoi\PERMAX_1_epsg32603_to_sa_csp_025_54-71_32603_a.tif',
    #                     path_dem,
    #                     cutlineDSName=path_aoi,
    #                     cropToCutline=True,
    #                     dstNodata=0)
    #
    # OutTile = None

    output_raster_path = output_raster_path = (r'E:\02_macs_fire_sites\00_working\00_orig-data\03_lidar\product-dem\dtm_1m\proj\cut_to_aoi\PERMAX5_epsg32604_' + name_aoi + '.tif')
    # print(output_raster_path)

    with fiona.open(path_aoi, "r") as shapefile:
        shapes = [feature["geometry"] for feature in shapefile]

    with rasterio.open(path_dem) as src:
        out_image, out_transform = rasterio.mask.mask(src, shapes, crop=True)
        out_meta = src.meta

    out_meta.update({"driver": "GTiff",
                     "height": out_image.shape[1],
                     "width": out_image.shape[2],
                     "transform": out_transform})

    with rasterio.open(output_raster_path, "w", **out_meta) as dest:
        dest.write(out_image)


if __name__ == '__main__':
    path_dem = r'E:\02_macs_fire_sites\00_working\00_orig-data\03_lidar\product-dem\dtm_1m\proj\PERMAX5_epsg32604.tif'
    path_aoi = r'E:\02_macs_fire_sites\00_working\01_processed-data\00_study_area_shp\sa_025_firescars'
    # path_aoi2 = r'E:\02_macs_fire_sites\00_working\01_processed-data\00_study_area_shp\sa_025_firescars\sa_csp_025_54-71_32603_b.shp'
    # name_aoi = path_aoi[86:-4]
    #
    # print(name_aoi)
    # print(output_raster_path)
    count = 0

    for filename in glob.iglob(f'{path_aoi}/sa_noa_025_12*.shp'):
        print(filename)
        clip_raster_to_aoi(filename, path_dem)
        print("-------")
        count += 1

    print(count)

    # clip_raster_to_aoi(path_aoi, path_dem)


    # print time needed for script execution
    print(datetime.now() - startTime)