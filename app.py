import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
import io
import base64

st.title("Draw Mask on Uploaded Image")

# Upload an image
uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    # Load image
    image = Image.open(uploaded_file)
    image = image.convert("RGB")
    width, height = image.size

    # Convert image to base64
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()

    # HTML + JS for canvas drawing on top of image
    canvas_html = f"""
    <div>
        <canvas id="sketch" width="{width}" height="{height}" 
                style="border:1px solid black; background-image: url(data:image/png;base64,{img_str}); 
                       background-size: contain; background-repeat: no-repeat;"></canvas>
        <br>
        <button onclick="saveCanvas()">Save Mask</button>
    </div>
    <script>
    const canvas = document.getElementById('sketch');
    const ctx = canvas.getContext('2d');
    let drawing = false;

    canvas.addEventListener('mousedown', () => {{ drawing = true; }});
    canvas.addEventListener('mouseup', () => {{ drawing = false; ctx.beginPath(); }});
    canvas.addEventListener('mousemove', draw);

    function draw(e) {{
        if(!drawing) return;
        ctx.lineWidth = 10;
        ctx.lineCap = 'round';
        ctx.strokeStyle = 'black';
        ctx.lineTo(e.offsetX, e.offsetY);
        ctx.stroke();
        ctx.beginPath();
        ctx.moveTo(e.offsetX, e.offsetY);
    }}

    function saveCanvas() {{
        const dataURL = canvas.toDataURL('image/png');
        const pyInput = document.createElement('input');
        pyInput.type = 'text';
        pyInput.value = dataURL;
        pyInput.id = 'canvas_data';
        document.body.appendChild(pyInput);
    }}
    </script>
    """

    # Embed the canvas
    components.html(canvas_html, height=height + 100)

    st.info("After drawing, click 'Save Mask' on the canvas. Copy the base64 string from the browser console if needed.")

