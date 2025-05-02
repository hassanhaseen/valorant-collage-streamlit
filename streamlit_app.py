import streamlit as st
import os
import shutil
import base64
from utils import sort_images_by_tier, generate_collages, zip_collages

# Setup folders
os.makedirs("uploads", exist_ok=True)
os.makedirs("outputs", exist_ok=True)

# Page config
st.set_page_config(page_title="Valorant Collage Generator", layout="wide")
st.title("🎮 Valorant Collage Generator")

# Session state init
if "collages_generated" not in st.session_state:
    st.session_state.collages_generated = False
if "output_files" not in st.session_state:
    st.session_state.output_files = []

# Upload section (no 'key' used!)
uploaded = st.file_uploader(
    "Upload your 1200x1200 VALORANT skin images",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True
)

# Generate button
generate = st.button("🚀 Generate Collages")

# Generate collages only on button click
if generate and uploaded:
    st.session_state.collages_generated = False
    st.session_state.output_files = []

    # Clean folders
    shutil.rmtree("uploads", ignore_errors=True)
    shutil.rmtree("outputs", ignore_errors=True)
    os.makedirs("uploads", exist_ok=True)
    os.makedirs("outputs", exist_ok=True)

    # Save files
    image_paths = []
    for file in uploaded:
        path = os.path.join("uploads", file.name)
        with open(path, "wb") as f:
            f.write(file.read())
        image_paths.append(path)

    # Sort and generate
    sorted_images = sort_images_by_tier(image_paths)
    with st.spinner("⚙️ Generating collages..."):
        st.session_state.output_files = generate_collages(sorted_images)
        st.session_state.collages_generated = True

# Display collages
if st.session_state.collages_generated and st.session_state.output_files:
    st.markdown("## 📸 Generated Collages")

    # Show 5 collages in one row
    cols = st.columns(5)
    for i, file in enumerate(st.session_state.output_files):
        with cols[i]:
            filename = os.path.basename(file)
            st.image(file, caption=f"Collage {i+1}", use_container_width=True)

            # Centered custom download button
            with open(file, "rb") as img_file:
                b64 = base64.b64encode(img_file.read()).decode()
                download_html = f'''
                <div style="text-align:center; margin-top:10px;">
                    <a href="data:file/jpg;base64,{b64}" download="{filename}">
                        <button style="
                            background-color:#ff4655;
                            border:none;
                            color:white;
                            padding:10px 24px;
                            font-size:14px;
                            border-radius:5px;
                            cursor:pointer;
                            width:100%;
                            transition:0.3s;">
                            ⬇ Download
                        </button>
                    </a>
                </div>
                '''
                st.markdown(download_html, unsafe_allow_html=True)

    # ZIP download button (below row)
    zip_path = zip_collages(st.session_state.output_files)
    with open(zip_path, "rb") as zip_file:
        st.markdown("---")
        st.download_button(
            label="⬇ Download All Collages (ZIP)",
            data=zip_file,
            file_name="valorant_collages.zip",
            mime="application/zip"
        )
