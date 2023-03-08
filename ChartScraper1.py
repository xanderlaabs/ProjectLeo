import pandas as pd
import os
import arcpy   #for functions that have to run in ArcGIS Pro

df = pd.read_html('https://www.austindowntownlions.org/Eyeglasses_Recycling') #Correct Web Address

print(df[1]) #Selects Index 1 of 0,1,2 , then prints out here to confirm

csvlocation=r"J:LionsLocations.csv"
df[1].to_csv(csvlocation) #Saves to CSV file, can write to locations py has permissions to

#gdblocation=r"E:\OneDriveDCCCD\ProjectLeo.gdb" #Setting up to output to GDB
#arcpy.conversion.TableToTable(csvlocation,gdblocation,LionsTable) #Converting and adding to gdb

#arcpy.geocoding.GeocodeLocationsFromTable(LionsTable,)

