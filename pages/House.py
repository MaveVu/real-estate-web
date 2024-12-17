import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from rf_train import train_rf_model
from utilities import get_info_for_train, get_min_max_closest, get_ranking

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

    house_counts = houses['SA2_Name'].value_counts()
    chosen_cols = house_counts[house_counts >= 50].index

    # getting the rf model
    mapping, scaler, rf_model = get_rf_model()

    # textbox: suburb, type, bed, bath, parking, num_school, closest?
    selected_suburb = st.selectbox("Select suburb that property is in",
                                    options=chosen_cols,
                                    index=None,
                                    placeholder="Select a suburb"
                                    )
    if (selected_suburb):
        closest = get_min_max_closest(houses, selected_suburb)
        type = st.selectbox('Select the type', options=['Apartment / Unit / Flat', 'House'])
        beds = st.slider("Select number of bedrooms", min_value=1, max_value=10, value=1)
        baths = st.slider("Select number of bathrooms", min_value=1, max_value=10, value=1)
        parkings = st.slider("Select number of parking lots", min_value=0, max_value=10, value=0)
        num_schools = st.slider("Select number of nearby schools", min_value=0, max_value=20, value=0)
        train = st.number_input("Enter distance to closest train station", min_value=float(closest['train'][0]), max_value=float(closest['train'][1]), value=float(closest['train'][2]))
        tram = st.number_input("Enter distance to closest tram station", min_value=float(closest['tram'][0]), max_value=float(closest['tram'][1]), value=float(closest['tram'][2]))
        hospital = st.number_input("Enter distance to closest hospital", min_value=float(closest['hospital'][0]), max_value=float(closest['hospital'][1]), value=float(closest['hospital'][2]))
        grocery = st.number_input("Enter distance to closest grocery store", min_value=float(closest['grocery'][0]), max_value=float(closest['grocery'][1]), value=float(closest['grocery'][2]))
        info = get_info_for_train(houses, selected_suburb)

        if st.button("Submit"):
            typed_info =pd.Series([parkings, type, num_schools, beds, baths, train, tram, hospital, grocery], 
                                  index=['parking', 'type', 'num_schools', 'beds', 'baths',
                                    'closest_train_station_distance_km', 'closest_tram_station_distance_km', 'closest_hospital_distance_km',
                                    'closest_grocery_distance_km'])
            columns_to_scale = [col for col in list(typed_info.index) if 'closest' in col] + list(info.index)
            map_SA2_Name = pd.Series([mapping[selected_suburb]], index=['map_SA2_Name'])
            full_info = pd.concat([typed_info, info, map_SA2_Name])
            full_info = full_info.to_frame().T
            full_info['type'] = full_info['type'].apply(lambda x: 0 if x == 'House' else 1) 
            full_info[columns_to_scale] = scaler.transform(full_info[columns_to_scale])
            st.write(rf_model.predict(full_info))
            
            
# Run
if __name__ == '__main__':
    main()




