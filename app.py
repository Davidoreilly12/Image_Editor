import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import io
import numpy as np

st.title("Cloakdocs‑Style Mask Editor")

uploaded = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
if uploaded is not None:
    img = Image.open(uploaded).convert("RGBA")
    w, h = img.size

    st.write("Draw over the image to create a mask:")

    # Use a canvas with the image as background
    canvas_result = st_canvas(
        fill_color="rgba(255, 0, 0, 0.3)",
        stroke_width=20,
        stroke_color="red",
        background_image=img,
        update_streamlit=True,
        height=h,
        width=w,
        drawing_mode="freedraw",
        key="cloakdocs_canvas"
    )

    if canvas_result.image_data is not None:
        # Convert RGBA drawing data to mask
        mask_data = canvas_result.image_data[:, :, 3]  # alpha channel
        mask = (mask_data > 0).astype(np.uint8) * 255  # binary mask

        # Convert to PIL to allow download
        mask_pil = Image.fromarray(mask)

        st.subheader("Mask Preview")
        st.image(mask_pil, use_column_width=True)

        # Download button
        buf = io.BytesIO()
        mask_pil.save(buf, format="PNG")
        st.download_button("Download Mask", buf.getvalue(), "mask.png", "image/png")


