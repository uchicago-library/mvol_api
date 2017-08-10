# mvol_api
An API for mvol project specific information, backed by the digcollretriever and knowledge of the mvol filesystem specification.

# Environmental Variables

## Global Required Env Vars
* MVOL_API_MVOL_ROOT: The filesystem path to the directory which contains the "mvol" directory.
* MVOL_API_RETRIEVER_URL: The URL at which the digcoll_retriever API can be accessed, including the port number in the URL if not 80. eg: MVOL_API_RETRIEVER_URL=localhost:5000

## Global Optional Env Vars
* MVOL_API_VERBOSITY: Controls the logging verbosity 
* MVOL_API_HOST: The host address for gunicorn to bind to if using gunicorn_debug.sh. Defaults to 0.0.0.0
* MVOL_API_PORT: The port for gunicorn to bind to if using gunicorn_debug.sh. Defaults to 5000.
* MVOL_API_WORKERS: The number of workers for gunicorn to spawn if using gunicorn_debug.sh. Defaults to 4
* MVOL_API_TIMEOUT: The time, in seconds, for gunicorn to wait before timing out a connection if using gunicorn_debug.sh. Defaults to 30.

# Example of how to run for testing/demos
First, run the digcoll_retriever API on the same host bound to port 5001. Then...
```
MVOL_API_MVOL_ROOT=/home/brian/sandbox/mock_oc_root/data/ldr_oc_admin/files/Preservation\ Unit/ MVOL_API_RETRIEVER_URL=http://localhost:5001/ MVOL_API_VERBOSITY=DEBUG bash debug.sh
```

## Endpoints

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

Returns an IA book reader compliant xtf ocr file
