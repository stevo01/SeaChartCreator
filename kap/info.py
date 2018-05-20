#!/usr/bin/python3
# encoding: utf-8
'''
KAPAnalyser/Info.py allows a analysis of a KAP file and export of the detected maps to
 - mobac project file
 - chart designer project file

Copyright (C) 2017  Steffen Volkmann

This file is part of SeaMapCreator.

Foobar is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Foobar is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Foobar.  If not, see <http://www.gnu.org/licenses/>.
'''

from Utils.filesystem import GetFileList, _GetFileList
from xml.dom.minidom import Document
from optparse import OptionParser
from kap.analyse import kapfile
from Utils.Helper import ensure_dir

# bookmarks:
# sample files for kap
#   https://sourceforge.net/projects/opennautical/files/Maps/Region/Europe/Inland%20Waterways/
#   http://www.charts.noaa.gov/InteractiveCatalog/nrnc.shtml
#
# list of zoom levels in "tile world"
#   https://wiki.openstreetmap.org/wiki/Zoom_levels
#
# Description of KAK File HEADER
#   https://opencpn.org/wiki/dokuwiki/doku.php?id=opencpn:supplementary_software:chart_conversion_manual:imgkap_and_kap_file


def WriteMobacProject(name, filename, maps, map_source="OpenSeaMapTEST"):

    # <?xml version="1.0" ?>
    #  <atlas name="OSM-UHW" outputFormat="PNGWorldfile" version="1">
    #    <Layer name="UHW_2_16">
    #      <Map mapSource="OpenSeaMapTEST" maxTileCoordinate="8999168/5517824" minTileCoordinate="8988416/5506048" name="UHW_2_16 16" zoom="16"/>
    #    </Layer>
    #  </atlas>

    doc = Document()

    root = doc.createElement("atlas")
    root.setAttribute("version", '1')
    root.setAttribute("name", name)
    root.setAttribute("outputFormat", "PNGWorldfile")

    doc.appendChild(root)

    for map in maps:

        # Create Element
        tempChild = doc.createElement("Layer")
        tempChild.setAttribute("name", map.name)
        root.appendChild(tempChild)

        tempMap = doc.createElement("Map")
        tempMap.setAttribute("maxTileCoordinate", "{}/{}".format(map.xtile_se * 256, map.ytile_se * 256))
        tempMap.setAttribute("minTileCoordinate", "{}/{}".format(map.xtile_nw * 256, map.ytile_nw * 256))
        tempMap.setAttribute("mapSource", map_source)
        tempMap.setAttribute("zoom", "{}".format(map.zoom))
        tempMap.setAttribute("name", "{} {}".format(map.name, map.zoom))

        tempChild.appendChild(tempMap)

    doc.writexml(open(filename, 'w'),
                 indent="  ",
                 addindent="  ",
                 newl='\n')

    doc.unlink()


def WriteChartDesignerProject(name, filename, maps, map_source="AH OpenStreetMap Mapnik"):

    # sample
    # <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    # <catalog name="Potsdamer_Havel" size="7" version="2">
    #    <Layer name="L16" zoomLvl="16">
    #        <Map name="L16-21544-35120-16-16" mapSource="AH OpenStreetMap Mapnik" ulc="52.34876318, 12.91992188" lrc="52.29504228, 13.00781250" minTileCoordinate="21544/35120" maxTileCoordinate="21559/35135" number="16-21544-35120-16-16"/>
    #    </Layer>
    # </catalog>

    doc = Document()

    root = doc.createElement("catalog")
    root.setAttribute("version", '2')
    root.setAttribute("name", name)
    root.setAttribute("size", "{}".format(len(maps)))

    doc.appendChild(root)

    for map in maps:

        # Create Element
        tempChild = doc.createElement("Layer")
        tempChild.setAttribute("name", map.name)
        tempChild.setAttribute("zoomLvl", "{}".format(map.zoom))

        root.appendChild(tempChild)

        tempMap = doc.createElement("Map")
        tempMap.setAttribute("name", "{} {}".format(map.name, map.zoom))
        tempMap.setAttribute("mapSource", map_source)
        tempMap.setAttribute("ulc", "{}, {}".format(map.NW_lat, map.NW_lon))
        tempMap.setAttribute("lrc", "{}, {}".format(map.SE_lat, map.SE_lon))
        tempMap.setAttribute("minTileCoordinate", "{}/{}".format(map.ytile_nw, map.xtile_nw))
        tempMap.setAttribute("maxTileCoordinate", "{}/{}".format(map.ytile_se, map.xtile_se))
        tempMap.setAttribute("number", "{}{}{}".format(map.zoom, map.ytile_nw, map.xtile_nw))
        tempChild.appendChild(tempMap)

    doc.writexml(open(filename, 'w'),
                 indent="  ",
                 addindent="  ",
                 newl='\n')

    doc.unlink()


if __name__ == '__main__':
    # sample calls of the script
    # python3 info.py -i ./../sample/kap/OSM-UHW/ -n UHW -o ./../sample/atlas/mobac-profile-UHW.xml -c ./../sample/atlas/chartdesigner-profile-UHW.xml
    # python3 info.py -i X:/80_User/stevo/021_Boote/10_Navigation/20_charts/ONC_Maps/UHW-UntereHavelWasserstrasse/ -n UHW -o ./../sample/atlas/mobac-profile-UHW.xml -c ./../sample/atlas/chartdesigner-profile-UHW.xml

    parser = OptionParser()
    usage = "usage: %prog [options] arg1 arg2"
    atlas = list()

    parser.add_option("-i", "--InDir", type="string", help="Input Directory with kap file(s)", dest="InDir", default="./../sample/kap/OSM-UHW/")
    parser.add_option("-n", "--AtlasName", type="string", help="Atlas Name", dest="name", default=".")
    parser.add_option("-o", "--OutFileM", type="string", help="Output: Mobac Project File", dest="MobacPrjFilename", default="./../sample/atlas/mobac-profile-UHW.xml")
    parser.add_option("-c", "--OutFileC", type="string", help="Output: Chart Designer Project File", dest="ChartDesignerPrjFilename", default="./../sample/atlas/chartdesigner-profile-UHW.xml")

    options, arguments = parser.parse_args()

    maps = list()

    # get a list of kap files for a given path
    kapfilelist = _GetFileList(options.InDir, '.kap')
    zoom = 16

    print("KapAnalyser: {} kap files found".format(len(kapfilelist)))

    # create a list with
    for kfile in kapfilelist:
        kap = kapfile(kfile)
        ti = kap.GetTileInfo(zoom)
        print(ti)
        maps.append(ti)

    # write mobac project file
    if options.MobacPrjFilename:
        print("WriteMobacProject {}".format(options.MobacPrjFilename))
        ensure_dir(options.MobacPrjFilename)
        WriteMobacProject(options.name, options.MobacPrjFilename, maps)

    # write chart designer project file
    if options.ChartDesignerPrjFilename:
        print("ChartDesignerPrject {}".format(options.ChartDesignerPrjFilename))
        ensure_dir(options.ChartDesignerPrjFilename)
        WriteChartDesignerProject(options.name, options.ChartDesignerPrjFilename, maps)

    print("ready")
