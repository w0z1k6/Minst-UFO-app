"""
UFO Sighting Predictor — Streamlit 单体版（用于 Streamlit Cloud 部署）

本地也可运行:
    streamlit run app.py
"""

import pickle
from pathlib import Path

import numpy as np
import streamlit as st

MODEL_PATH = Path(__file__).resolve().parent / "ufo-model.pkl"
COUNTRIES = ["Australia", "Canada", "Germany", "UK", "US"]


@st.cache_resource
def load_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"找不到模型: {MODEL_PATH}")
    with open(MODEL_PATH, "rb") as f:
        return pickle.load(f)


st.set_page_config(page_title="UFO Predictor", page_icon="🛸", layout="centered")

st.title("🛸 UFO Appearance Prediction 👽")
st.markdown(
    "根据 **目击持续时间（秒）**、**纬度**、**经度**，"
    "预测 UFO 最可能出现在哪个国家。"
)

model = load_model()

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    seconds = st.number_input(
        "Seconds（秒）",
        min_value=1,
        max_value=60,
        value=50,
        step=1,
    )

with col2:
    latitude = st.number_input("Latitude（纬度）", value=44.0, format="%.4f")

with col3:
    longitude = st.number_input("Longitude（经度）", value=-12.0, format="%.4f")

st.caption("💡 示例: seconds=50, latitude=44, longitude=-12")

st.divider()

if st.button("Predict country where the UFO is seen", type="primary", use_container_width=True):
    features = np.array([[int(seconds), float(latitude), float(longitude)]])
    prediction = int(model.predict(features)[0])
    country = COUNTRIES[prediction]
    st.success(f"**Likely country: {country}**")
    st.write(f"模型编号: `{prediction}` （0=Australia, 1=Canada, 2=Germany, 3=UK, 4=US）")

with st.sidebar:
    st.header("支持的国家")
    for i, name in enumerate(COUNTRIES):
        st.write(f"{i} → {name}")
