import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import numpy as np
import cv2
from io import BytesIO

st.set_page_config(layout="wide")

st.title("🎨 Mask Drawer")

uploaded_file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    img = Image.open(uploaded_file).convert("RGB")

    # Get dimensions
    w, h = img.size

    # THE FIX: Always resize background manually — prevents Streamlit Cloud crash
    bg = img.resize((w, h))

    st.write("👉 Draw directly on the image below:")

    canvas_result = st_canvas(
        background_image=bg,        # MUST be PIL, not base64
        width=w,
        height=h,
        drawing_mode="freedraw",
        stroke_width=25,
        stroke_color="red",
        update_streamlit=True,
        key="canvas_editor"
    )

    if canvas_result.image_data is not None:

        # Extract only the drawing layer
        drawn = canvas_result.image_data[:, :, :3]

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

        # Save mask
        buf = BytesIO()
        mask_img.save(buf, format="PNG")
        st.download_button(
            "Download Mask",
            buf.getvalue(),
            "mask.png",
            "image/png"
        )


