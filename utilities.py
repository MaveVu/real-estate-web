import pandas as pd

def get_info(address, df):
    cols = ['parking', 'type', 'num_schools', 'cost', 'beds', 
            'baths']
    row = df[df['address'] == address]
    return row[cols]