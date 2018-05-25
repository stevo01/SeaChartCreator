generation of chart bundles:
- fetch tiles
- merge tiles
- stich tiles
- generate chart bundle 


# Fetch Tiles
Input Data:
 - atlas xml specification
 - database with tiles and meta data (date and etag)
  
Output Data:
 - database with tiles and meta data (date and etag)
 - update flag (indicate if new tile was received)

Process description:
  Download tiles based on atlas xml specification and store it in database(s).
  Merge the tiles and store result in seperate database (ImageMagick/montage tool).

The database contains following elements
  - the tile (png file)
  - last modified date (given from http server)
  - etag (given from http server)

# Merge Tiles
Input Data:
 - database with tiles and meta data (date and etag)
  
Output Data:
 - database with merged tile
 
Process description:
- Load Tile and check if update flag is set
- if Update required: merge tiles and store it in database

The database contains following elements
  - the tile (png file)
  - last modified date (given from http server)
  - etag (given from http server)
  

# Stich Tiles
Input Data:
 - atlas xml specification
 - database with tiles and meta data (date and etag)
  
Output Data:
 - one picture for each chart
 
Process description:
 - export the tiles from database to filesystem
 - use "ImageMagick/composite" tool to stich the images
 
# Generate KAP File
Input Data:
 - atlas xml specification
 - one picture for each chart

Output Data:
 - kap file
 - geo json file
 
 
 



