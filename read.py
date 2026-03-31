import pandas as pd

df = pd.read_csv('server_logs.csv')
print(df.to_string())