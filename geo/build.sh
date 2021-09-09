#!/bin/bash
set -ue
DB=db.sqlite3
rm -f $DB
npx mapshaper raw/tl_2020_us_zcta520.shp -simplify dp 2% -o force format=shapefile raw/simplified.shp
echo ".loadshp raw/simplified zcta_shp ASCII 4326" | spatialite $DB
echo "SELECT CreateSpatialIndex('zcta_shp', 'geometry');" | spatialite $DB
npx mapshaper raw/tl_2020_us_zcta520.shp -simplify dp 10% -o force format=geojson raw/simplified.json
geojson-to-sqlite $DB zcta_geojson raw/simplified.json
