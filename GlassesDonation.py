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
print("")

gdbpath=r"E:\OneDriveMain\OneDrive\_GisProjects\2023Projects\ProjectLeo\Default.gdb"
print("~~|   Geodatabase Path Set to:" + gdbpath)


df = pd.read_html('http://www.austindowntownlions.org/Eyeglasses_Recycling')#Scraping Correct Web Address
print("   ")
print("~~|  Reading Info From Website...")
dfa = df[1]#(skiprows=1,header=0)
print(dfa)
firstcsv=r"D:\ScratchFolder\firstcsv.csv"
dfa.to_csv(firstcsv)
print("   ")
print("~~|  Saved as CSV File... ")
dfb = pd.read_csv(firstcsv,skiprows=1, header=0,index_col='Facility') #removes row, sets header to new first row
#Sets index column to facility, auto deletes numeric first column
print("   ")
print("~~|  Formatting Data... ")
dfb=dfb.drop(dfb.columns[[0]],axis=1) #removes extra column
print(dfb) #removing first row sucessful to this point
csvfinal=r"D:\ScratchFolder\csvfinal.csv"
dfb.to_csv(csvfinal) #for testing csv at this point, has 2 extra colums
print("   ")
print("~~|  Output to CSV LionsTable")

#Setting up to output to GDB
OutTableName="LionsTable"
arcpy.conversion.TableToTable(csvfinal,gdbpath,OutTableName) #Converting and adding Lions Locations to gdb
print("   ")
print("~~|  Lions Donation Locations Converted to table in ArcGIS...")
print("")

spottablename="SpotTable"
arcpy.conversion.TableToTable(secondcsv,gdbpath,spottablename)
print("~~|   User Address Converted to table in ArcGIS...")
print("   ")

print("~~|  Attempting to Geocode Table Locations...")
print("   ")
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
print("   ")
print("~~|  Geocoding Locations Completed...")
print("   ")

print("~~|    Geocoding User Location into Feature Class")
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
print("   ")
print("~~|    User Location Geocoded...")



print("   ")
print("~~|  Attempting to create a feature layer on the map...")
ResultPath1=r"E:\OneDriveMain\OneDrive\_GISProjects\2023Projects\ProjectLeo\Default.gdb\GeocodedDonationLocations"
##Making Feature Layer from Feature Class, adding to map
layername="Donation Locations"
layerfile1=arcpy.management.MakeFeatureLayer(ResultPath1,layername)[0]
p=arcpy.mp.ArcGISProject(r"E:\OneDriveMain\OneDrive\_GISProjects\2023Projects\ProjectLeo\ProjectLeo.aprx")
m=p.listMaps()[0]
m.addLayer(layerfile1,"TOP")
print("")
print("~~|   Donation Locations Layer Added")

print("")
print("~~|   Adding User Location Layer")
ResultPath1=r"E:\OneDriveMain\OneDrive\_GISProjects\2023Projects\ProjectLeo\Default.gdb\GeocodedUserLocation"
layername="User Location"
layerfile1=arcpy.management.MakeFeatureLayer(ResultPath1,layername)[0]
m=p.listMaps()[0]
m.addLayer(layerfile1,"TOP")

print("~~|   User Location Layer Added")

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


p.save()  #Will want to move this save around for before launching ArcGIS Pro

#arcpy.analysis.GenerateNearTable(
#    in_features="GeocodedUserLocation",
#    near_features="GeocodedDonationLocations",
 #   out_table=r"E:\OneDriveMain\OneDrive\_GISProjects\2023Projects\ProjectLeo\Default.gdb\NearTable",
 #   search_radius=None,
 #   location="NO_LOCATION",
#    angle="NO_ANGLE",
#    closest="ALL",
#    closest_count=5,
 #   method="PLANAR",
 #   distance_unit=""
#)

