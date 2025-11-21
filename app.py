import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import numpy as np
import cv2
import base64
from io import BytesIO

st.set_page_config(layout="wide")

def pil_to_base64(img: Image.Image):
    buf = BytesIO()
    img.save(buf, format="PNG")
    img_bytes = buf.getvalue()
    return "data:image/png;base64," + base64.b64encode(img_bytes).decode()

st.title("🎨 Accurate Mask Drawer")

uploaded_file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    img = Image.open(uploaded_file).convert("RGB")
    img_np = np.array(img)
    h, w = img_np.shape[:2]

    # Convert to base64 so fabric.js can load it
    img_b64 = pil_to_base64(img)

    st.write("👉 Draw directly on the image below:")

    canvas_result = st_canvas(
        background_image=img_b64,     # <- BASE64 FIX
        width=w,
        height=h,
        drawing_mode="freedraw",
        stroke_width=30,
        stroke_color="red",
        update_streamlit=True,
        key="canvas",
    )

    if canvas_result.image_data is not None:
        drawn = canvas_result.image_data[:, :, :3].astype(np.uint8)

        gray = cv2.cvtColor(drawn, cv2.COLOR_RGB2GRAY)
        mask = (gray < 250).astype(np.uint8) * 255

        mask_img = Image.fromarray(mask)

        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Original")
            st.image(img)
        with c2:
            st.subheader("Mask")
            st.image(mask_img)

        st.download_button(
            "Download Mask",
            data=mask_img.tobytes(),
            file_name="mask.png",
            mime="image/png"
        )

