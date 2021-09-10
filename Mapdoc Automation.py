import arcpy
from arcpy.sa import *
import os


arcpy.env.overwriteOutput = True
arcpy.env.workspace = 'C:/Users/HP/Desktop/Task_Zone/Solution'

#set the map documentas a variable
mxd = arcpy.mapping.MapDocument("Map_doc.mxd")

#set the map dataframe as variable
dataframe = arcpy.mapping.ListDataFrames(mxd)[0]

# set the data as variable
dsm = "TechPark_dsm.tif"
dtm = "TechPark_dtm.tif"
ortho = "TechPark_orthomosaic.tif"
zone_file = "Boundaries.lyr"

#using minus to subtract two raster
minus = Minus(dsm,dtm)
minus.save("features.tif")


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

ExtractValuesToPoints("features_pnt.shp", dsm,"Building.shp","INTERPOLATE","ALL")

# Adding Data to the map docment
building = arcpy.mapping.Layer("Building.shp")
arcpy.mapping.AddLayer(dataframe,building,"TOP")

#add the authmosaic to the map
orthophoto = arcpy.mapping.Layer("TechPark_orthomosaic.lyr")
arcpy.mapping.AddLayer(dataframe,orthophoto,"BOTTOM")

#add the zone file to the map
zone = arcpy.mapping.Layer(zone_file)
arcpy.mapping.AddLayer(dataframe,zone,"AUTO_ARRANGE")

# 7. configure legend
legend = arcpy.mapping.ListLayoutElements(mxd,"LEGEND_ELEMENT")[0]
legend.autoAdd = True
legend.elementPositionX,legend.elementPositionY = 0.7, 2.3
    
## Get the legend as an object
Style = arcpy.mapping.ListStyleItems("ESRI.style","Legend Items")[2]

## Change the style of the building point features
layer = arcpy.mapping.ListLayers(mxd)

#legend.updateItem(Style,layer[0])
legend.removeItem(layer[1])
legend.removeItem(layer[2])


# Select Zone
arcpy.SelectLayerByAttribute_management(layer[1],"NEW_SELECTION","Zone = 0")

# zoom to the selected Zone
dataframe.zoomToSelectedFeatures()

# set title to the Building Zone
text_0 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT","Title")[0]
text_0.text = "Map Showing Building in Zone 0"

#set all textbox elements
text_1 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT","area1")[0]
text_2 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT","height1")[0]
text_3 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT","Num1")[0]
alist = []
#use search cursorto loop through the bildings and get th attribute values
with arcpy.da.SearchCursor(building,("FID","POLY_AREA","RASTERVALU")) as cursor:
    for row in cursor:
        # extracting the area and heignht of the building bases on the FID number
        if row[0] == 5: 
            area = int(row[1])
            hgh = int(row[2])
            #print area,hgh
        
            """
            select the text of the text boxes base on the cursor values
            """
            value1 = area
            value2 = hgh
            text_1.text = value1
            text_2.text = value2
            text_3.text = "5"

#Unselect everything
arcpy.SelectLayerByAttribute_management(layer[1],"CLEAR_SELECTION")


mxd.saveACopy("Zone0.mxd")

#ExporttoPDF
arcpy.mapping.ExportToPDF(mxd,"PDF/Zone_0.pdf")



# Select Zone
arcpy.SelectLayerByAttribute_management(layer[1],"NEW_SELECTION","Zone = 1")

# zoom to the selected Zone
dataframe.zoomToSelectedFeatures()

# set title to the Building Zone
text_0 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT","Title")[0]
text_0.text = "Map Showing Building in Zone 1"

#set all textboxelements
text_1 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT","area1")[0]
text_2 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT","height1")[0]
text_3 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT","Num1")[0]
text_4 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT","area2")[0]
text_5 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT","height2")[0]
text_6 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT","Num2")[0]
text_7 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT","area3")[0]
text_8 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT","height3")[0]
text_9 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT","Num3")[0]
text_10 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT","area4")[0]
text_11 = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT","height4")[0]
text_12= arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT","Num4")[0]


#use search cursorto loop through the bildings and get the attribute values
with arcpy.da.SearchCursor(building,("FID","POLY_AREA","RASTERVALU")) as cursor:
                        for row in cursor:
                            if row[0] == 0: 
                                area = int(row[1])
                                hgh = int(row[2])
                                
                                """
                                select the text of the text boxes base on the cursor values
                                """
                                value1 = area
                                value2 = hgh
                                text_1.text = value1
                                text_2.text = value2
                                text_3.text = "0"

                            if row[0] == 1: 
                                area = int(row[1])
                                hgh = int(row[2])
                                
                                """
                                select the text of the text boxes base on the cursor values
                                """
                                value1 = area
                                value2 = hgh
                                text_4.text = value1
                                text_5.text = value2
                                text_6.text = "1"

                            if row[0] == 2: 
                                area = int(row[1])
                                hgh = int(row[2])
                                """
                                select the text of the text boxes base on the cursor values
                                """
                                value1 = area
                                value2 = hgh
                                text_7.text = value1
                                text_8.text = value2
                                text_9.text = "2"

                            if row[0] == 3: 
                                area = int(row[1])
                                hgh = int(row[2])
                                
                                """
                                select the text of the text boxes base on the cursor values
                                """
                                value1 = area
                                value2 = hgh
                                text_10.text = value1
                                text_11.text = value2
                                text_12.text = "3"


#Unselect everything
arcpy.SelectLayerByAttribute_management(layer[1],"CLEAR_SELECTION")

mxd.saveACopy("Zone1.mxd") #Save a copy as mxd doc

#ExporttoPDF
arcpy.mapping.ExportToPDF(mxd,"PDF/Zone_1.pdf")



#Merge PDF
"""
Using the pdfmerger class
pdf_folder = r"C:/User/HP\Desktop/Task_Zone/Solution/PDF"

pdf_file = os.listdir(pdf_folder)

for pdf in pdf_file:
    pdf_path = ps.path.join(pdf_folder,pdf)

merger = PdfFileMerger()
for PDF in pdf_path:
    merger.append(PDF)

merger.write("CourseAnalysis.pdf")
merger.close
"""
#using arcpy to create and merge pdfs
pdfpath = "PDF/CourseAnalysis.pdf"
pdfDoc = arcpy.mapping.PDFDocumentCreate(pdfpath)
pdfDoc.appendPages("PDF/CoverPage.pdf")
pdfDoc.appendPages("PDF/Zone_0.pdf")
pdfDoc.appendPages("PDF/Zone_1.pdf")
pdfDoc.appendPages("PDF/MXDTemplate.pdf")
pdfDoc.saveAndClose()
