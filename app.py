import streamlit as st
import gradio as gr
from PIL import Image
import numpy as np

st.title("Draw Custom Masks on Images")

uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Original Image", use_column_width=True)

    def process_mask(sketch_img):
        if sketch_img is None:
            return None
        mask = np.array(sketch_img)
        # Add alpha channel if missing
        if mask.shape[2] == 4:
            return Image.fromarray(mask)
        else:
            alpha = (mask.sum(axis=2) > 0).astype(np.uint8) * 255
            mask_rgba = np.dstack([mask, alpha])
            return Image.fromarray(mask_rgba)

    # Use Gradio Blocks
    with gr.Blocks() as demo:
        sketchpad = gr.Sketchpad(label="Draw mask here", shape=image.size[::-1], brush_radius=10)
        output_img = gr.Image(type="pil", label="Mask Output")
        sketchpad.change(fn=process_mask, inputs=sketchpad, outputs=output_img)

    # Embed Gradio in Streamlit
    demo.launch(inline=True)
