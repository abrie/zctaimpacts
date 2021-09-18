#!/bin/bash
set -ue
ZCTA_SHAPEFILE=tl_2020_us_zcta520
COUNTY_SHAPEFILE=tl_2020_us_county
DB=db.spatialite
rm -rf out
mkdir -p out
npx mapshaper raw/$ZCTA_SHAPEFILE.shp -simplify dp 2% -o force format=shapefile out/$ZCTA_SHAPEFILE.shp
echo ".loadshp out/$ZCTA_SHAPEFILE zcta_shp UTF8 4326" | spatialite out/$DB
echo "SELECT CreateSpatialIndex('zcta_shp', 'geometry');" | spatialite out/$DB
npx mapshaper raw/$ZCTA_SHAPEFILE.shp -simplify dp 10% -o force format=geojson out/$ZCTA_SHAPEFILE.json
geojson-to-sqlite out/$DB zcta_geojson out/$ZCTA_SHAPEFILE.json

npx mapshaper raw/$COUNTY_SHAPEFILE.shp -o force format=shapefile out/$COUNTY_SHAPEFILE.shp
echo ".loadshp out/$COUNTY_SHAPEFILE county_shp UTF8 4326" | spatialite out/$DB
echo "SELECT CreateSpatialIndex('county_shp', 'geometry');" | spatialite out/$DB
npx mapshaper raw/$COUNTY_SHAPEFILE.shp -o force format=geojson out/$COUNTY_SHAPEFILE.json
geojson-to-sqlite out/$DB county_geojson out/$COUNTY_SHAPEFILE.json
