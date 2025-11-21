import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import io
import base64

st.title("Image Mask Editor")

# 1️⃣ Upload the base image
uploaded_file = st.file_uploader("Upload an image to annotate", type=["png", "jpg", "jpeg"])
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Original Image", use_column_width=True)

    # 2️⃣ Create a drawing canvas overlay
    canvas_result = st_canvas(
        fill_color="rgba(255, 0, 0, 0.3)",  # semi-transparent red mask
        stroke_width=20,
        stroke_color="rgba(255, 0, 0, 0.8)",
        background_image=image,
        update_streamlit=True,
        height=image.height,
        width=image.width,
        drawing_mode="freedraw",
        key="canvas",
    )

    # 3️⃣ When the user draws, export the mask automatically
    if canvas_result.image_data is not None:
        # Convert numpy array to PIL image
        mask = Image.fromarray(canvas_result.image_data.astype('uint8'), 'RGBA')

        # Display mask
        st.image(mask, caption="Generated Mask", use_column_width=True)

        # Convert mask to downloadable bytes
        buf = io.BytesIO()
        mask.save(buf, format="PNG")
        byte_im = buf.getvalue()

        # Download button
        st.download_button(
            label="Download Mask",
            data=byte_im,
            file_name="mask.png",
            mime="image/png"
        )

