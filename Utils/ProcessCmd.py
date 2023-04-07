#!/usr/bin/python3
# encoding: utf-8


import subprocess
from kap.gen import KapGen
from Utils.glog import getlog
from Utils.Helper import ensure_dir

CONVERT_APP = "convert"
COMPOSITE_APP = "composite"
MONTAGE_APP = "/usr/bin/montage"
IMGKAP_APP = "/usr/local/bin/imgkap"
SEVEN_Z_APP = "7z"


def _ProcessCmd(cmd, CWD="./"):
    logger = getlog()
    logger.debug("execute command: {}".format(cmd))
    return_code = subprocess.call(cmd, cwd=CWD, shell=True)
    return return_code


def MergePictures(SeaMapFilename, OSMFilename, ResultFilename):
    cmd = "{} {} {} {}".format(COMPOSITE_APP, SeaMapFilename, OSMFilename, ResultFilename)
    ret = _ProcessCmd(cmd)
    if ret is not 0:
        logger = getlog()
        logger.error("error occure: {}".format(cmd))
    return ret


def StitchPicture(xcnt, ycnt, filenamelist, filename):
    options = ' '
    # options += '-limit memory 0 '
    options += '+frame '
    options += '+shadow '
    options += '+label '
    options += '-background none '  # This option keeps the background transparent

    cmd = "{} {} -tile {}x{} -geometry 256x256+0+0 {} {}".format(MONTAGE_APP, options, xcnt, ycnt, filenamelist, filename)
    ret = _ProcessCmd(cmd)
    if ret is not 0:
        logger = getlog()
        logger.error("error occure: {}".format(cmd))
    return ret


def ConvertPicture(infile, outfile, options="+dither -colors 127 "):
    cmd = "{} {} {} {}".format(CONVERT_APP, infile, options, outfile)
    ret = _ProcessCmd(cmd)
    if ret is not 0:
        logger = getlog()
        logger.error("ConvertPicture error occure: {}".format(cmd))
    return ret


'''
def GenerateKapFile(filenamein, filenameout, ti):
    ensure_dir(filenameout)
    cmd = "{} {} {} {} {} {} {} -t {}".format(IMGKAP_APP, filenamein, ti.NW_lat, ti.NW_lon, ti.SE_lat, ti.SE_lon, filenameout, ti.name)
    ret = _ProcessCmd(cmd)
    if ret is not 0:
        #assert(ret == 0)
        logger = getlog()
        logger.error("Kap File Generation failed: {}".format(cmd))
'''

'''
c:\data\OSM\50_SeaChartCreator\ExternalUtils\imgkap>imgkap.exe
ERROR - Usage:\imgkap [option] [inputfile] [lat0 lon0 lat1 lon1 | headerfile] [outputfile]

imgkap Version 1.11 by M'dJ

Convert kap to img :
        imgkap mykap.kap myimg.png : convert mykap into myimg.png
        imgkap mykap.kap mheader.kap myimg.png : convert mykap into header myheader (only text header kap file) and myimg.png

Convert img to kap :
        imgkap myimg.png myheaderkap.kap : convert myimg.png into myimg.kap using myheader.kap for kap informations
        imgkap myimg.png myheaderkap.kap myresult.kap : convert myimg.png into myresult.kap using myheader.kap for kap informations
        imgkap mykap.png lat0 lon0 lat1 lon2 myresult.kap : convert myimg.png into myresult.kap using WGS84 positioning
        imgkap -s 'LOWEST LOW WATER' myimg.png lat0 lon0 lat1 lon2 -f : convert myimg.png into myimg.kap using WGS84 positioning and options
'''


def GenerateKapFile(filenamein, filenameout, ti):
    ensure_dir(filenameout)

    # generate header
    gen = KapGen()
    header = gen.GenHeader(ti)

    kapheaderfilename = filenamein + ".header.kap"

    with open(kapheaderfilename, "w") as f:
        f.write(header)

    cmd = "{} {} {} {} -t {} -c".format(IMGKAP_APP, filenamein, kapheaderfilename, filenameout, ti.name)
    ret = _ProcessCmd(cmd)
    if ret is not 0:
        logger = getlog()
        logger.error("error occure: {}".format(cmd))
        assert(False)
    # ExternalUtils/imgkap/imgkap ./work/StichDir/OpenSeaMapMerged/ArabianSea/L16-27816-42904-16-8/16/L16-27816-42904-16-8_16.png ./work/StichDir/OpenSeaMapMerged/ArabianSea/L16-27816-42904-16-8/16/L16-27816-42904-16-8_16.png.header.kap ./work/kap/OSM-OpenCPN2-KAP-ArabianSea-20190427-1106//L16-27816-42904-16-8_16.kap -t L16-27816-42904-16-8


def ZipFiles(dirname, archivfilename):
    '''
    7z a $target $dir
    '''
    options = 'a'
    cmd = "{} {} {} {}".format(SEVEN_Z_APP, options, archivfilename, dirname)
    ret = _ProcessCmd(cmd)
    if ret is not 0:
        logger = getlog()
        logger.error("error occure: {}".format(cmd))
    return ret
