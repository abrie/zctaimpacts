#!/bin/bash
set -ue
SHAPEFILE=tl_2020_us_zcta520
DB=db.spatialite
rm -rf out
mkdir -p out
npx mapshaper raw/$SHAPEFILE.shp -simplify dp 2% -o force format=shapefile out/$SHAPEFILE.shp
echo ".loadshp out/$SHAPEFILE zcta_shp ASCII 4326" | spatialite out/$DB
echo "SELECT CreateSpatialIndex('zcta_shp', 'geometry');" | spatialite out/$DB
npx mapshaper raw/$SHAPEFILE.shp -simplify dp 10% -o force format=geojson out/$SHAPEFILE.json
geojson-to-sqlite out/$DB zcta_geojson out/$SHAPEFILE.json
