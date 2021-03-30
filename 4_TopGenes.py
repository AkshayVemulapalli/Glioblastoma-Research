# -*- coding: utf-8 -*-
import os, glob
import pandas as pd

numTopGenes = 100
    
path = r'./GDC_DATA'

all_files = glob.glob(os.path.join(path, "*.htseq.counts.out"))

all_df = []
for f in all_files:
    df = pd.read_csv(f, sep='\t', header=None, names=['gene', 'count', 'tpm', 'HL'], nrows=numTopGenes, engine='python')
    df.loc[:,"top"] = 1;
    # print(df)
    all_df.append(df)
        
merged_df = pd.concat(all_df, ignore_index=False)

useful_columns = ['gene','top']
merged_df = merged_df.loc[:,useful_columns]
# print(merged_df)

topsum_df = merged_df.groupby('gene').sum()
topsum_df=topsum_df.sort_values(['top'],ascending=0)
# print(topsum_df);

topsum_df.to_csv(r'./out_4_topGenes.tsv', header=None,sep='\t', encoding='utf-8')

    