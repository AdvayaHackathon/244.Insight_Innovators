import streamlit as st
from PIL import Image

st.set_page_config(page_title="Rural Health AI", layout="centered")

# Display larger image
img = Image.open("logo.png")
st.image(img, width=500)  # 🔼 Increase width to 500px

# Heading aligned under the image
st.markdown(
    "<h1 style='color: #2E8B57; font-size: 36px; margin-top: -20px;'>Rural Health AI</h1>",
    unsafe_allow_html=True
)

# Button to enter the app
if st.button("Enter App"):
    st.switch_page("pages/app.py")  # ✅ Make sure app.py is in 'pages/' folder
