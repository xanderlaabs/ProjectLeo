import pandas as pd

df = pd.read_html('https://www.austindowntownlions.org/Eyeglasses_Recycling')

print(df[1])

