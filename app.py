import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import numpy as np
import cv2

st.title("Interactive Image Editing App")

# Load an image
uploaded_file = st.file_uploader("Upload an image", type=["png","jpg","jpeg"])
if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Original Image", use_column_width=True)

    # Create a canvas for mask drawing
    canvas_result = st_canvas(
        fill_color="rgba(255, 255, 255, 255)",  # color for drawing
        stroke_width=5,
        stroke_color="black",
        background_image=image,
        height=image.height,
        width=image.width,
        drawing_mode="freedraw",  # can be 'freedraw', 'rect', 'circle', 'transform'
        key="canvas"
    )

    if canvas_result.image_data is not None:
        # Convert drawn area to binary mask
        mask_array = cv2.cvtColor(canvas_result.image_data.astype(np.uint8), cv2.COLOR_RGBA2GRAY)
        _, mask_binary = cv2.threshold(mask_array, 10, 255, cv2.THRESH_BINARY)
        mask = Image.fromarray(mask_binary)
        mask.save("mask.png")
        st.image(mask, caption="Generated Mask", use_column_width=True)

        st.success("Mask generated! Ready for inpainting or SAM.")
