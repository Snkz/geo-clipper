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

    if len(sys.argv) < 6:
        print("Usage %s raster.tif top_x top_y bot_x bot_y" % sys.argv[0])
        sys.exit(1)
    
    
    raster = sys.argv[1]

    top_x = float(sys.argv[2]) 
    top_y = float(sys.argv[3]) 
    bot_x = float(sys.argv[4])  
    bot_y = float(sys.argv[5]) 
    
    
    print("Clipping %s, bounding box btwn (%d, %d) and (%d, %d)." %(raster, top_x, top_y, bot_x, bot_y))
    
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
    driver = gdal.GetDriverByName('GTiff');
    dataset = driver.Create(
            "%s.out.%d.%d.tif" %(raster, top_x, top_y),
            (bot_x - top_x)*(1.0/pxW),
            (bot_y - top_y)*(1.0/pxW),
            4,
            gdal.GDT_Byte,
            )

    dataset.SetGeoTransform((
        top_x,
        pxW,
        rotx,
        top_y,
        roty,
        pxH))

    dataset.GetRasterBand(1).WriteArray(bandList[0,top_x*(1/pxW):bot_x*(1/pxW),top_y*(1/pxH):bot_y*(1/pxH)])
    dataset.GetRasterBand(2).WriteArray(bandList[1,top_x*(1/pxW):bot_x*(1/pxW),top_y*(1/pxH):bot_y*(1/pxH)])
    dataset.GetRasterBand(3).WriteArray(bandList[2,top_x*(1/pxW):bot_x*(1/pxW),top_y*(1/pxH):bot_y*(1/pxH)])
    dataset.GetRasterBand(4).WriteArray(bandList[3,top_x*(1/pxW):bot_x*(1/pxW),top_y*(1/pxH):bot_y*(1/pxH)])

    dataset.SetProjection(proj)
    
    dataset.FlushCache()
    #Gdalnumeric.SaveArray(bandList[:,chunkx:chunkxUP,chunky:chunkyUP], 
    #        "%s.out.%d.%d.tif" %(raster, j, i), 
    #        format="GTiff", prototype=raster)
