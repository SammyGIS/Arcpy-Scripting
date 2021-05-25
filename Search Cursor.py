import arcpy
# add worksapce
arcpy.env.workspace = 'C:\Users\HP\Desktop\Arcpy\Data'
# add ur data
data = 'C:\Users\HP\Desktop\Arcpy\Data\Country.shp'
# crrete a SQL expression to sellect the attribute you wants
sql = "CNTRY_NAME IN ('Nigeria','Ghana')"

#using arcpy SearchCursor to selet an attribute
with arcpy.da.SearchCursor(data,'CNTRY_NAME',sql) as cursor:

#using For loop to itterate throught the item n the list
    for items in cursor:
            data = cursor
            print data

