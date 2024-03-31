import math
import pandas as pd
from datetime import datetime, timedelta

dfs = []

for i in range (6):
    now = datetime.now()
    naxt = now - i * timedelta(minutes=10)
  
    first_part = naxt.strftime('%Y%m%d')
    hhmm_int = int(naxt.strftime('%H%M'))
    hhmm = 10 * math.floor(hhmm_int/10)
    filename = f'crypto_{first_part}_{hhmm:04d}.csv'
    uri = f'http://punchao.com/{filename}'
    
    print(uri)
    
    df = pd.read_csv(uri)
    df = df.drop('pulled_at', axis=1)
    df = df.rename(columns={'price': f'time_{hhmm}'})
    dfs.append(df)
    
    
x = dfs[0]
for i in range(6):
    if i > 0:
        x = x.merge(dfs[i], on='crypto', suffixes=('', ''))

cols = sorted(x.columns, reverse=True)
for i, col in enumerate(cols):
    if col != 'crypto':
        try:
            delta = 10000 * (x[col] - x[cols[i+1]]) / x[cols[i+1]]
            x = x.join(delta.to_frame(f'delta{i}'))
        except Exception as e:
            print(e)
            print('fer')
            
olds = list(filter(lambda x: (x != 'crypto'), cols))
x = x.drop(olds, axis=1)
        
html = x.to_html()
text_file = open("/xamp/htdocs/index.html", "w")
text_file.write(html)
text_file.close()

print(x)

