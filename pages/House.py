import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from rf_train import train_rf_model

@st.cache_data
def get_rf_model():
    return train_rf_model()

def load(file):
    df = pd.read_csv(file)
    return df

def main():
    st.title("Predict the rental price for a property")

    # getting the data
    file = 'data/houses_all_properties.csv'
    houses = load(file)

    # getting the rf model
    rf_model = get_rf_model()

    



