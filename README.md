# ZCTA Impacts

A project for the [2021 Sustainable Communities Web Challenge](https://model.earth/community/challenge/).
Generates Environmental Footprint ["Nutrition Labels"](https://model.earth/io/template/) for communities in the USA.

## Live Site

The CI process publishes new builds to: https://zctaimpacts.abrie.dev

You are able to visit the live site for a UI, or query it using the API:

`curl -X POST -H "Content-Type: application/json" -d '{"statefp":17,"countyfp":31}' http://localhost:5000/query/county/impacts`


## Create Virtual Environment

    python3 -m venv .venv

OSX / Linux:

	source .venv/bin/activate

Windows:

	\.venv\Scripts\activate.bat

### Install Requirements.txt

    pip install -r requirements.txt

### Download File

Download this file since it's too big for GitHub at 528 MB  
https://www2.census.gov/geo/tiger/TIGER2020/ZCTA520/  
Add to: backend/utils/spatial/downloads/tl_2020_us_zcta520.zip  

## Self Hosting

There are two options: Docker, or from source. Both options require API keys and a local copy of the database.


### First, The Database
The finished database is about 220 megabytes, and must be built from scratch. A utility script is provided:
1. `cd backend/utils/spatial`
2. Execute `./build.sh`

BUG - The following error occurs:  
./build.sh: line 13: spatialite: command not found

<!--
If a small topojson file for zipcode boundaries is needed:
https://model.earth/community/zip/leaflet/#columns=JobsAgriculture:50;JobsManufacturing:50
-->

3. Copy the resulting file `out/db.spatialite` file to `backend/instance`

### Next, API Keys
The app queries the Census.gov API for County Business Patterns information. This app needs an API key do that.
1. [Get one here](https://api.census.gov/data/key_signup.html).
2. Copy `backend/secrets.json` to `backend/instance` and your your API key to it.

### Option 1: Use Docker
1. `docker run -v{/full/path/to/instance/folder}:/backend/instance abriedev/zctaimpacts` will serve on port 80.

### Option 2: Run from source

1. Install backend dependencies: `cd backend && python -m pip install --upgrade pip`
2. Start the backend: `cd backend && make serve`
3. Install frontend dependencies: `yarn`
4. Start the frontend: `cd frontend && yarn start`
5. Access the site through `http://localhost:3000`
