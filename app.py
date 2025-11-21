import streamlit as st
import gradio as gr
from PIL import Image, ImageOps
import numpy as np

st.set_page_config(page_title="Sketch Mask Editor", layout="wide")

st.title("Sketch Mask Editor")

# Instructions
st.markdown("""
Draw a mask on the canvas below. The output will show your mask as an image.
""")

# Dummy function for Gradio: converts drawing to a binary mask
def create_mask(image):
    if image is None:
        return None
    # Convert to grayscale
    img = Image.fromarray(image).convert("L")
    # Binarize (0 or 255)
    mask = img.point(lambda p: 255 if p > 0 else 0)
    return np.array(mask)

# Gradio Interface
gr_interface = gr.Interface(
    fn=create_mask,
    inputs=gr.Image(source="canvas", tool="sketch", type="numpy"),
    outputs=gr.Image(type="numpy"),
    live=True,
    title="Draw Your Mask",
    description="Draw on the canvas to generate a binary mask."
)

# Launch Gradio in share mode to get a public URL
launch_result = gr_interface.launch(prevent_thread_lock=True, share=True)

# Extract URL
gradio_url = launch_result[0] if isinstance(launch_result, tuple) else None

# Embed in Streamlit
if gradio_url:
    st.components.v1.iframe(gradio_url, height=500, scrolling=True)
else:
    st.error("Gradio URL could not be retrieved. Make sure 'share=True' works.")
