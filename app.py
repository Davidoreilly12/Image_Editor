import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import numpy as np
import cv2

st.title("Draw Mask on Image")

# 1️⃣ Upload
uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    # 2️⃣ Open image as PIL
    original = Image.open(uploaded_file).convert("RGBA")
    orig_w, orig_h = original.size

    # 3️⃣ Scale for canvas to avoid huge canvas
    MAX_WIDTH = 900
    if orig_w > MAX_WIDTH:
        scale = MAX_WIDTH / orig_w
        canvas_w = MAX_WIDTH
        canvas_h = int(orig_h * scale)
        canvas_img = original.resize((canvas_w, canvas_h))
    else:
        canvas_w, canvas_h = orig_w, orig_h
        canvas_img = original

    st.write("Draw directly on the image:")

    # 4️⃣ Draw on the canvas
    canvas_result = st_canvas(
        background_image=canvas_img,   # MUST be PIL Image
        height=canvas_h,
        width=canvas_w,
        drawing_mode="freedraw",
        stroke_color="red",
        stroke_width=10,
        update_streamlit=True,
        key="canvas",
    )

    if canvas_result.image_data is not None:
        # 5️⃣ Extract drawing layer only
        drawing = canvas_result.image_data[:, :, :3]
        gray = cv2.cvtColor(drawing.astype(np.uint8), cv2.COLOR_RGB2GRAY)

        # Threshold to get mask
        mask_small = (gray < 250).astype(np.uint8) * 255  # all non-white areas

        # Resize mask back to original size
        mask = cv2.resize(mask_small, (orig_w, orig_h), interpolation=cv2.INTER_NEAREST)

        st.subheader("Original Image")
        st.image(original)

        st.subheader("Mask")
        st.image(mask)




