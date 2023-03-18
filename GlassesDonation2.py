import pandas as pd
import os
import arcpy#for functions that have to run in ArcGIS Pro
import csv

p=arcpy.mp.ArcGISProject(r"E:\OneDriveMain\OneDrive\_GISProjects\2023Projects\ProjectLeo\ProjectLeo.aprx")
m=p.listMaps()[0]
DonationLayer=m.listLayers()[0]
UserLayer=m.listLayers()[1]

print("~~|   Calculating closest location to User Address...")
arcpy.analysis.Near(
    in_features=DonationLayer,
    near_features=UserLayer,
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



#dfinal=pd.read_csv(out_table)
#print("")
#print("~~|   Here are the closest locations, from closest distance to furthest:")
#print("")
#print(dfinal)
#print("")
#print("~~|   Now Opening ArcGIS Pro...")
#print("~~|   Thank You and Have a Nice Day.   |~~~")
#print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
