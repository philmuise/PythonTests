import arcpy,os
arcpy.env.overwriteOutput = True


def rasterCentroid(rasterFile):
    raster = arcpy.Raster(rasterFile)
    x = raster.extent.XMin + (raster.extent.XMax- raster.extent.XMin)/2
    y = raster.extent.YMin + (raster.extent.YMax - raster.extent.YMin)/2
    return x, y


def duplicatePids(nosFile):
    with arcpy.da.SearchCursor(nosFile,'Pid') as cursor:
          pidList = [row[0] for row in cursor]
          duplicatePid = list(set(x for x in pidList if pidList.count(x)>1))
    return duplicatePid

def polygonCentroid(nosFile):
    #add x, y fields to polygon shapefile
    arcpy.AddField_management(nosFile, "X", "DOUBLE")
    arcpy.AddField_management(nosFile, "Y", "DOUBLE")
    arcpy.CalculateField_management(nosFile, "X", "!SHAPE.CENTROID.X!", "PYTHON_9.3")
    arcpy.CalculateField_management(nosFile, "Y", "!SHAPE.CENTROID.Y!", "PYTHON_9.3")
    centroidList = []
    with arcpy.da.SearchCursor(nosFile,('Pid','X','Y')) as cursor:
         for row in cursor:
             centroidList.append((row[0],row[1],row[2]))
    return centroidList

def shortestDistance(polygonCentroid, rasterCentroid1, rasterCentroid2):

    distancebtw1 = ((polygonCentroid[1]-rasterCentroid1[0])**2 + (polygonCentroid[2]-rasterCentroid1[1])**2)**0.5
    distancebtw2 = ((polygonCentroid[1]-rasterCentroid2[0])**2 + (polygonCentroid[2]-rasterCentroid2[1])**2)**0.5
    return distancebtw1, distancebtw2

nosFile =  r'K:\Projects\GEM1\GEM1toGEM2\Products\NOS_2016_RSimageinfo.shp'

arcpy.env.workspace = r'K:\Projects\GEM1\GEM1toGEM2\Products'
#get list with duplicate polygons
duplicates = duplicatePids(nosFile)
print duplicates
#set x,y information for nosfile
##polygonCentroid(nosFile)

#Make a layer of all duplicates
arcpy.CopyFeatures_management('NOS_2016_RSimageinfo.shp','duplicateNOS3')
arcpy.MakeFeatureLayer_management('duplicateNOS3.shp','DUP')
for values in duplicates:
    query = "\"Pid\"=" + str(values)
    arcpy.SelectLayerByAttribute_management('DUP','ADD_TO_SELECTION',query)

arcpy.AddField_management('DUP', "XRASTER", "DOUBLE")
arcpy.AddField_management('DUP', "YRASTER", "DOUBLE")
rasterinfo = []
with arcpy.da.UpdateCursor('DUP',['Pid','RefImgName','XRASTER','YRASTER']) as cursor:
     for row in cursor:
         rasterfile = os.path.join(r'K:\Projects\GEM1\8bit\Median_filtered_8bit','{}.tif'.format(row[1]))
         rastercenter = rasterCentroid(rasterfile)
         row[2] = rastercenter[0]
         row[3] = rastercenter[1]
         cursor.updateRow(row)
arcpy.CopyFeatures_management('DUP','duplicateNOs4')

