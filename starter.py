import requests
import pandas as pd


url='https://austindowntownlions.org/Eyeglass_Recycling'
pagestuff=requests.get(url).content
placelist=pd.read_html(pagestuff,match='.+')
placelistdata=placelist
print(placelistdata)
placelist.to_csv('C:\testdata1.csv')
