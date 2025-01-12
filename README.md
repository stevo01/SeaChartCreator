# SeaChartCreator

SeaChartCreator is based on python script. The script was developed and tested on system with following linux OS
- Linux debian 11 / 64 bit 

The need following external librarys / applications:
- python 3.9
- python3-venv
- ImageMagick 6.9.11
- FreeImage - https://sourceforge.net/projects/freeimage/files/Source Distribution/3.18.0/FreeImage3180.zip
- imgkap (master branch from from https://github.com/stevo01/imgkap  master branch (do not use releases)
- pyyaml
- pillow
- geojson

SeaChartCreator is using tiles from the OpenSeaMap Project and/or the Open Streetmap Project.

Open Sea Map
     https://openseamap.org/

Open Street Map:
     https://openstreetmap.org
     https://operations.osmfoundation.org/policies/tiles/

Please read and meet tile usage policy: 
     https://operations.osmfoundation.org/policies/tiles/

All loaded tiles and generated maps stay under following license:
"Creative Commons Attribution-Share Alike 2.0", CC-BY-SA-Lizenz

## Instruction for the creation of KAP Files

### Use Mobac [1] Software to select one or multiple areas for chart generation.
* start the software
* select a tile server e.g. OpenStreetMap 4UMaps.eu
* select GridZoom 16 in upper area of the shown map
* Create New Atlas Content PNG + Worldwide (PNG & PWG)
* Set Menue -> Selection -> Selection Mode -> Rectangle
* Select "15" in zoom level dialog, select multiple zoom levels where needed.
* Use the Mouse to select a area for single chart
* press "add selection" in the "atlas content" dialog
* save the profile e.g. newatlas 
   
note: the atlas will be stored in a xml file located in the mobac software directory (e.g. "C:\tools\Mobile Atlas Creator 2.0.0\mobac-profile-newatlas.xml"). 
    
### clone project and call python scripts to create kap file of specific mobac project file

```console
cd ~/
git clone https://github.com/stevo01/SeaChartCreator
cd SeaChartCreator
git clone git@github.com:OpenSeaMap/chart-projectfiles.git


MAP_DESCR_FILE=./sample/atlas/osmcb/sea/osmcb-catalog-test.xml
MAPSOURCE="./sample/mapsource/mp-OpenSeaMap-Bravo.yaml"
DB_DIR="./cache/"

# fetch tiles
python3 fetch.py -m $MAPSOURCE -d $DB_DIR -q -s -f -i $MAP_DESCR_FILE

# merge tiles
python3 merge.py -d $DB_DIR -q -s -i $MAP_DESCR_FILE 

# build kap file
python3 build.py -t kap -d $DB_DIR -s -i $MAP_DESCR_FILE

# build mbtile file
python3 build.py -t mbtiles -d $DB_DIR -s -i $MAP_DESCR_FILE

```

notes: 
* the generated kap file is located in directory ./work/kap/
* the generated mbtiles file is located in directory ./work/mbtiles/


## bookmarks:
[1] http://mobac.sourceforge.net/
