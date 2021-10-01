# Build a Spatialite Database required by the ZCTAImpacts App

1. Download all necessary files listed in `resources.txt`
```
xargs -n 1 curl --create-dirs -O --output-dir downloads < ../resources.txt
```

2. Run the `build.sh` script to build the spatialite database.

3. Copy the resulting `out/db.spatialite` to the folder used for flask instance files.
