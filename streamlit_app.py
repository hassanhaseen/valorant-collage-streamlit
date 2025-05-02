import streamlit as st
import os
import shutil
from utils import sort_images_by_tier, generate_collages, zip_collages

# Create folders
os.makedirs("uploads", exist_ok=True)
os.makedirs("outputs", exist_ok=True)

st.set_page_config(page_title="Valorant Collage Generator", layout="centered")

st.title("🎮 Valorant Collage Generator")

uploaded_files = st.file_uploader("Upload your VALORANT skin images (1200x1200)", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

if uploaded_files:
    st.success(f"{len(uploaded_files)} files uploaded")

    # Clear previous files
    shutil.rmtree("uploads", ignore_errors=True)
    shutil.rmtree("outputs", ignore_errors=True)
    os.makedirs("uploads", exist_ok=True)
    os.makedirs("outputs", exist_ok=True)

    with st.spinner("Generating collages..."):
        # Save uploaded images
        image_paths = []
        for file in uploaded_files:
            path = os.path.join("uploads", file.name)
            with open(path, "wb") as f:
                f.write(file.read())
            image_paths.append(path)

        sorted_images = sort_images_by_tier(image_paths)
        output_files = generate_collages(sorted_images)

st.subheader("📸 Collages Generated:")

for file in output_files:
    col1, col2 = st.columns([4, 1])
    with col1:
        st.image(file, caption=os.path.basename(file), use_container_width=True)
    with col2:
        with open(file, "rb") as img_file:
            st.download_button(
                label="⬇ Download",
                data=img_file,
                file_name=os.path.basename(file),
                mime="image/jpeg"
            )

# ZIP download for all
zip_path = zip_collages(output_files)
with open(zip_path, "rb") as f:
    st.download_button("⬇ Download All Collages (ZIP)", f, file_name="collages.zip", mime="application/zip")

