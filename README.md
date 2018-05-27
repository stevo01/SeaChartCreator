# SeaChartCreator

SeaChartCreator is based on python script. The script was developed and tested on system with
- Windows 10 / 64 bit 
- python 3.5

The need following externel librarys / applications:
- ImageMagick 7.0.7-35
- imgkap Ver. 1.1

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
cd c:\tools\SeeChartCreator
C:\tools\SeaChartCreator>c:\tools\Python35\python.exe seamapcreator.py -i "c:\tools\Mobile Atlas Creator 2.0.0\mobac-profile-newatlas.xml"
```

## bookmarks:
[1] http://mobac.sourceforge.net/

