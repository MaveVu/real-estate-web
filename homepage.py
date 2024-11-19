import streamlit as st

st.set_page_config(
    page_title="Real Estate Consultation",  # Title displayed in the browser tab
    page_icon=":house:",  # Icon displayed in the browser tab
    layout="centered",  # Layout: "centered" or "wide"
    initial_sidebar_state="expanded",  # Sidebar state: "expanded" or "collapsed"
)


st.title("Real Estate Consulting Website")
st.sidebar.success("Select a page above")

st.header("About the website")
st.write("""
This is the project that my teammates and I did in the MAST30034 - Applied Data Science
course at the University of Melbourne. In this project, our primary data was collected
from Domain.com - an Australian real estate website. We used several models (Linear Regression
and Random Forest) to predict the current rental prices and also give the predictions
for the rental prices in the next 3 years. After that, we formed a
metric to rank Victorian suburbs based on their livability and affordability. 
The code can be found here: ...
""")

