import pandas as pd
import os
import arcpy#for functions that have to run in ArcGIS Pro
import csv

print("")     #Intro Message and Explanation
print("   Welcome to the Austin Downtown Lions Club")
print("     Glasses Donation Location Finder Tool")
print("~~~~~~~~~~~~*********************~~~~~~~~~~~")
print("")
print(" This tool takes your Austin, TX address and finds the ")
print(" nearest donation location for you.")
print("")

InputAddress=input("Please Input Austin, TX Street Address:   ")  #Gathering user input
InputZip=input("Please Input Zip Code    ")
secondcsv=r"D:\ScratchFolder\secondcsv.csv" #saving as CSV file

with open(secondcsv,"w",newline="") as file_writer:     #writing user input to second csv file
    fields=["Address","Zip"]
    writer=csv.DictWriter(file_writer,fieldnames=fields)
    writer.writeheader()
    writer.writerow({"Address":InputAddress,"Zip":InputZip})


#SpotList=[InputAddress,InputZip] #Creating List from strings


gdbpath=r"E:\OneDriveMain\OneDrive\_GisProjects\2023Projects\ProjectLeo\Default.gdb"
print("~~|   Geodatabase Path Set to:" + gdbpath)


df = pd.read_html('http://www.austindowntownlions.org/Eyeglasses_Recycling')#Scraping Correct Web Address

print("~~|   Reading Info From Website...")
dfa = df[1]#(skiprows=1,header=0)
#print(dfa)
firstcsv=r"D:\ScratchFolder\firstcsv.csv"
dfa.to_csv(firstcsv)

print("~~|   Saved as CSV File ")
dfb = pd.read_csv(firstcsv,skiprows=1, header=0,index_col='Facility') #removes row, sets header to new first row
#Sets index column to facility, auto deletes numeric first column

print("~~|   Formatting Data... ")
dfb=dfb.drop(dfb.columns[[0]],axis=1) #removes extra column
#print(dfb) #removing first row sucessful to this point
csvfinal=r"D:\ScratchFolder\csvfinal.csv"
dfb.to_csv(csvfinal) #for testing csv at this point, has 2 extra colums

print("~~|   Output to CSV LionsTable")

#Setting up to output to GDB
OutTableName="LionsTable"
arcpy.conversion.TableToTable(csvfinal,gdbpath,OutTableName) #Converting and adding Lions Locations to gdb

print("~~|   Lions Donation Locations Converted to table in ArcGIS")


spottablename="SpotTable"
arcpy.conversion.TableToTable(secondcsv,gdbpath,spottablename)
print("~~|   User Address Converted to table in ArcGIS")


print("~~|   Attempting to Geocode Table Locations...")

arcpy.geocoding.GeocodeAddresses(
    in_table=r"E:\OneDriveMain\OneDrive\_GISProjects\2023Projects\ProjectLeo\Default.gdb\LionsTable",
    address_locator=r"E:\OneDriveMain\OneDrive\_GISProjects\2023Projects\ProjectLeo\AustinLocatorDelta.loc",
    in_address_fields="'Address or Place' Address VISIBLE NONE;Address2 <None> VISIBLE NONE;Address3 <None> VISIBLE NONE;Neighborhood <None> VISIBLE NONE;City City VISIBLE NONE;County <None> VISIBLE NONE;State <None> VISIBLE NONE;ZIP ZIP VISIBLE NONE;ZIP4 <None> VISIBLE NONE;Country <None> VISIBLE NONE",
    out_feature_class=r"E:\OneDriveMain\OneDrive\_GISProjects\2023Projects\ProjectLeo\Default.gdb\GeocodedDonationLocations",
    out_relationship_type="STATIC",
    country=None,
    location_type="ADDRESS_LOCATION",
    category=None,
    output_fields="LOCATION_ONLY"
)
######Geocoding the Table and adding point layer to Default GDB

print("~~|   Geocoding Locations Completed")


print("~~|   Geocoding User Location into Feature Class...")
arcpy.geocoding.GeocodeAddresses(
    in_table=r"E:\OneDriveMain\OneDrive\_GISProjects\2023Projects\ProjectLeo\Default.gdb\SpotTable",
    address_locator=r"E:\OneDriveMain\OneDrive\_GISProjects\2023Projects\ProjectLeo\AustinLocatorDelta.loc",
    in_address_fields="'Address or Place' Address VISIBLE NONE;Address2 <None> VISIBLE NONE;Address3 <None> VISIBLE NONE;Neighborhood <None> VISIBLE NONE;City <None> VISIBLE NONE;County <None> VISIBLE NONE;State <None> VISIBLE NONE;ZIP ZIP VISIBLE NONE;ZIP4 <None> VISIBLE NONE;Country <None> VISIBLE NONE",
    out_feature_class=r"E:\OneDriveMain\OneDrive\_GISProjects\2023Projects\ProjectLeo\Default.gdb\GeocodedUserLocation",
    out_relationship_type="STATIC",
    country=None,
    location_type="ADDRESS_LOCATION",
    category=None,
    output_fields="LOCATION_ONLY"
)#Creadted one entry layer with user input location, for use with Near tool

