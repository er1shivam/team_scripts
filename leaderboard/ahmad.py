import pandas as pd
import csv

df = pd.read_csv('ahmad.csv')

df = df[['Call Date','Name', 'Email', 'Call Host', 'Booking Source', 'Offer Made?', 'Deposit Taken?', "Disqualified by Call?", 'Closed?']]
print(df.info())

df_filtered = df[df['Offer Made?'] == 'Yes']
df_filtered = df_filtered[df_filtered['Closed?'] != 'Yes']
df_filtered = df_filtered[df_filtered['Closed?'] != '‚Äé']
df_filtered = df_filtered[df_filtered['Disqualified by Call?'] != 'Yes']
df_filtered = df_filtered[df_filtered['Deposit Taken?'] != 'Yes']
print(df_filtered.info())

newdf = df[['Call Date','Name', 'Email', 'Call Host', 'Booking Source']]
df_filtered.to_csv('ahmad_output.csv')
