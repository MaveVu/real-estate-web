import streamlit as st
import pandas as pd
import altair as alt
import random
from utilities import get_ranking, visualize_score, visualize_median, label_hist_pred

@st.cache_data
def load(file):
    df = pd.read_csv(file)
    return df

def main():
    st.title("Find information about a suburb")
    
    # Load data
    file = 'data/hist_and_pred_median.csv'
    file_2 = 'data/suburb_score.csv'

    data = load(file)
    scores = load(file_2)

    ranking = get_ranking(scores)
    label_hist_pred(data)
    ranking.rename(columns={'total_score': 'score'}, inplace=True)
    
    
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
        st.write(f'Historical and Predicted Median Prices in {selected_suburb}')
        visualize_median(data, selected_suburb)
        st.write(f'Score for {selected_suburb}')
        visualize_score(data, ranking, selected_suburb)
        
# Run
if __name__ == '__main__':
    main()
