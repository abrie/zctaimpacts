HOST=http://localhost:5000
#HOST=https://zctaimpacts.abrie.dev
#!/bin/bash
#curl -X POST -H "Content-Type: application/json" -d '{ "x1": -84.66133117675783, "y1": 33.93196649986436, "x2": -84.14497375488283, "y2": 33.695208841799214 }' ${HOST}/query/zcta/mbr

#curl -X POST -H "Content-Type: application/json" -d '{"zipcode":"30309"}' http://localhost:5000/query/naics

#curl -X POST -H "Content-Type: application/json" -d '{"zipcode":"90210"}' http://localhost:5000/query/zipcode
curl -X POST -H "Content-Type: application/json" -d '{"statefp":17,"countyfp":31}' http://localhost:5000/query/county/impacts

#curl -X POST -H "Content-Type: application/json" -d '{}' http://localhost:5000/query/useeio/sectors

#curl -X POST -H "Content-Type: application/json" -d '{}' http://localhost:5000/query/useeio/matrices
