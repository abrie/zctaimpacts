#!/bin/bash
set -ue
ZCTA_SHAPEFILE=tl_2020_us_zcta520
COUNTY_SHAPEFILE=tl_2020_us_county
STATE_SHAPEFILE=tl_2020_us_state
DB=db.spatialite
rm -rf out
mkdir -p out
rm -rf raw
mkdir raw
unzip downloads/$ZCTA_SHAPEFILE.zip -d raw
npx mapshaper raw/$ZCTA_SHAPEFILE.shp -simplify dp 2% -o force format=shapefile out/$ZCTA_SHAPEFILE.shp
echo ".loadshp out/$ZCTA_SHAPEFILE zcta_shp UTF8 4326" | spatialite out/$DB
echo "SELECT CreateSpatialIndex('zcta_shp', 'geometry');" | spatialite out/$DB
npx mapshaper raw/$ZCTA_SHAPEFILE.shp -simplify dp 10% -o force format=geojson out/$ZCTA_SHAPEFILE.json
geojson-to-sqlite out/$DB zcta_geojson out/$ZCTA_SHAPEFILE.json

unzip downloads/$COUNTY_SHAPEFILE.zip -d raw
npx mapshaper raw/$COUNTY_SHAPEFILE.shp -simplify dp 2% -o force format=shapefile out/$COUNTY_SHAPEFILE.shp
echo ".loadshp out/$COUNTY_SHAPEFILE county_shp UTF8 4326" | spatialite out/$DB
echo "SELECT CreateSpatialIndex('county_shp', 'geometry');" | spatialite out/$DB
npx mapshaper raw/$COUNTY_SHAPEFILE.shp -simplify dp 10% -o force format=geojson out/$COUNTY_SHAPEFILE.json
geojson-to-sqlite out/$DB county_geojson out/$COUNTY_SHAPEFILE.json

unzip downloads/$STATE_SHAPEFILE.zip -d raw
npx mapshaper raw/$STATE_SHAPEFILE.shp -simplify dp 2% -o force format=shapefile out/$STATE_SHAPEFILE.shp
echo ".loadshp out/$STATE_SHAPEFILE state_shp UTF8 4326" | spatialite out/$DB
echo "SELECT CreateSpatialIndex('state_shp', 'geometry');" | spatialite out/$DB
npx mapshaper raw/$STATE_SHAPEFILE.shp -simplify dp 10% -o force format=geojson out/$STATE_SHAPEFILE.json
geojson-to-sqlite out/$DB state_geojson out/$STATE_SHAPEFILE.json

sqlite3 -csv out/$DB ".import downloads/county_fips_master.csv county_fips"
sqlite3 -csv out/$DB ".import downloads/state_fips_master.csv state_fips"
