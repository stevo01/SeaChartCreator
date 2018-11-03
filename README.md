# SeaChartCreator

SeaChartCreator is based on python script. The script was developed and tested on system with
- Windows 10 / 64 bit
- Linux Ubuntu 16.04 / 64 bit 
- python 3.5

The need following external librarys / applications:
- ImageMagick 7.0.8-1
- imgkap Ver. 1.1
- FreeImage - https://kent.dl.sourceforge.net/project/freeimage/Source%20Distribution/3.18.0/FreeImage3180.zip
- pyyaml

SeaChartCreator use tiles from the OpenSeaMap Projekt and the Open Streetmap Projekt.

Open Sea Map
     http://openseamap.org/

Open Street Map:
     http://openstreetmap.org
     https://operations.osmfoundation.org/policies/tiles/

Please read and meet tile usage policy: 
     https://operations.osmfoundation.org/policies/tiles/

All loaded tiles and generated maps stay under following license:
"Creative Commons Attribution-Share Alike 2.0", CC-BY-SA-Lizenz

## Instruction for the creation of KAP Files:
1 - Use Mobac [1] Software to select one or multiple areas for chart generation.
* start the software
* select a tile server e.g. OpenStreetMap 4UMaps.eu
* select GridZoom 16 in upper area of the shown map
* Create New Atlas Content PNG + Worldwide (PNG & PWG)
* Set Menue -> Selection -> Selection Mode -> Rectangle
* Select "15" in zoom level dialog
* Use the Mouse to select a area for single chart
* press "add selection" in the "atlas content" dialog
* save the profile e.g. newatlas 
   
note: the atlas will be stored in a xml file located in the mobac software directory (e.g. "C:\tools\Mobile Atlas Creator 2.0.0\mobac-profile-newatlas.xml"). 
    
2 - call the python script and use the -i option to specify the mobac project file
```
cd ~/
clone https://github.com/stevo01/SeaChartCreator
cd SeaChartCreator
python3 fetch.py -i ./sample/atlas/mobac/mobac-profile-testprj.xml 
python3 build.py -i ./sample/atlas/mobac/mobac-profile-testprj.xml 
```
the generated kap file is located in directory ./work/kap/

## bookmarks:
[1] http://mobac.sourceforge.net/

