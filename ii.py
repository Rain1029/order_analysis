import pandas as pd
s = pd.DataFrame(data=[[3, 4], [12, 34], [121, 2]], 
                 index=["a", "b", "c"],
                 columns=["j", "k"])
print(s)
df = pd.read_csv('data/raw_orders.csv')
df.info()
df.dropna(subset=['city'])
df.info()