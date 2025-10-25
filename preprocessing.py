import pandas as pd

# The four files can be found on government site, because of their size I decided to not put them here
df_cara = pd.read_csv("data/caracteristiques.csv", encoding='latin1')
df_lieux = pd.read_csv("data/lieux.csv", encoding='latin1')
df_usagers = pd.read_csv("data/usagers.csv", encoding='latin1')
df_vehicules = pd.read_csv("data/vehicules.csv", encoding='latin1')


# Lighten the data 1: keep only data between 2015 and 2020
# Why 2015 - 2020?
# => Because from 2020 to 2022 the traffic was highly impacted by Covid-19
# => Because before 2015 the data is less reliable
# => Because there are currently no data after 2023
df_vehicules = df_vehicules[(df_vehicules["annee"] > 2014) & (df_vehicules["annee"] < 2020)]
df_cara = df_cara[(df_cara["annee"] > 2014) & (df_cara["annee"] < 2020)]
df_lieux = df_lieux[(df_lieux["annee"] > 2014) & (df_lieux["annee"] < 2020)]
df_usagers = df_usagers[(df_usagers["annee"] > 2014) & (df_usagers["annee"] < 2020)]

# Lighten the data 2: dropping som columns
df_lieux = df_lieux[["vma", "situ", "surf", "catr", "num_acc"]]
df_vehicules = df_vehicules.drop(columns=["manv","annee"])
df_usagers = df_usagers.drop(columns=["annee","etatp"])

# Merging
df_merged = pd.merge(df_cara, df_lieux, on="num_acc", how='inner')
df_merged = pd.merge(df_merged, df_usagers, on="num_acc", how='inner')
df_merged = pd.merge(df_merged, df_vehicules, on="num_acc", how='inner')

df_merged.to_csv("data/merged_data.csv", index=False)