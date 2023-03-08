import pandas as pd
import os
import arcpy   #for functions that have to run in ArcGIS Pro

df = pd.read_html('http://www.austindowntownlions.org/Eyeglasses_Recycling') #Correct Web Address
dfa = df[1]#(skiprows=1,header=0)
print(dfa)
firstcsv=r"J:\firstcsv"
dfa.to_csv(firstcsv)
dfb = pd.read_csv(firstcsv,skiprows=1, header=0)
print(dfb) #removing first row sucessful to this point



csvtesta=r"J:\csvtesta"
dfb.to_csv(csvtesta) #for testing csv at this point, has 2 extra colums



#csvlocation=r"J:LionsLocations.csv"
#df[1].to_csv(csvlocation) #Saves to CSV file, can write to locations py has permissions to

#gdblocation=r"E:\OneDriveDCCCD\ProjectLeo\ProjectLeo.gdb" #Setting up to output to GDB
#OutTableName="LionsTable"
#arcpy.conversion.TableToTable(csvlocation,gdblocation,OutTableName) #Converting and adding to gdb

#arcpy.geocoding.GeocodeLocationsFromTable(LionsTable,)

