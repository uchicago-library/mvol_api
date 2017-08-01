# mvol_api
An API for mvol project specific information, backed by the digcollretriever and knowledge of the mvol filesystem specification.

## Endpoints

## <identifier>/nav

Returns what identifiers compose this object
Mvol identifier --> Volumes
volume identifier --> issues
Issue identifier --> pages

## <identifier>/ocr

### Required Paramters
* jpg_height: The height of the jpg derivative created in pixels
* jpg_width: The width of the jpg derivative created in pixels

Returns an IA book reader compliant xtf ocr file
