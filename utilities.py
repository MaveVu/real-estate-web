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

    # Step 3: Combine the two charts
    chart = historical_chart + predicted_chart

    # Step 4: Display the Altair chart in Streamlit
    st.altair_chart(chart, use_container_width=True)
