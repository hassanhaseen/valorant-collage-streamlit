import streamlit as st
import os
import shutil
from utils import sort_images_by_tier, generate_collages, zip_collages

# Setup folders
os.makedirs("uploads", exist_ok=True)
os.makedirs("outputs", exist_ok=True)

st.set_page_config(page_title="Valorant Collage Generator", layout="centered")

st.title("🎮 Valorant Collage Generator")

# Session state flags
if "collages_generated" not in st.session_state:
    st.session_state.collages_generated = False
    st.session_state.output_files = []

# File uploader
uploaded_files = st.file_uploader(
    "Upload your 1200x1200 VALORANT skin images",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True
)

# Handle upload + generation
if uploaded_files:
    if not st.session_state.collages_generated:
        st.success(f"{len(uploaded_files)} files uploaded")

        # Clear old folders
        shutil.rmtree("uploads", ignore_errors=True)
        shutil.rmtree("outputs", ignore_errors=True)
        os.makedirs("uploads", exist_ok=True)
        os.makedirs("outputs", exist_ok=True)

        # Save uploaded files
        image_paths = []
        for file in uploaded_files:
            path = os.path.join("uploads", file.name)
            with open(path, "wb") as f:
                f.write(file.read())
            image_paths.append(path)

        # Process and sort
        sorted_images = sort_images_by_tier(image_paths)

        with st.spinner("⚙️ Generating collages..."):
            st.session_state.output_files = generate_collages(sorted_images)
            st.session_state.collages_generated = True

# Show collages + download buttons
if st.session_state.output_files:
    st.subheader("📸 Generated Collages")
    for file in st.session_state.output_files:
        filename = os.path.basename(file)

        # Two columns: image and download button
        col1, col2 = st.columns([4, 1])
        with col1:
            st.image(file, caption=filename, use_container_width=True)
        with col2:
            with open(file, "rb") as img_file:
                st.download_button(
                    label="⬇ Download",
                    data=img_file,
                    file_name=filename,
                    mime="image/jpeg",
                    key=filename  # prevents re-render issues
                )

    # ZIP download button at the end
    zip_path = zip_collages(st.session_state.output_files)
    with open(zip_path, "rb") as zip_file:
        st.download_button(
            label="⬇ Download All Collages (ZIP)",
            data=zip_file,
            file_name="valorant_collages.zip",
            mime="application/zip"
        )
