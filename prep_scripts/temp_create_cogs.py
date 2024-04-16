from osgeo import gdal, gdalconst, gdal_array
import os
from pathlib import Path
import numpy as np


# subsets = ['WA_BucklandFireScar_20210627_7cm_02', 'WA_BucklandFireScar_20210627_7cm_03', 'WA_BucklandFireScar_20210627_7cm_04', 'WA_BucklandFireScar_20210627_7cm_05', 'WA_BucklandFireScar_20210627_7cm_06',
#            'WA_NoatakValleyN_20210702_7cm_01', 'WA_NoatakValleyN_20210702_7cm_02', 'WA_NoatakValleyN_20210702_7cm_03', 'WA_NoatakValleyN_20210702_7cm_04', 'WA_NoatakValleyS_20210702_20cm_01',
#            'WA_NoatakValleyS_20210702_20cm_02', 'WA_NoatakValleyS_20210702_20cm_03']
subsets = ['WA_NoatakValleyS_20210702_20cm_01', 'WA_NoatakValleyS_20210702_20cm_02', 'WA_NoatakValleyS_20210702_20cm_03']

for subset in subsets:
    print(subset)
    # input_folder = f'/isipd/projects-noreplica/p_macsprocessing/data_products/{subset}/'
    # input_folder = f'E:/02_macs_fire_sites/00_working/00_orig-data/02_macs_mosaics/MACS_water/'
    # tiles_folder = f'E:/02_macs_fire_sites/00_working/03_code_scripts/IWD_graph_analysis/data_arf/'


    # vrt = f'E:/02_macs_fire_sites/00_working/00_orig-data/02_macs_mosaics/MACS_orthos/{subset}_macs_ortho.vrt'
    vrt = f'S:/data_products/{subset}/Ortho.vrt'
    cog = f'E:/02_macs_fire_sites/00_working/00_orig-data/02_macs_mosaics/MACS_orthos/{subset}_macs_ortho_cog.tif'

    # flist = list(Path(input_folder).glob('*.tif'))

    # with open('flist.txt', 'w') as filetext:
    #     [filetext.write(f.as_posix() + '\n') for f in flist[:]]
    # os.system(f'gdalbuildvrt -input_file_list flist.txt {vrt}')
    # os.remove('flist.txt')

    os.system(f'gdal_translate -of COG -co BIGTIFF=YES -co NUM_THREADS=ALL_CPUS -co COMPRESS=DEFLATE {vrt} {cog}')
    # os.system(f'cp {cog} /isipd/projects-noreplica/p_trettel/cross_resolution/c_water_segmentation_unet/raster_continuous/')
    os.remove(f'{vrt}')