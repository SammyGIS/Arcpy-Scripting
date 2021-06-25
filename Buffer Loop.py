#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      HP
#
# Created:     13/12/2020
# Copyright:   (c) HP 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import arcpy

arcpy.env.overwriteOutput = True

shapefile = r"C:\Users\HP\Desktop\PM_CompostBuffer\Compost.shp"

arcpy.CheckOutExtension('spatial')

with arcpy.da.SearchCursor(shapefile, 'Beneficiar') as searcher:
    beneficiary = []
    for row in searcher:
        bene = row[0]
    if bene not in beneficiary:
        beneficiary.append(bene)

print 'beneficiary='+'beneficiary'
for bene  in beneficiary:
    print
    print'bene='+bene
    query = 'bene = '{}''.format(bene)
    output = "C:/Users/HP/Desktop/PM_CompostBuffer/{}_.shp".format(bene)
    arcpy.Select_analysis(shapefile,output,query)


    Buffer = arcpy.Buffer_analysis(shapefile,output,"20 Meters", "FULL", "ROUND", "NONE", "", "PLANAR")
