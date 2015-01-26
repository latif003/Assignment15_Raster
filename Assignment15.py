# Team Nikoula: Latifah & Nikos
# Date: 26/1/2015

# import modules
import os
from osgeo import gdal
from osgeo.gdalconst import GA_ReadOnly, GDT_Float32
import numpy as np

os.getcwd() # finding working directory

# Open Landsat satellite images
driver = gdal.GetDriverByName('GTiff')

b4 = gdal.Open('data/LC81980242014260LGN00_sr_band4.tif')
b5 = gdal.Open('data/LC81980242014260LGN00_sr_band5.tif')

# derive information from the images
b4.RasterXSize #band4
b4.RasterYSize
b4.RasterCount
b4.GetProjection()
b5.RasterXSize #band5
b5.RasterYSize
b5.RasterCount
b5.GetProjection()

# Reading band's per array and chanding the store type into float
band4 = b4.GetRasterBand(1)
band5 = b5.GetRasterBand(1)
band4Arr = band4.ReadAsArray(0, 0, b4.RasterXSize, b4.RasterYSize)
band5Arr = band5.ReadAsArray(0, 0, b5.RasterXSize, b5.RasterYSize)
band4Arr = band4Arr.astype(np.float32)
band5Arr = band5Arr.astype(np.float32)

# Create the mask layer
mask = np.greater(band4Arr+band5Arr, 0)

# Calculate NDWI
ndwi = np.choose(mask,(-99,(band4Arr-band5Arr)/(band4Arr+band5Arr)))
print "NDWI min and max values", ndwi.min(), ndwi.max()

# Create an image as an output
outDataSet = driver.Create('data/NDWI.tif', b4.RasterXSize, b4.RasterYSize, 1, GDT_Float32)
outBand = outDataSet.GetRasterBand(1)
outBand.WriteArray(ndwi, 0, 0)
outBand.SetNoDataValue(-99)
outBand.FlushCache()
outDataSet.FlushCache()
