import pandas as pd
import os
import arcpy   #for functions that have to run in ArcGIS Pro

df = pd.read_html('http://www.austindowntownlions.org/Eyeglasses_Recycling') #Correct Web Address
dfa = df[1]#(skiprows=1,header=0)
print(dfa)
firstcsv=r"J:\firstcsv.csv"
dfa.to_csv(firstcsv)
dfb = pd.read_csv(firstcsv,skiprows=1, header=0,index_col='Facility') #removes row, sets header to new first row
#Sets index column to facility, auto deletes numeric first column
dfb=dfb.drop(dfb.columns[[0]],axis=1) #removes extra column
print(dfb) #removing first row sucessful to this point
csvfinal=r"J:\csvfinal.csv"
dfb.to_csv(csvfinal) #for testing csv at this point, has 2 extra colums

#csvlocation=r"J:LionsLocations.csv"
#df[1].to_csv(csvlocation) #Saves to CSV file, can write to locations py has permissions to

#gdblocation=r"E:\OneDriveDCCCD\ProjectLeo\ProjectLeo.gdb" #Setting up to output to GDB
#OutTableName="LionsTable"
#arcpy.conversion.TableToTable(csvlocation,gdblocation,OutTableName) #Converting and adding to gdb

#arcpy.geocoding.GeocodeLocationsFromTable(LionsTable,)

