import streamlit as st
from PIL import Image
import io
import base64

st.title("Mask Editor App")

# Upload image
uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    width, height = image.size
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Encode image to base64
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()

    # Load HTML file
    with open("mask_editor.html", "r") as f:
        html_content = f.read()

    # Insert the image base64 and dimensions into HTML
    html_content = html_content.replace("window.onloadImage = function(base64Str, width, height)", 
                                        f"window.onloadImage('{img_str}', {width}, {height})")

    # Embed HTML in Streamlit
    st.components.v1.html(html_content, height=height+100, scrolling=True)
