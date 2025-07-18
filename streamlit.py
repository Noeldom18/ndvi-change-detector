# -*- coding: utf-8 -*-
"""Streamlit.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1PrzSu3KU5fHEpCK7uBJMGx0r1IUBhoEw
"""

# Install required packages
!pip install streamlit opencv-python-headless matplotlib pillow pyngrok

# Set your ngrok authtoken here (replace the string below)
!ngrok authtoken 2z2zfkR0zEbBq3s3r4N7RUy8rEB_TGLhZGbbqbxJWSNbEd8K

import streamlit as st
import numpy as np
import cv2
import matplotlib.pyplot as plt
from PIL import Image
import io
from pyngrok import ngrok
import subprocess
import sys

# Write Streamlit app code to a file
code = '''
import streamlit as st
import numpy as np
import cv2
import matplotlib.pyplot as plt
from PIL import Image

st.set_page_config(page_title="NDVI Change Detection", layout="centered")

st.title("🌿 NDVI Change Detection Web App")
# 🧭 Wikipedia-style layout begins
st.markdown("""
## Overview
This web application analyzes NDVI images captured by drones over agricultural fields on different days.
It calculates the change in plant health using visual patterns and shows areas of **growth**, **stress**, or **no significant change**.

## Purpose
To help farmers, researchers, and agronomists track plant health over time and take data-driven action.

---
## How It Works
- Upload two NDVI screenshots (from Day 1 and Day 6)
- The app aligns and compares them
- It displays:
  - A heatmap showing areas of change
  - A summary of how much of the field improved, declined, or stayed stable
""")

# Sidebar Content
st.sidebar.title("🗂️ App Sidebar")

st.sidebar.markdown("### 🔧 How to Use")
st.sidebar.markdown("""
1. Upload two NDVI images (Day 1 and Day 6).
2. Images must be similar in field coverage.
3. App calculates pixel-wise changes.
4. See which areas improved or declined.
""")

st.sidebar.markdown("---")
st.sidebar.markdown("### 📌 Project Info")
st.sidebar.markdown("""
- **Project:** Crop Health Monitoring
- **Tech:** NDVI, Drone, Python, Streamlit
- **Drone:** DJI Mavic 3M
""")

day1_file = st.file_uploader("📤 Upload Day 1 NDVI Screenshot", type=["jpg", "jpeg", "png"])
day6_file = st.file_uploader("📤 Upload Day 6 NDVI Screenshot", type=["jpg", "jpeg", "png"])

if day1_file and day6_file:
    day1_img = Image.open(day1_file).convert("RGB")
    day6_img = Image.open(day6_file).convert("RGB")
    day1_np = np.array(day1_img)
    day6_np = np.array(day6_img)

    if day1_np.shape != day6_np.shape:
        st.warning("🔁 Resizing Day 6 image to match Day 1...")
        day6_np = cv2.resize(day6_np, (day1_np.shape[1], day1_np.shape[0]))

    gray_day1 = cv2.cvtColor(day1_np, cv2.COLOR_RGB2GRAY) / 255.0
    gray_day6 = cv2.cvtColor(day6_np, cv2.COLOR_RGB2GRAY) / 255.0

    ndvi_diff = gray_day6 - gray_day1

    growth_mask = ndvi_diff > 0.05
    stress_mask = ndvi_diff < -0.05
    stable_mask = (ndvi_diff >= -0.05) & (ndvi_diff <= 0.05)

    total_pixels = ndvi_diff.size
    growth_pixels = np.sum(growth_mask)
    stress_pixels = np.sum(stress_mask)
    stable_pixels = np.sum(stable_mask)

    st.subheader("📊 NDVI Change Classification")
    st.markdown(f"""
    - 🟩 **Growth** Area: {growth_pixels} pixels ({(growth_pixels/total_pixels)*100:.2f}%)
    - 🟥 **Stress** Area: {stress_pixels} pixels ({(stress_pixels/total_pixels)*100:.2f}%)
    - 🟨 **No Change** Area: {stable_pixels} pixels ({(stable_pixels/total_pixels)*100:.2f}%)
    """)

    fig, ax = plt.subplots(figsize=(8, 4))
    im = ax.imshow(ndvi_diff, cmap='RdYlGn', vmin=-1, vmax=1)
    plt.colorbar(im, ax=ax, label='NDVI Change')
    ax.set_title("NDVI Change Map (Day 6 - Day 1)")
    ax.axis('off')
    st.pyplot(fig)
else:
    st.info("👆 Please upload both images to proceed.")
'''

with open("ndvi_app.py", "w") as f:
    f.write(code)

# Open a tunnel to the streamlit port 8501 with correct port format
public_url = ngrok.connect("8501")  # <-- pass port as string
print(f"🚀 Your Streamlit app will be live at:\n{public_url}\n")


# Run the Streamlit app in the background
proc = subprocess.Popen([sys.executable, "-m", "streamlit", "run", "ndvi_app.py", "--server.port", "8501"])