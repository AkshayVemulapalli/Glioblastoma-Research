# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 22:17:28 2020

@author: MyGuest
"""

import os, glob
import pandas as pd
    
path = r'C:\Users\MyGuest\Documents\GBMproject\Out'

all_files = glob.glob(os.path.join(path, "*.htseq.counts.out"))

all_df = []
for f in all_files:
    df = pd.read_csv(f, sep='\t', header=None, names=['gene', 'count', 'tpm'], 
                                      nrows=10, engine='python')
    df.loc[:,"top"] = 1;
    # print(df)
    all_df.append(df)
        
merged_df = pd.concat(all_df, ignore_index=False)

useful_columns = ['gene','top']
merged_df = merged_df.loc[:,useful_columns]
# print(merged_df)

top10sum_df = merged_df.groupby('gene').sum()
top10sum_df=top10sum_df.sort_values(['top'],ascending=0)
# print(top10sum_df);

top10sum_df.to_csv(r'C:\Users\MyGuest\Documents\GBMproject\Out\top10.tsv', header=None,sep='\t', 
         encoding='utf-8')

    
