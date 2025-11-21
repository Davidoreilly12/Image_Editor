import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import numpy as np
import cv2

st.set_page_config(layout="wide")

MAX_CANVAS_WIDTH = 900   # keep canvas safe for Streamlit Cloud


st.title("🖌️ Draw Mask on Image")

uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    # Load original image
    original = Image.open(uploaded_file).convert("RGBA")
    orig_w, orig_h = original.size

    # Compute scaled size for canvas
    if orig_w > MAX_CANVAS_WIDTH:
        scale = MAX_CANVAS_WIDTH / orig_w
        canvas_w = MAX_CANVAS_WIDTH
        canvas_h = int(orig_h * scale)
    else:
        canvas_w, canvas_h = orig_w, orig_h

    # Create scaled image for canvas
    canvas_img = original.resize((canvas_w, canvas_h))

    st.write("Draw directly on the image:")

    canvas_result = st_canvas(
        background_image=canvas_img,
        height=canvas_h,
        width=canvas_w,
        drawing_mode="freedraw",
        stroke_color="red",
        stroke_width=20,
        update_streamlit=True,
        key="canvas",
    )

    if canvas_result.image_data is not None:
        # Drawing is same size as canvas
        drawing = canvas_result.image_data[:, :, :3]

        # Convert drawing to a binary mask
        gray = cv2.cvtColor(drawing, cv2.COLOR_RGB2GRAY)
        mask_small = (gray < 200).astype(np.uint8) * 255

        # Resize mask back to original resolution so your pipeline works
        mask = cv2.resize(mask_small, (orig_w, orig_h), interpolation=cv2.INTER_NEAREST)

        # Display outputs
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Original Image")
            st.image(original)

        with col2:
            st.subheader("Generated Mask (Original Size)")
            st.image(mask)



