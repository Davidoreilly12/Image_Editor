import streamlit as st
import gradio as gr
import numpy as np
from PIL import Image
import io

st.set_page_config(page_title="Image Mask Editor", layout="wide")

st.title("Draw Custom Masks on Images")

# Upload an image
uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Original Image", use_column_width=True)

    # Function that receives the sketch and returns it as a mask
    def process_mask(sketch_img):
        """
        sketch_img is a numpy array of the sketchpad output.
        Returns an RGBA mask image (white drawing on transparent background)
        """
        if sketch_img is None:
            return None
        mask = np.array(sketch_img)
        # Convert white strokes on transparent background
        # If sketch has alpha channel, keep it
        if mask.shape[2] == 4:
            return Image.fromarray(mask)
        else:
            # Add alpha channel
            alpha = (mask.sum(axis=2) > 0).astype(np.uint8) * 255
            mask_rgba = np.dstack([mask, alpha])
            return Image.fromarray(mask_rgba)

    # Create Gradio sketchpad interface
    iface = gr.Interface(
        fn=process_mask,
        inputs=gr.Sketchpad(
            label="Draw mask here",
            shape=image.size[::-1],  # Gradio expects (height, width)
            brush_radius=10
        ),
        outputs=gr.Image(type="pil", label="Mask Output"),
        live=True
    )

    # Embed Gradio in Streamlit
    gradio_html = iface.embed()
    st.components.v1.html(gradio_html, height=650, scrolling=True)

    st.info("Draw on the canvas to create your mask. The mask will appear below the canvas.")