print("~~|   User Location Geocoded")




print("~~|   Attempting to create a feature layer on the map...")
ResultPath1=r"E:\OneDriveMain\OneDrive\_GISProjects\2023Projects\ProjectLeo\Default.gdb\GeocodedDonationLocations"
##Making Feature Layer from Feature Class, adding to map
layername="Donation Locations"
layerfile1=arcpy.management.MakeFeatureLayer(ResultPath1,layername)[0]
p=arcpy.mp.ArcGISProject(r"E:\OneDriveMain\OneDrive\_GISProjects\2023Projects\ProjectLeo\ProjectLeo.aprx")
m=p.listMaps()[0]
m.addLayer(layerfile1,"TOP")

print("~~|   Donation Locations Layer Added")


print("~~|   Adding User Location Layer...")
ResultPath1=r"E:\OneDriveMain\OneDrive\_GISProjects\2023Projects\ProjectLeo\Default.gdb\GeocodedUserLocation"
layername="User Location"
layerfile1=arcpy.management.MakeFeatureLayer(ResultPath1,layername)[0]
m=p.listMaps()[0]
m.addLayer(layerfile1,"TOP")

print("~~|   User Location Layer Added")

print("~~|   Attempting to save...")
p.save()
print("~~|   Saved Layers in aprx")
print("~~|   Attempting to disconnect all users from GDB [schema lock]...")
arcpy.DisconnectUser(gdbpath,'ALL')
print("~~|   Disconnected"
      "")
print("~~|   Calculating closest location to User Address...")
arcpy.analysis.Near(
    in_features="Donation Locations",
    near_features="User Location",
    search_radius=None,
    location="NO_LOCATION",
    angle="NO_ANGLE",
    method="PLANAR",
    field_names="NEAR_FID NEAR_FID;NEAR_DIST NEAR_DIST",
    distance_unit="Miles"
)


#arcpy.management.Sort(
#    in_dataset="Donation Locations",
#    out_dataset=r"E:\OneDriveMain\OneDrive\_GISProjects\2023Projects\ProjectLeo\Default.gdb\DonationLocationsSorted",
#    sort_field="NEAR_DIST ASCENDING",
#    spatial_sort_method="UR"
#)
##Attempting sort ascending by distance. Should have -1's on top now

###
#lyr="Donation Locations"
#with arcpy.da.UpdateCursor(lyr,"NEAR_DIST") as cursor:
#    for row in cursor:
#        if row[0]==-1:
#            cursor.deleteRow()

print("~~|   Calculation complete")

#newname="NEARDIST"
#newalias="Distance in Miles"
#arcpy.management.AlterField(lyr,"NEAR_DIST",newname,newalias)
###Giving the Distance field an alias


#arcpy.conversion.ExportTable(
#    in_table="Donation Locations",
#    out_table=r"D:\ScratchFolder\endresults.csv",
#    where_clause="",
#    use_field_alias_as_name="USE_ALIAS",
#    field_mapping='Facility "Facility" true true false 8000 Text 0 0,First,#,Donation Locations,Facility,0,8000;Address "Address" true true false 8000 Text 0 0,First,#,Donation Locations,Address,0,8000;City "City" true true false 8000 Text 0 0,First,#,Donation Locations,City,0,8000;Zip "Zip" true true false 4 Long 0 0,First,#,Donation Locations,Zip,-1,-1;Phone "Phone" true true false 8000 Text 0 0,First,#,Donation Locations,Phone,0,8000;Lion_responsible "Lion responsible" true true false 8000 Text 0 0,First,#,Donation Locations,Lion_responsible,0,8000;NEAR_DIST "NEAR_DIST" true true false 8 Double 0 0,First,#,Donation Locations,NEAR_DIST,-1,-1',
#    sort_field="NEAR_DIST ASCENDING"
#)
#######Exports as CSV table so that PyCharm Console can display



dfinal=pd.read_csv(out_table)
print("")
print("~~|   Here are the closest locations, from closest distance to furthest:")
print("")
print(dfinal)
print("")
print("~~|   Now Opening ArcGIS Pro...")
print("~~|   Thank You and Have a Nice Day.   |~~~")
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")





#print("~~|   Changing Symbology of Donation Locations")
#lyr=m.listLayers("Donation Locations")[0]
#sym=lyr.symbology
#sym.renderer.symbol.applySymbolFromGallery("Tear Pin") #selects tear pin symbol
#sym.renderer.symbol.color={'RGB':[0,169,230,0]}   #Sets color to Blue
#sym.renderer.symbol.outlinecolor={'RGB':[0,0,0,0]}
#sym.renderer.symbol.size=11
#lyr.symbology=sym
#print("~~|   Symbology Changed")

#print("~~|   Changing Symbology of User Location")
#lyr=m.listLayers("User Location")[0]
#sym=lyr.symbology
#sym.renderer.symbol.applySymbolFromGallery("Hexagon")
#sym.renderer.symbol.color={'RGB':[255,165,0,0]} #sets color to Orange
#sym.renderer.symbol.outlinecolor
#sym.renderer.symbol.size=11
#lyr.symbology=sym
#print("~~|   Symbology Changed")


