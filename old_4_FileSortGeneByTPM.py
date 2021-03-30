# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 22:17:28 2020

@author: MyGuest
"""


import os
import pandas as pd

directory = r'C:\Users\MyGuest\Documents\GBMproject'
for entry in os.scandir(directory):
    if entry.path.endswith(".htseq.counts") and entry.is_file():        
        f=open(entry.path,'r')
        df = pd.DataFrame(pd.read_csv(f, sep='\t', header=None, names=['val1', 'val2'], skipfooter=5, engine='python'))
        # print(df["val2"].sum())
        df.loc[:,"val3"] = df.loc[:,"val2"].div(df["val2"].sum()).multiply(1000000)
        df=df.sort_values(['val2'],ascending=0)
        df.to_csv(entry.path+'.out', header=None,sep='\t', index=0, encoding='utf-8')
