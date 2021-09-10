import arcpy
from arcpy.sa import *

arcpy.env.overwriteOutput = True
arcpy.env.workspace = 'C:\Users\HP\Desktop\Task_Zone\Solution'
#set the map documentas a variable
mxd = arcpy.mapping.MapDocument('Map_Doc.mxd')

#set the map dataframe as variable
dataframe = arcpy.mapping.ListDataFrames(mxd)[0]
mxd.activeView = "PAGE_LAYOUT"
dataframe.elementPositionX,dataframe.elementPositionY = 0.5,0.5
dataframe.elementHeight, dataframe.elementWidth = 10,7.5


# set the data as variable
dsm = "TechPark_dsm.tif"
dtm = "TechPark_dtm.tif"
ortho = "TechPark_orthomosaic.tif"
zone_file = "Boundaries.shp"

#using minus to subtract two raster
minus = Minus(dsm,dtm)
minus.save("features.tif")

##Extract buildings
#Reclass Raster
outReclass = Reclassify("features.tif", "Value",RemapValue([[-5.255,5,1],[5,28,2]]))
outReclass.save("Reclass_features.tif")


#Raster to Polygon
inRaster = "Reclass_features.tif"
outPolygons = "features_poly.shp"
field = "Value"

arcpy.RasterToPolygon_conversion(inRaster, outPolygons, "SIMPLIFY", field)

# adding the Area Attributes
arcpy.AddGeometryAttributes_management(outPolygons, "AREA")



#Select Buildingsbase on gridcode and area
in_features = "features_poly.shp"
out_feature_class = "features_hgh.shp"
where_clause = 'gridcode = 2 AND POLY_Area >1000'

arcpy.Select_analysis(in_features, out_feature_class, where_clause)

arcpy.FeatureToPoint_management("features_hgh.shp", "features_pnt.shp","CENTROID")

ExtractValuesToPoints("features_pnt.shp", dsm,"building_height.shp","INTERPOLATE","ALL")

# Adding Data to the map docment
building = arcpy.mapping.Layer("building_height.shp")
arcpy.mapping.AddLayer(dataframe,building,"TOP")

#add the authmosaic to the map
orthophoto = arcpy.mapping.Layer("TechPark_orthomosaic.lyr")
arcpy.mapping.AddLayer(dataframe,orthophoto,"BOTTOM")

#add the zone file to the map
zone = arcpy.mapping.Layer(zone_file)
arcpy.mapping.AddLayer(dataframe,zone,"AUTO_ARRANGE")

# 7. configure legend
legend = arcpy.mapping.ListLayoutElements(mxd,"LEGEND_ELEMENT")[0]
legend.autoAdd = False
styles = arcpy.mapping.ListStyleItems("ESRI.style","Legend Items")[2]
#for style in styles:
 #   print style.itemName

## Get the legend as an object
layers = arcpy.mapping.ListLayers(mxd)

## Change the style of the building point features
builds = layers[0]
legend.updateItem(builds,styles)

# Slect Zone
selected_zone = arcpy.SelectLayerByAttribute_management(zone,"NEW_SELECTION","Zone = 1")

# Select sll the buildings in that zone
arcpy.SelectByLocation_management(selected_zone,"INTERSECT",buildng)
# zoom to the selected Zone
dataframe.zoomToSelectedFeatures()

# set title to the Building Zone
#titleElement.text = "Zone 1"


mxd.save()
#Fill in the data in the table forthose attribute by updating textboxes

#set all textboxelements
"""
Detemine howmany buildings are in themap andhow many textboses you needtofill
use search cursorto loop through the bildings and get th attribute values
select the text of theext boxes basedon the cursorvalues

Unselect everything
arcpy.SelectLayerByAttribute_management(zone_file,"CLEAR_SELECTION")



ExporttoPDF


#Repeating the steps for second zone
## Slect Zone

#setitletothe BuildingZone



#Fill in the data in the table forthose attribute by updating textboxes

#set all textboxelements
Detemine howmany buildings are in themap andhow many textboses you needtofill
use search cursorto loop through the bildings and get th attribute values
select the text of theext boxes basedon the cursorvalues

Unselect everything
ExporttoPDF

# Configure North Arrow
northArrows = arcpy.mapping.ListLayoutElements(mxd,'MAPSURROUND_ELEMENT', "North*")
for objects in northArrows:
    print objects
"""
