import streamlit as st
import streamlit.components.v1 as components
import base64
from PIL import Image
import io

st.title("Custom Mask Drawing")

# HTML/JS Canvas
canvas_html = """
<canvas id="sketch" width="512" height="512" style="border:1px solid black;"></canvas>
<br>
<button onclick="saveCanvas()">Save</button>
<script>
const canvas = document.getElementById('sketch');
const ctx = canvas.getContext('2d');
let drawing = false;

canvas.addEventListener('mousedown', () => { drawing = true; });
canvas.addEventListener('mouseup', () => { drawing = false; ctx.beginPath(); });
canvas.addEventListener('mousemove', draw);

function draw(e) {
    if(!drawing) return;
    ctx.lineWidth = 10;
    ctx.lineCap = 'round';
    ctx.strokeStyle = 'black';
    ctx.lineTo(e.offsetX, e.offsetY);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(e.offsetX, e.offsetY);
}

// Send the canvas data back to Streamlit
function saveCanvas() {
    const dataURL = canvas.toDataURL('image/png');
    const input = document.createElement('input');
    input.type = 'text';
    input.value = dataURL;
    input.id = 'canvas_data';
    document.body.appendChild(input);
}
</script>
"""

# Embed the canvas
components.html(canvas_html, height=600)

# Grab the saved data from the JS input
canvas_data = st.experimental_get_query_params().get("canvas_data")
if canvas_data:
    data_url = canvas_data[0]
    header, encoded = data_url.split(",", 1)
    binary_data = base64.b64decode(encoded)
    image = Image.open(io.BytesIO(binary_data))
    st.image(image, caption="Your Mask")
