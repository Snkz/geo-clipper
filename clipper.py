import sys, os, time

# osgeo is the top level package
import gdal #geo spatial tool. Requires libgdal
import gdalnumeric
from gdalconst import *

import numpy

gdal.AllRegister()

def readGeoImage(image, rows, cols, bands):
        
    # Image dimensions
    print(rows, cols, bands)
    
    transform = image.GetGeoTransform()
    xOrg = transform[0]
    yOrg = transform[3]
    rotx = transform[2]
    roty = transform[4]
    pxW = transform[1]
    pxH = transform[5]
    
    # Geo Spatial dimensions
    print(xOrg, yOrg, pxW, pxH);
    # Rotations
    print(rotx, roty)
    assert(rotx == roty == 0.0)
    
    bandList = []
    
    for i in range(bands):
        band = image.GetRasterBand(i+1)
        data = band.ReadAsArray(0, 0, cols, rows)
        bandList.append(data)
    
    
    return numpy.array(bandList)

if __name__ == '__main__':

    if len(sys.argv) < 2:
        print "Please input geotiff file name"
        sys.exit(1)
    
    
    width = 3
    height = 2
    raster = sys.argv[1]
    
    if len(sys.argv) == 4:
        width = int(sys.argv[2])
        height = int(sys.argv[3])
    
    
    print("Clipping %s, %d times in x and %d times in y." %(raster, width, height))
    
    image = gdal.Open(raster, GA_ReadOnly);
    if image is None:
        print("Could not open image")
        sys.exit(1)
    else:
        print("Opened Image succesfully!")
    
    rows = image.RasterYSize
    cols = image.RasterXSize
    bands = image.RasterCount

    bandList = readGeoImage(image, rows, cols, bands)
    rangex = rows/width
    rangey = cols/height
    
    for j in range(height):
        for i in range(width):
    
            # save chunks of the image at a time
            chunkx = rangex*i
            chunkxUP = rangex*(i+1)
    
            chunky = rangey*j
            chunkyUP = rangey*(j+1)
    
            if chunkyUP > cols:
                chunkyUP = cols
    
            if chunkxUP > rows:
                chunkx = rows
    
            assert((chunkyUP - chunky) <= rangey)
            assert((chunkxUP - chunkx) <= rangex)
    
            gdalnumeric.SaveArray(bandList[:,chunkx:chunkxUP,chunky:chunkyUP], 
                    "%s.out.%d.%d.tif" %(raster, j, i), 
                    format="GTiff", prototype=raster)
