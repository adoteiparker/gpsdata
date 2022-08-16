import streamlit as st

data = st.session_state['data']


st.header('Data Header')    
st.write(data.head())

st.header('Data Statistics')    
st.write(data.describe())