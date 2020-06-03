# SeaChartCreator

SeaChartCreator is based on python script. The script was developed and tested on system with
- Linux debian 9 / 64 bit 
- python 3.5

The need following external librarys / applications:
- ImageMagick 7.0.8-1
- imgkap (master branch from from https://github.com/stevo01/imgkap/commits/master ,do not use releases)
- FreeImage - https://kent.dl.sourceforge.net/project/freeimage/Source%20Distribution/3.18.0/FreeImage3180.zip
- pyyaml
- PIL

SeaChartCreator use tiles from the OpenSeaMap Project and the Open Streetmap Project.

Open Sea Map
     http://openseamap.org/

Open Street Map:
     http://openstreetmap.org
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

	cd ~/
	git clone https://github.com/stevo01/SeaChartCreator
	cd SeaChartCreator
	python3 fetch.py -i ./sample/atlas/mobac/mobac-profile-testprj.xml 
	python3 build.py -i ./sample/atlas/mobac/mobac-profile-testprj.xml 

the generated kap file is located in directory ./work/kap/

* In case of file cannot be found errors during building, check the path to the helper scripts in Util/ProcessCommand.py

## bookmarks:
[1] http://mobac.sourceforge.net/
