import sys
import fnmatch
import os
import arcpy
from arcpy.sa import *
arcpy.CheckOutExtension("spatial")
nosFile = sys.argv[1]
rasterFolder = sys.argv[2]

arcpy.env.overwriteOutput = True

#list of images to open\
field = 'RsatID'
images = [row[0] for row in arcpy.da.SearchCursor(nosFile,field)]
uniqueImages =list(set(images))

for image in uniqueImages:
    rastertoclip = os.path.join(rasterFolder,'{}_12.5m_nrlcc_8bit_med.tif'.format(image))
    print rastertoclip
    print '"RsatID" = {}'.format(image)

    #select polygon to use as clip
    query = str('"RsatID"')+ " = " + "'{}'".format(image)
    arcpy.MakeFeatureLayer_management(nosFile,'polygon_lyr')
    arcpy.SelectLayerByAttribute_management('polygon_lyr','NEW_SELECTION', query)

    outfile = os.path.join('K:/Projects/GEM1/GEM1toGEM2/test',str(image))+ '.tif'
    print outfile
    arcpy.Clip_management(rastertoclip,"#",outfile,'polygon_lyr',"#","ClippingGeometry")
    print 'saved' + outfile

arcpy.CheckInExtension("spatial")
