import pandas as pd
import streamlit as st
from utilities import get_info, closest, get_coord

@st.cache_data
def load(file):
    df = pd.read_csv(file)
    return df

def main():
    st.title("Find information about a property")
    
    # Load data
    file = 'data/houses_all_properties.csv'
    data = load(file)
    
    # Get the address column
    address = data['address']
    
    selected_address = st.selectbox("Search an addresss",
                                    options=address,
                                    index=None,
                                    placeholder="Select an address"
                                    )
    if selected_address:
        position = get_coord(selected_address, data)
        st.markdown(f"[View the (approximate) position of the property on Google Maps]({position})")
        info = get_info(selected_address, data)
        info = info.T
        cl = closest(selected_address, data)
        st.write('Property details:')
        st.table(info)
        st.write('Proximities to some **public facilities**:')
        st.table(cl)


# Run
if __name__ == '__main__':
    main()

    