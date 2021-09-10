'''
Python verion : Version 3

PROJECT GOAL
Automate the extraction of airspace locations where drones cannot fly from FAA shapefile 
Using GIS to design a system to check airspace taking inputs from clients.
The final product needs to be readable to many people at multiple levels within your organization.

'''


#Importing the libaries needed to achive the goals of the project
import datetime # This module will be used when working with time and date
import urllib.request   # This module will be used when waccessing the webpage url
import zipfile  # This module will be used to retrieve the and extract extract zip file


test_date = datetime.date(2021,3,25) # The Realease date for march 2021,was passsed into the datatime function
current_date = datetime.date.today() # This function is used to get the current date

NASR_Sdate = 28 # The date cycle when date is realeased

'''
A while loop is written to iterate through all possible release date, if the released date whihc is the test date
is less than the current date, the loop wil print out the last the last release data before the current data
'''
while test_date < current_date:
    date_time = test_date + datetime.timedelta(days = NASR_Sdate)
    NASR_Sdate +=  28 #an increment of 28 is passed into the while loop
    if date_time > current_date:
        '''
        An if statemnt is passed if the datetime fromthe while loop is greeter than the current data days
        the the release date willbe changed to the last 28 days interval
        '''
        ReleaseDate = date_time - datetime.timedelta(days =28)
        break
        
# The output date format from the while is converted to string format to be able to use it within a string
String_ReleaseDate = str(ReleaseDate)
print ("The latest released date is: " + String_ReleaseDate )

# Delaring the webpage link as a variable
URL = 'https://nfdc.faa.gov/webContent/28DaySub/' + String_ReleaseDate + '/class_airspace_shape_files.zip'

Webpage = urllib.request.urlopen(URL) # Declare the url as a variable 

FileLocation = r'C:\Users\New.zip' # Declare the storage folder as a variable 

# Write the zip file the storage location
with open(FileLocation, 'wb') as file:
    file.write(Webpage.read())
file.closed()

# Save and extract zip file
ZipfileLocation = (r"C:\Users\New.zip")
SaveZiped = zipfile.ZipFile(ZipfileLocation, 'r') 
SaveZiped.extractall(r"C:\Users") 
SaveZiped.closed()


import arcpy  # importing the arcpy python library for the spatial analysis
from arcpy import env  # Importing the enviroment methodfrom the arcpy module

env.overwriteOutput = 1  # It allows files in this processs to be overwrittten
env.workspace = r"C:\Users" #

# Decalring the input shapefiles and output as a variable
Class_Airspace = r"Shape_Files\Class_Airspace.shp"
Locations = r'Locations\Locations.shp'
out_feature_class = "Airspace_Check.shp"

# Run the Spatial Join tool, using the defaults for the join operation and join type
arcpy.SpatialJoin_analysis(Locations, Class_Airspace , out_feature_class)

arcpy.MakeFeatureLayer_management(out_feature_class, "lyr") # Making the output feature class as a layer

# Using an sql query make selection and to calculate area that fail and pass
sql = "LOWER_VAL > '0'" 
arcpy.SelectLayerByAttribute_management("lyr", "NEW_SELECTION",sql) # Inputing the query into a selection
arcpy.management.CalculateField(Locations, "AirCheck", "\"Pass\"") # then filled with pass
arcpy.SelectLayerByAttribute_management("lyr", "SWITCH_SELECTION") # switches the selection                            
arcpy.management.CalculateField("lyr", "AirCheck", "\"Fail\"") # then fill with :fail

# For locations that fail   
sql_fail = "LOWER_VAL = '0'"
layer = arcpy.SelectLayerByAttribute_management("lyr", "NEW_SELECTION",sql_fail) #making new selection with the query
arcpy.TableToTable_conversion(layer,r"C:\Users", "Result.csv") # Coverting the seleted layer attribute to a csv file


import pandas as pd #import the pandas module as pd
data = pd.read_csv(r"C:\Users\Result.csv") #Declairng the ouput csv filefrom the anlysis as variable
# uisng pandas DataFrame to extract airspace class, airspace name, and airport identifier for location that fail
new_data = data[["IDENT","NAME","CLASS","AirCheck"]]
new_data.to_csv(r"C:\Users\Result_%String_ReleaseDate%.csv",index = False) #Export the new cleaned csv out

print "All done"

