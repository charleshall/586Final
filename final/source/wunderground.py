#-------------------------------------------------------------------------------
# Name:        wubderground
# Purpose:     retrieve almanac data from weather underground for a given city
#
# Author:      charlemh
#
# Created:     30/11/2014
# Copyright:   (c) charlemh 2014
# Licence:
#-------------------------------------------------------------------------------

# Import all of the libraries
import httplib
import json
import arcpy
from arcpy import env
env.workspace = "g:/586/final"
conn = httplib.HTTPConnection("api.wunderground.com")
inFC = arcpy.GetParameterAsText(0)
inCountry = arcpy.GetParameterAsText(1)


#Limit our results for testing purposes
#fc and selectCountry should be parameters
#fc = "G:/586/final/urbanareas1_1/urbanareas1_1.shp"
fc = inFC

fields = arcpy.ListFields(fc, "lowTemp")
if len(fields) > 0:
    print "lowTemp exists"
else:
    arcpy.AddField_management(fc, "lowTemp", "TEXT", "", "", 50)
    print "No low temp Field"
    arcpy.AddMessage("Low Temp Field Added")

fields = arcpy.ListFields(fc, "highTemp")
if len(fields) > 0:
    print "highTemp exists"
else:
    arcpy.AddField_management(fc, "highTemp", "TEXT", "", "", 50)
    print "No Field"
    arcpy.AddMessage("High Temp Field Added")

fieldname = "Country"
delimfield = arcpy.AddFieldDelimiters(fc,fieldname)
#selectCountry = "Bulgaria"
selectCountry = inCountry
selectCountry =selectCountry.replace("USA", "United States of America")

encselectCountry = selectCountry.replace(" ", "%20")

cursor  = arcpy.da.UpdateCursor(fc, ["CITY", "City_Alter", "Country", "lowTemp", "highTemp"], delimfield +" = '" + selectCountry + "'")

for row in cursor:
    #print city name for debug purposes
    #print 'Current city : ' + row[0]


    if row[1] == " ":
        city = row[0]
    else:
        city = row[1]
    #Replace all spaces with underscores, remove commas
    city = city.replace(" ", "_")
    city = city.replace(",", "")
    #Break multiple cities on one line separated by - into individual cities
    cities = city.split('-')
    for workCity in cities:
        # Print working city name for debug purposes
        #print 'Working city:', workCity
        arcpy.AddMessage("Working city name: " + workCity)
        conn.request("GET", "/api/613393ec1cc60128/almanac/q/" + encselectCountry + "/" + workCity + ".json")
        r1 = conn.getresponse()
        if r1.status == 200:
            data1 = r1.read()
            #print data1
            parsed_json = json.loads(data1)
            if 'temp_low' not in data1:
                #raise ValueError("No almanac data received")
                row[3] = "Unavailable"
                row[4] = "Unavailable"
                cursor.updateRow(row)
            else:
                tempLow = parsed_json['almanac']['temp_low']['normal']['F']
                tempHigh = parsed_json['almanac']['temp_high']['normal']['F']
                #print tempLow + " " + tempHigh
                #print r1.status, r1.reason
                print "The city of %s has a normal low of %s degrees F and a normal high of %s degrees F" % (workCity, tempLow, tempHigh)
                arcpy.AddMessage("Temp data added for: " + workCity)
                row[3] = tempLow
                row[4] = tempHigh
                cursor.updateRow(row)
        else:
            print "Error retireving wg data"
    del workCity
del row
del cursor
arcpy.AddMessage("Tool completed")
print arcpy.GetMessages
