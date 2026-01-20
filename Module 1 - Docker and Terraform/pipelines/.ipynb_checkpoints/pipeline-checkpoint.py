import sys
import pandas as pd
import os

print('System arguments', sys.argv)

month = int(sys.argv[1])

print(f'hello pipeline, month= {month}')


df = pd.DataFrame({"day" : [1,2], "num_passengers":[3,4]})
df["month"] = month

df.to_parquet(f"output_{month}.parquet")

print(df.head())
print(os.getcwd())