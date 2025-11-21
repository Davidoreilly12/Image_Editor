import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import numpy as np
import cv2

st.title("Draw Mask on Image")

uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    # Open image as PIL
    original = Image.open(uploaded_file).convert("RGBA")
    orig_w, orig_h = original.size

    # Determine max canvas size for page
    MAX_WIDTH = 900
    scale = min(1.0, MAX_WIDTH / orig_w)
    canvas_w = int(orig_w * scale)
    canvas_h = int(orig_h * scale)

    # Resize image for canvas
    canvas_img = original.resize((canvas_w, canvas_h))

    st.write("Draw directly on the image:")

    # Create canvas
    canvas_result = st_canvas(
        background_image=canvas_img,
        height=canvas_h,
        width=canvas_w,
        drawing_mode="freedraw",
        stroke_color="red",
        stroke_width=10,
        update_streamlit=True,
        key="canvas",
    )

    if canvas_result.image_data is not None:
        # Extract drawing layer
        drawing = canvas_result.image_data[:, :, :3]
        gray = cv2.cvtColor(drawing.astype(np.uint8), cv2.COLOR_RGB2GRAY)

        # Create mask from non-white pixels
        mask_small = (gray < 250).astype(np.uint8) * 255

        # Resize mask to original size
        mask = cv2.resize(mask_small, (orig_w, orig_h), interpolation=cv2.INTER_NEAREST)

        st.subheader("Original Image")
        st.image(original)

        st.subheader("Mask")
        st.image(mask)




