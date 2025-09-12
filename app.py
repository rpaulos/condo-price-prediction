import streamlit as st

st.sidebar.title("Options")
st.sidebar.write("This is in the sidebar.")

st.title("Hello Streamlit!")
st.write("This is my first Streamlit app.")
name = st.text_input("Enter your name:")
if name:
    st.success(f"Hi {name}, welcome!")


