import pandas as pd
import streamlit as st
from utilities import get_info

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
        info = get_info(selected_address, data)
        
        st.write(f"Information for {selected_address}")
        st.dataframe(info, hide_index=True)


# Run
if __name__ == '__main__':
    main()

    