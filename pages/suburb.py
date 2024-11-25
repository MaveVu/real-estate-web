import streamlit as st
import pandas as pd
import altair as alt
import random

@st.cache_data
def load(file):
    df = pd.read_csv(file)
    return df

def main():
    st.title("Find information about a suburb")
    
    # Load data
    file = 'data/hist_and_pred_median.csv'
    file_2 = 'data/suburb_ranking.csv'

    data = load(file)
    ranking = load(file_2)
    ranking.rename(columns={'SA2_Name': 'suburb', 'total_score': 'score'}, inplace=True)
    
    
    TOTAL = ranking.shape[0]

    if 'shuffled_suburbs' not in st.session_state:
        shuffled_suburbs = ranking['suburb'].tolist()
        random.shuffle(shuffled_suburbs)
        st.session_state.shuffled_suburbs = shuffled_suburbs

    selected_suburb = st.selectbox("Search a suburb",
                                    options=st.session_state.shuffled_suburbs,
                                    index=None,
                                    placeholder="Select a suburb"
                                    ) 

    # Check if a suburb is selected
    if selected_suburb:
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
            title=f"Scores for {selected_suburb}",
            width=600,
            height=400
        )
        
        # Display the chart in Streamlit
        st.altair_chart(chart, use_container_width=True)

        st.markdown(f"<h2 style='color: white;'>Score Rank: {selected_row.name + 1} / {TOTAL}</h2>", unsafe_allow_html=True)
# Run
if __name__ == '__main__':
    main()
