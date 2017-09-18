# mvol_api

v0.0.1

[![Build Status](https://travis-ci.org/uchicago-library/mvol_api.svg?branch=master)](https://travis-ci.org/uchicago-library/mvol_api) [![Coverage Status](https://coveralls.io/repos/github/uchicago-library/mvol_api/badge.svg?branch=master)](https://coveralls.io/github/uchicago-library/mvol_api?branch=master)

An API for mvol project specific information, backed by the digcollretriever and knowledge of the mvol filesystem specification.

# Debug Quickstart
Set environmental variables appropriately
```
./debug.sh
```

# Docker Quickstart
Inject environmental variables appropriately at either buildtime or runtime
```
# docker build . -t mvol_api
# docker run -p 5000:80 mvol_api --name my_mvol_api
```

# Endpoints
## /
Returns 

```
{"status": "Not broken!"}
```

## /$identifier/nav

Returns what identifiers compose this object
* Mvol identifier --> Volumes
* volume identifier --> issues
* Issue identifier --> pages

## /$identifier/ocr

### Required URL Paramters
* jpg_height: The height of the jpg derivative created in pixels
* jpg_width: The width of the jpg derivative created in pixels
* min_year: The minimum year to populate the IA OCR meta element
* max_year: The maximum year to populate the IA OCR meta element

Returns an IA book reader compliant xtf ocr file

# Environmental Variables
## Global Required Env Vars
* MVOL_API_MVOL_ROOT: The filesystem path to the directory which contains the "mvol" directory.
* MVOL_API_RETRIEVER_URL: The URL at which the digcoll_retriever API can be accessed, including the port number in the URL if not 80. eg: MVOL_API_RETRIEVER_URL=localhost:5000

## Global Optional Env Vars
* MVOL_API_VERBOSITY: Controls the logging verbosity 

# Example of how to run for testing/demos
First, run the digcoll_retriever API on the same host bound to port 5001. Then...
```
MVOL_API_MVOL_ROOT=/home/brian/sandbox/mock_oc_root/data/ldr_oc_admin/files/Preservation\ Unit/ MVOL_API_RETRIEVER_URL=http://localhost:5001/ MVOL_API_VERBOSITY=DEBUG bash debug.sh
```


# Author
Brian Balsamo <balsamo@uchicago.edu>
