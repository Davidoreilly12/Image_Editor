import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import numpy as np
import cv2

st.set_page_config(layout="wide")

st.title("🖌️ Draw Mask on Image")

uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    # Load image correctly
    img = Image.open(uploaded_file).convert("RGBA")
    w, h = img.size

    st.write("Draw on top of the image:")

    canvas_result = st_canvas(
        background_image=img,   # MUST be RGBA
        height=h,
        width=w,
        drawing_mode="freedraw",
        stroke_color="red",
        stroke_width=20,
        update_streamlit=True,
        key="canvas",
    )

    if canvas_result.image_data is not None:
        # Extract drawing layer
        drawing = canvas_result.image_data[:, :, :3]  # RGB only

        # Convert to 1-channel mask
        gray = cv2.cvtColor(drawing, cv2.COLOR_RGB2GRAY)
        mask = (gray < 200).astype(np.uint8) * 255

        mask_img = Image.fromarray(mask)

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Original")
            st.image(img)

        with col2:
            st.subheader("Generated Mask")
            st.image(mask_img)


