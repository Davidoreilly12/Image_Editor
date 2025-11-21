import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import numpy as np
import cv2

st.set_page_config(layout="wide")
st.title("🎨 Accurate Image Mask Drawer")

uploaded_file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    # Load image
    img = Image.open(uploaded_file).convert("RGB")
    img_np = np.array(img)

    h, w, _ = img_np.shape

    st.write("👉 Draw directly *on top* of the image below.")

    # Embed the actual image into the canvas
    canvas_result = st_canvas(
        background_image=img,              # <- THE IMPORTANT FIX
        width=w,
        height=h,
        drawing_mode="freedraw",
        stroke_width=30,
        stroke_color="red",
        update_streamlit=True,
        key="canvas",
    )

    if canvas_result.image_data is not None:
        # Extract drawing layer only
        drawn = canvas_result.image_data[:, :, :3].astype(np.uint8)

        # Detect strokes: anything not white
        gray = cv2.cvtColor(drawn, cv2.COLOR_RGB2GRAY)
        mask = (gray < 250).astype(np.uint8) * 255

        mask_img = Image.fromarray(mask)

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Original")
            st.image(img)

        with col2:
            st.subheader("Generated Mask")
            st.image(mask_img)

        st.download_button(
            "Download Mask",
            data=mask_img.tobytes(),
            file_name="mask.png",
            mime="image/png",
        )
