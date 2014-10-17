import sys, os, time

# osgeo is the top level package
import gdal #geo spatial tool. Requires libgdal
import gdalnumeric
from gdalconst import *

import numpy

gdal.AllRegister()

def readGeoImage(image, rows, cols, bands):
    pass
        
    
if __name__ == '__main__':

    if len(sys.argv) < 2:
        print "Please input geotiff file name"
        sys.exit(1)
    
    
    width = 2
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

    # Image dimensions
    print(rows, cols, bands)
    
    transform = image.GetGeoTransform()
    proj = image.GetProjection()

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
    
    
    bandList = numpy.array(bandList)

    rangex = cols/width
    rangey = rows/height

    print(rangex, rangey)

    driver = gdal.GetDriverByName('GTiff');
    
    for j in range(height):
        for i in range(width):
    
            # save chunks of the image at a time
            chunkx = rangex*i
            chunkxUP = rangex*(i+1)
    
            chunky = rangey*j
            chunkyUP = rangey*(j+1)
    
            if chunkxUP > cols:
                chunkxUP = cols
    
            if chunkyUP > rows:
                chunky = rows
    
            assert((chunkyUP - chunky) <= rangey)
            assert((chunkxUP - chunkx) <= rangex)
    
            dataset = driver.Create(
                    "%s.out.%d.%d.tif" %(raster.split(".")[0], j, i),
                    (chunkxUP - chunkx),
                    (chunkyUP - chunky),
                    4,
                    gdal.GDT_Byte,
                    )

            dataset.SetGeoTransform((
                xOrg + chunkx*(pxW),
                pxW,
                rotx,
                yOrg + chunky*(pxH),
                roty,
                pxH))

            print(chunky,chunkyUP,chunkx,chunkxUP)
            dataset.GetRasterBand(1).WriteArray(bandList[0,chunky:chunkyUP,chunkx:chunkxUP])
            dataset.GetRasterBand(2).WriteArray(bandList[1,chunky:chunkyUP,chunkx:chunkxUP])
            dataset.GetRasterBand(3).WriteArray(bandList[2,chunky:chunkyUP,chunkx:chunkxUP])
            dataset.GetRasterBand(4).WriteArray(bandList[3,chunky:chunkyUP,chunkx:chunkxUP])

            dataset.SetProjection(proj)
            
            dataset.FlushCache()
            #Gdalnumeric.SaveArray(bandList[:,chunkx:chunkxUP,chunky:chunkyUP], 
            #        "%s.out.%d.%d.tif" %(raster, j, i), 
            #        format="GTiff", prototype=raster)
