import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image, ImageOps
import numpy as np
import cv2

st.set_page_config(page_title="Mask Drawer", layout="wide")
st.title("🎨 Draw Mask on Image")

uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    # Load image
    img = Image.open(uploaded_file).convert("RGB")
    img_w, img_h = img.size

    st.write("Draw over the area to isolate. Anything you draw becomes the mask.")

    # Canvas for drawing
    canvas = st_canvas(
        fill_color="rgba(255, 0, 0, 0.4)",       # transparent red fill
        stroke_color="red",
        stroke_width=25,
        background_image=img,
        update_streamlit=True,
        height=img_h,
        width=img_w,
        drawing_mode="freedraw",
        key="canvas",
    )

    if canvas.image_data is not None:
        # Convert overlay to mask
        overlay = canvas.image_data[:, :, :3]  # drop alpha
        overlay_gray = cv2.cvtColor(overlay.astype(np.uint8), cv2.COLOR_RGB2GRAY)

        # Mask: any non-white pixel is part of the drawing
        mask = (overlay_gray < 250).astype(np.uint8) * 255
        mask_pil = Image.fromarray(mask)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Original Image")
            st.image(img)

        with col2:
            st.subheader("Generated Mask")
            st.image(mask_pil)

        # Downloadable mask
        st.download_button(
            label="Download Mask",
            data=mask_pil.tobytes(),
            file_name="mask.png",
            mime="image/png",
        )

        # If you want to send mask to your pipeline:
        st.success("Mask generated and ready for processing!")
