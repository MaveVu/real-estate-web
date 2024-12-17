import pandas as pd
import streamlit as st
import altair as alt
import matplotlib.pyplot as plt

# Address page
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

def get_coord(address, df):
    coords = df[df['address'] == address]['geometry']
    coords = coords.iloc[0][7:-1].split()
    return f"https://www.google.com/maps?q={coords[1]},{coords[0]}"


# Suburb page
def get_ranking(df):
    df = df.sort_values('total_score',ascending=False)
    df = df.reset_index(drop=True)
    return df

def visualize_score(data, ranking, selected_suburb):
    TOTAL = ranking.shape[0]
    # Filter the data for the selected suburb
    selected_row = ranking[ranking['suburb'] == selected_suburb].iloc[0]
    metrics = ['livability', 'affordability', 'score']
    values = [selected_row[metric] for metric in metrics]
    
    # Prepare data for Altair
    altair_data = pd.DataFrame({
        'Metric': metrics,
        'Value': values,
        'Color': ['blue', 'green', 'orange']
    })

    bars = (
        alt.Chart(altair_data)
        .mark_bar()
        .encode(
            x=alt.X('Metric', title=None, axis=alt.Axis(labelAngle=0)),
            y=alt.Y('Value', title='Score', scale=alt.Scale(domain=[0, max(values) * 1.1])),
            color=alt.Color('Color', scale=None),  # Use the 'Color' column for individual bar colors
            tooltip=['Metric', 'Value']
        )
    )

    chart = bars.properties(
        width=600,
        height=400
    )
    
    # Display the chart in Streamlit
    st.altair_chart(chart, use_container_width=True)
    st.markdown(f"<h2 style='color: white;'>Score Rank: {selected_row.name + 1} / {TOTAL}</h2>", unsafe_allow_html=True)

def label_hist_pred(data):
    data['label'] = 'predicted'
    data.loc[data['year'] <= 2024, 'label'] = 'historical'

def visualize_median(data, selected_suburb):
    data = data[data['suburb'] == selected_suburb]
    historical_data = data[data['label'] == 'historical']
    predicted_data = pd.concat([data[data['year'] == 2024], data[data['label'] == 'predicted']])

    historical_chart = alt.Chart(historical_data).mark_line(
        color='blue',
        strokeWidth=6  # Solid line for historical data
    ).encode(
        x='year:O',  # Ordinal axis for year
        y=alt.Y('median_rental_price:Q', title='price'), # Quantitative axis for median rental price
        tooltip=['year', 'median_rental_price', 'suburb']
    )

    # Create a line chart for predicted data
    predicted_chart = alt.Chart(predicted_data).mark_line(
        color='red',
        strokeDash=[10, 5],
        strokeWidth=6  # Dashed line for predicted data
    ).encode(
        x='year:O',
        y=alt.Y('median_rental_price:Q', title='price'),
        tooltip=['year', 'median_rental_price', 'suburb']
    )

    chart = historical_chart + predicted_chart
    st.altair_chart(chart, use_container_width=True)

def add_total_and_rename(df):
    count = df['SA2_Name'].value_counts()
    df['total_props'] = df['SA2_Name'].map(count)
    info_cols = ['total_props', 'Net_migration_2022_23', 'ERP_per_km2_2023', 'ERP_increase_2022_23', 
                 'NUMBER_OF_JOBS_PERSONS_2020-21', 'MEDIAN_INCOME_PERSONS_2020-21']
    new_cols = ['Total number of rental properties', 'Net migration in 2022-2023', 'ERP per km2 in 2023'
                , 'Increase of ERP in 2022-2023', 'Number of employed people in 2020-2021',
                'Median income of people in 2020-2021']
    cols = dict(zip(info_cols, new_cols))
    df.rename(columns=cols, inplace=True)
    return df[['SA2_Name'] + new_cols]

def get_suburb_info(df, selected_suburb):
    info = pd.DataFrame(df[df['SA2_Name'] == selected_suburb].iloc[0])
    info = info.iloc[1:]
    st.table(info)

# House page
def get_min_max_closest(df, selected_suburb):
    minmax = dict()
    df_suburb = df[df['SA2_Name'] == selected_suburb]
    cols = [col for col in df_suburb.columns if 'closest' in col]
    cols = [col for col in cols if 'distance' in col]
    cols1 = [col.split('_')[1] for col in cols]
    for i in range(len(cols)):
        # +-5 for range
        mincol = df_suburb[cols[i]].min() - 5 if df_suburb[cols[i]].min() - 5 >= 0 else 0
        maxcol = df_suburb[cols[i]].max() + 5
        avg = (mincol+maxcol)//2
        minmax[cols1[i]] = [mincol, maxcol, avg]
    return minmax

def get_info_for_train(df, selected_suburb):
    info = df[df['SA2_Name'] == selected_suburb].iloc[0]
    columns = ['Net_migration_2021_22', 'Net_migration_2022_23', 'ERP_per_km2_2021',
                'ERP_per_km2_2022', 'ERP_per_km2_2023', 'ERP_increase_2020_21', 'ERP_increase_2021_22', 'ERP_increase_2022_23',
                'NUMBER_OF_JOBS_PERSONS_2020-21', 'MEDIAN_INCOME_PERSONS_2020-21']
    return info[columns]

