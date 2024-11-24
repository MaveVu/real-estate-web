import pandas as pd

def get_info(address, df):
    cols = ['type', 'beds', 'baths', 'parking', 'num_schools', 'cost']
    column_mapping = {
        'type': 'Type of property',
        'beds': 'Number of bedrooms',
        'baths': 'Number of bathrooms',
        'parking': 'Number of parking slots',
        'num_schools': 'Number of schools nearby',
        'cost': 'Price'
    }
    
    # Filter for the row matching the address
    row = df[df['address'] == address][cols]
    
    # Rename columns
    row.rename(columns=column_mapping, inplace=True)
    return row

def closest(address, df):
    cols = [col for col in df.columns if 'closest' in col]
    row = df[df['address'] == address][cols]
    new_cols = [col.replace('_', ' ')[1:-1] for col in cols]
    new_cols = [' '.join(col.split()[1:-1]).capitalize() for col in new_cols]
    columns_mapping = dict(zip(cols, new_cols))
    row.rename(columns=columns_mapping, inplace=True)
    row = row.iloc[0]
    n = len(cols)
    close = {
        "Facility": [row.index[i] for i in range(0, n, 2)],
        "Name": [row[i] for i in range (0, n, 2)],
        "Distance (km)": [row[i] for i in range (1, n, 2)],
    }
    return pd.DataFrame(close)
