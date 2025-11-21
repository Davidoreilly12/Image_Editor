import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import io
import numpy as np

st.title("Full-Size Image Mask Editor")

uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
if uploaded_file:
    # Load the image
    image = Image.open(uploaded_file)
    
    # Use the image dimensions for canvas
    canvas_result = st_canvas(
        fill_color="rgba(255,0,0,0.3)",  # semi-transparent fill
        stroke_width=15,
        stroke_color="rgba(255,0,0,0.8)",
        background_image=image,
        update_streamlit=True,
        height=image.height,
        width=image.width,
        drawing_mode="freedraw",
        key="canvas_fullsize",
    )

    if canvas_result.image_data is not None:
        # Convert drawn canvas to mask
        mask = Image.fromarray(canvas_result.image_data.astype("uint8"), "RGBA")
        st.image(mask, caption="Mask Overlay", use_column_width=True)

        # Optional: save automatically
        mask.save("mask.png")
        st.success("Mask saved as mask.png")


