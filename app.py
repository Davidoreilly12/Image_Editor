import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import io

st.title("Image Mask Editor with Zoom")

uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
if uploaded_file:
    image = Image.open(uploaded_file)
    
    # Resize for canvas display
    max_dim = 800  # max canvas width or height
    ratio = min(max_dim / image.width, max_dim / image.height, 1)
    display_size = (int(image.width*ratio), int(image.height*ratio))
    display_image = image.resize(display_size)
    
    canvas_result = st_canvas(
        fill_color="rgba(255,0,0,0.3)",
        stroke_width=15,
        stroke_color="rgba(255,0,0,0.8)",
        background_image=display_image,
        update_streamlit=True,
        height=display_image.height,
        width=display_image.width,
        drawing_mode="freedraw",
        key="canvas_zoom",
    )

    if canvas_result.image_data is not None:
        # Convert to original image size mask
        mask_small = Image.fromarray(canvas_result.image_data.astype('uint8'), 'RGBA')
        mask = mask_small.resize(image.size)
        st.image(mask, caption="Mask (original size)", use_column_width=True)


