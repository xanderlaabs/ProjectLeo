import pandas as pd
import os
import arcpy

df = pd.read_html('https://www.austindowntownlions.org/Eyeglasses_Recycling') #Correct Web Address

print(df[1]) #Selects Index 1 of 0,1,2 , then prints out here to confirm
df[1].to_csv('LionsLocations.csv') #Saves to CSV file


