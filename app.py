import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import numpy as np
import cv2
from io import BytesIO

st.set_page_config(layout="wide")

st.title("🎨 Working Mask Drawer (Streamlit + Colab Compatible)")

uploaded_file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    # Load image
    img = Image.open(uploaded_file).convert("RGB")

    # Force RGBA → REQUIRED for st_canvas to not be blank
    bg = img.convert("RGBA")

    w, h = bg.size

    st.write("👉 Draw on the image:")

    canvas_result = st_canvas(
        background_image=bg,      # MUST be RGBA
        width=w,
        height=h,
        drawing_mode="freedraw",
        stroke_width=20,
        stroke_color="red",
        key="canvas"
    )

    if canvas_result.image_data is not None:
        drawing = canvas_result.image_data[:, :, :3]

        gray = cv2.cvtColor(drawing, cv2.COLOR_RGB2GRAY)
        mask = (gray < 240).astype(np.uint8) * 255

        mask_img = Image.fromarray(mask)

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Original")
            st.image(img)

        with col2:
            st.subheader("Generated Mask")
            st.image(mask_img)

        # Download button
        buf = BytesIO()
        mask_img.save(buf, format="PNG")
        st.download_button(
            "Download Mask",
            buf.getvalue(),
            "mask.png",
            "image/png"
        )


