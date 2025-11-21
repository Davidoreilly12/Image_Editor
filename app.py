import streamlit as st
import gradio as gr
import numpy as np
from PIL import Image

st.title("Image Mask Drawer")

# Upload an image
uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Original Image", use_column_width=True)

    # Define a function that returns the mask drawn by the user
    def get_mask(mask):
        """
        mask: a numpy array returned from gr.Sketchpad
        """
        if mask is None:
            return np.zeros((image.height, image.width), dtype=np.uint8)
        # Convert mask to binary
        return (mask[:, :, 0] > 0).astype(np.uint8) * 255

    # Launch Gradio Sketchpad inside Streamlit
    mask = gr.Sketchpad(
        image=image,  # initial image as background
        shape=(image.height, image.width),
        brush_radius=5,
        invert_colors=False,
    ).launch(inline=True)  # inline embeds in Streamlit

    # Show mask if available
    if mask is not None:
        st.subheader("Mask Output")
        st.image(mask, channels="L", use_column_width=True)

