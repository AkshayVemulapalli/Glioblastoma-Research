import os
import pandas as pd

os.chdir('./GDC_DATA/')
directory = r'.'
for entry in os.scandir(directory):
    if entry.path.endswith(".htseq.counts") and entry.is_file():        
        f=open(entry.path,'r')
        df = pd.DataFrame(pd.read_csv(f, sep='\t', header=None, names=['val1', 'val2'], skipfooter=5, engine='python'))        
        df=df.sort_values(['val2'],ascending=0)
        df.loc[:,"val3"] = df.loc[:,"val2"].div(df["val2"].sum()).multiply(1000000)
        df.loc[:,"val4"] = 'No'
        df.loc[df.head(100).index,"val4"] = 'Yes'

        df.to_csv(entry.path+'.out', header=None,sep='\t', index=0, encoding='utf-8')