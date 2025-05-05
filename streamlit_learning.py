import streamlit as st

st.title("Streamlit")
st.write("Hello Python")
st.balloons()
st.image("https://www.streamlit.io/images/brand/streamlit-mark-color.png")
x = st.slider("Select number",min_value=1,max_value=10)
st.write("The square of ",x,"is", x*x)
st.video("C:\Users\somay\Downloads\Untitled video - Made with Clipchamp.mp4")
a = st.text_input("Enter your name")
st.write("Your Name is : ",a)