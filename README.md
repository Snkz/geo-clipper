geo-clipper
===========

Clip geospatial images into smaller chunks

requires: libgdal and gdal python wrapper.
```bash
USAGE: python range_clipper.py mynmar_copy.tif  200821.400 2316187.200 204283.900 2313922.700
USAGE: python grid_clipper.py mynmar_copy.tif 10 10
```

Expects lat/lng values projected to geotif's plane for range clipping (top\_x, top\_y), (bot\_x, bot\_y).
