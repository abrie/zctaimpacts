DB=db.spatialite
ZCTA_SHAPEFILE=tl_2020_us_zcta520
COUNTY_SHAPEFILE=tl_2020_us_county
STATE_SHAPEFILE=tl_2020_us_state
STATE_FIPS=states_fips_master
COUNTY_FIPS=county_fips_master

downloads:
	mkdir -p downloads
	curl -o downloads/${COUNTY_SHAPEFILE}.zip https://www2.census.gov/geo/tiger/TIGER2020/COUNTY/tl_2020_us_county.zip
	curl -o downloads/${ZCTA_SHAPEFILE}.zip https://www2.census.gov/geo/tiger/TIGER2020/ZCTA520/tl_2020_us_zcta520.zip
	curl -o	downloads/${STATE_SHAPEFILE}.zip https://www2.census.gov/geo/tiger/TIGER2020/STATE/tl_2020_us_state.zip
	curl -o downloads/${STATE_FIPS}.csv https://raw.githubusercontent.com/kjhealy/fips-codes/master/state_fips_master.csv
	curl -o downloads/${COUNTY_FIPS}.csv	https://raw.githubusercontent.com/kjhealy/fips-codes/master/county_fips_master.csv

clean:
	rm -rf out
	rm -rf raw

zctas:
	unzip downloads/$(ZCTA_SHAPEFILE).zip -d raw
	npx mapshaper raw/$(ZCTA_SHAPEFILE).shp -simplify dp 2% -o force format=shapefile out/$(ZCTA_SHAPEFILE).shp
	echo ".loadshp out/$(ZCTA_SHAPEFILE) zcta_shp UTF8 4326" | spatialite out/$(DB)
	echo "SELECT CreateSpatialIndex('zcta_shp', 'geometry');" | spatialite out/$(DB)
	npx mapshaper raw/$(ZCTA_SHAPEFILE).shp -simplify dp 10% -o force format=geojson out/$(ZCTA_SHAPEFILE).json
	geojson-to-sqlite out/$(DB) zcta_geojson out/$(ZCTA_SHAPEFILE).json

counties:
	unzip downloads/$(COUNTY_SHAPEFILE).zip -d raw
	npx mapshaper raw/$(COUNTY_SHAPEFILE).shp -simplify dp 2% -o force format=shapefile out/$(COUNTY_SHAPEFILE).shp
	echo ".loadshp out/$(COUNTY_SHAPEFILE) county_shp UTF8 4326" | spatialite out/$(DB)
	echo "SELECT CreateSpatialIndex('county_shp', 'geometry');" | spatialite out/$(DB)
	npx mapshaper raw/$(COUNTY_SHAPEFILE).shp -simplify dp 10% -o force format=geojson out/$(COUNTY_SHAPEFILE).json
	geojson-to-sqlite out/$(DB) county_geojson out/$(COUNTY_SHAPEFILE).json

states:
	unzip downloads/$(STATE_SHAPEFILE).zip -d raw
	npx mapshaper raw/$(STATE_SHAPEFILE).shp -simplify dp 2% -o force format=shapefile out/$STATE_SHAPEFILE.shp
	echo ".loadshp out/$(STATE_SHAPEFILE) state_shp UTF8 4326" | spatialite out/$(DB)
	echo "SELECT CreateSpatialIndex('state_shp', 'geometry');" | spatialite out/$(DB)
	npx mapshaper raw/$(STATE_SHAPEFILE).shp -simplify dp 10% -o force format=geojson out/$(STATE_SHAPEFILE).json
	geojson-to-sqlite out/$(DB) state_geojson out/$(STATE_SHAPEFILE).json

fips:
	sqlite3 -csv out/$(DB) ".import downloads/$(COUNTY_FIPS).csv county_fips"
	sqlite3 -csv out/$(DB) ".import downloads/$(STATE_FIPS).csv state_fips"

all: clean zctas counties states fips
