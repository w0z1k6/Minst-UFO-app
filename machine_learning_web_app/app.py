import streamlit as st
from streamlit_drawable_canvas import st_canvas
from tensorflow import keras
import numpy as np
from pathlib import Path

from preprocess import preprocess_canvas, preprocess_for_display, batch_for_model

APP_DIR = Path(__file__).resolve().parent


@st.cache_resource
def load_model():
    return keras.models.load_model(APP_DIR / "mnist.hdf5")


model_new = load_model()

st.title("MNIST Digit Recognizer")

SIZE = 192

canvas_result = st_canvas(
    fill_color="#ffffff",
    stroke_width=8,
    stroke_color="#ffffff",
    background_color="#000000",
    height=150,
    width=150,
    drawing_mode="freedraw",
    key="canvas",
)

if canvas_result.image_data is not None:
    st.write("Input Image (预处理后)")
    st.image(preprocess_for_display(canvas_result.image_data, SIZE))
    st.caption("已自动：灰度 → 居中缩放 → 归一化，与 MNIST 训练格式对齐")

if st.button("Predict"):
    if canvas_result.image_data is None:
        st.warning("请先在画板上写一个数字")
    else:
        batch = preprocess_canvas(canvas_result.image_data)
        pred = model_new.predict(batch_for_model(batch, model_new), verbose=0)
        st.write(f"result: {np.argmax(pred[0])}")
        st.bar_chart(pred[0])
