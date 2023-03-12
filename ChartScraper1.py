import pandas as pd
import os
import arcpy   #for functions that have to run in ArcGIS Pro

gdbpath=r"E:\OneDriveMain\OneDrive\_GisProjects\2023Projects\ProjectLeo\Default.gdb"
print("~~|  Geodatabase Path Set to:" + gdbpath)
aprx.defaultGeodatabase=gdbpath   #setting up defualt gdb for arcpy results

df = pd.read_html('http://www.austindowntownlions.org/Eyeglasses_Recycling')#Correct Web Address
print("   ")
print("~~| Reading Info From Website...")
dfa = df[1]#(skiprows=1,header=0)
print(dfa)
firstcsv=r"D:\ScratchFolder\firstcsv.csv"
dfa.to_csv(firstcsv)
print("   ")
print("~~| Saved as CSV File... ")
dfb = pd.read_csv(firstcsv,skiprows=1, header=0,index_col='Facility') #removes row, sets header to new first row
#Sets index column to facility, auto deletes numeric first column
print("   ")
print("~~| Formatting Data... ")
dfb=dfb.drop(dfb.columns[[0]],axis=1) #removes extra column
print(dfb) #removing first row sucessful to this point
csvfinal=r"D:\ScratchFolder\csvfinal.csv"
dfb.to_csv(csvfinal) #for testing csv at this point, has 2 extra colums
print("   ")
print("~~| Output to CSV LionsTable")

#Setting up to output to GDB
OutTableName="LionsTable"
arcpy.conversion.TableToTable(csvfinal,gdbpath,OutTableName) #Converting and adding to gdb
print("   ")
print("~~| Converted to table in ArcGIS...")

#####Setting up for Geocode Address function
tabletogeocode=(gdbpath+"\LionsTable")
locatorname=(r"E:\OneDriveMain\OneDrive\_GISProjects\2023Projects\ProjectLeo\AustinLocatorDelta.loc")
addressfieldmap=("\'Address or Place\' Address VISIBLE NONE;Address2 <None> VISIBLE NONE;Address3 <None> VISIBLE NONE;"+
                "Neighborhood <None> VISIBLE NONE;\'City\' City VISIBLE NONE;County <None> VISIBLE NONE;"+
                 "State <None> VISIBLE NONE;\'Zip\' Zip VISIBLE NONE;Zip4 <None> VISIBLE NONE;Country <None> VISIBLE NONE")
outclass=(gdbpath+"\GeocodedDonationLocations.shp")
loctype="ADDRESS_LOCATION"
outfieldchoice="LOCATION_ONLY"

arcpy.geocoding.GeocodeAddresses(tabletogeocode,locatorname,addressfieldmap,outclass,locationtype=loctype,output_fields=outfieldchoice)
######Geocoding the Table and adding point layer to Default GDB
print("   ")
print("~~|  Attempting to Geocode Table Locations...")


############Attempting to add LionsTable to Map
######May not be needed, going to try to process table from filename and add to Gdb with filename/arcpy

#aprx=arcpy.mp.ArcGISProject(r"E:\OneDriveMain\OneDrive\_GISProjects\2023Projects\ProjectLeo\ProjectLeo.aprx")
#addTab=arcpy.mp.Table(r"E:\OneDRiveMain\OneDrive\_GISProjects\2023Projects\ProjectLeo\Default.gdb\LionsTable")
#m=aprx.listMaps("Lions*")[0]
#arcpy.RefreshTOC() #Setting up default map as project map and adding LionsTable to it

##################################################
