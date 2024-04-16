from osgeo import gdal
import numpy as np
import os
import rasterio
from skimage import morphology
import pdb

from skimage.filters import threshold_otsu

def main():
    directory = f'E:/02_macs_fire_sites/00_working/00_orig-data/02_macs_mosaics/MACS_orthos/'
    
    for root, dirs, files in os.walk(f'{directory}'):
        for filename in files:
            # print(filename)
            if '_macs_ortho_cog.tif' in filename and 'WA_NoatakValleyS' in filename:
                print(filename)
                ortho_file = root + filename
                water_dir = f'E:/02_macs_fire_sites/00_working/00_orig-data/02_macs_mosaics/MACS_water/'
                if not os.path.exists(water_dir):
                    os.makedirs(water_dir)
                water_file = f'{water_dir}{filename[:-14]}_water.tif'
                outfile = water_file 


                with rasterio.open(ortho_file) as src:
                    profile = src.profile
                    img = src.read(4)
                    profile.update(dtype=rasterio.uint8,
                                   count=1,
                                   nodata=255
                                   )

                thresh = threshold_otsu(img)
                water = img <= thresh
                water2 = morphology.remove_small_objects(water, min_size=100, connectivity=2)
                
                with rasterio.open(outfile, 'w', **profile) as dst:
                    dst.write(np.expand_dims(water2, 0).astype(rasterio.uint8))


if __name__ == '__main__':
    main()
