# Build a Spatialite Database of ZCTA areas with associated GeoJSON polygons

1. Download the US Census zipcode cartographic areas (ZCTA)
  https://www2.census.gov/geo/tiger/TIGER2020/ZCTA520/tl_2020_us_zcta520.zip
  * The record layout is described by this document:https://www2.census.gov/geo/pdfs/maps-data/data/tiger/tgrshp2021/TGRSHP2021_TechDoc.pdf

2. Run the `build.sh` script to build the spatialite database.

3. Some sample queries:
```
select * from zcta_shp where MBRContains(BuildMBR(-85.605165, 30.357851, -80.839729, 35.000659, 4326), "geometry");
```

* This returns the zipcode and geojson feature off all ZCTAs in Georgia
```
SELECT zcta_geojson.ZCTA5CE20, zcta_geojson.geometry from zcta_geojson inner join (select ZCTA5CE20 from zcta_shp where MBRContains(BuildMBR(-85.605165, 30.357851, -80.839729, 35.000659, 4326), "geometry")) as zcta_shp ON zcta_geojson.ZCTA5CE20 = zcta_shp.ZCTA5CE20;
```

# FIPS code translations
https://raw.githubusercontent.com/kjhealy/fips-codes/master/county_fips_master.csv
https://raw.githubusercontent.com/kjhealy/fips-codes/master/state_fips_master.csv
