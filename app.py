import streamlit as st
from PIL import Image
from streamlit_drawable_canvas import st_canvas
import numpy as np

st.title("Custom Mask Generator")

uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
if uploaded_file:
    img = Image.open(uploaded_file).convert("RGBA")  # Use RGBA for alpha channel

    # Resize canvas to match image
    canvas_result = st_canvas(
        fill_color="rgba(255, 0, 0, 0.5)",  # semi-transparent red
        stroke_width=5,
        stroke_color="red",
        background_image=img,               # PIL image here
        update_streamlit=True,
        height=img.height,
        width=img.width,
        drawing_mode="freedraw",
        key="canvas"
    )

    if canvas_result.image_data is not None:
        # Extract the alpha channel to get the mask
        mask = canvas_result.image_data[:, :, 3]  # alpha channel
        mask_binary = (mask > 0).astype(np.uint8) # 1 where drawn
        st.image(mask_binary * 255, caption="Mask", use_column_width=True)

