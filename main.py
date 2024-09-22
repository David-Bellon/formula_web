import streamlit as st

st.title("My First Streamlit Webpage")

# Add a header
st.header("Welcome to My Streamlit App")

# Add a subheader
st.subheader("This is a simple interactive web application")

# Add some text
st.write("Streamlit is an open-source Python library that makes it easy to create and share beautiful, custom web apps for machine learning and data science.")

# Add a slider
age = st.slider("Select your age:", 0, 100, 25)
st.write(f"Your age is {age}.")

# Add a button
if st.button("Click me!"):
    st.write("Button clicked!")