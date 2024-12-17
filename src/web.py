import os
import tempfile
import cv2
import numpy as np
import streamlit as st
from PIL import Image
import zipfile
import io
from .processor import ImageProcessor
from .utils import create_circular_mask


def main():
    st.set_page_config(
        page_title="FaceCrop",
        page_icon="👤",
        layout="wide",
    )

    st.title("FaceCrop - Face Detection and Cropping Tool")
    st.markdown(
        """
    Upload one or more images to detect faces and create cropped versions with optional circular mask.
    The tool will automatically detect faces and create properly cropped images.
    """
    )

    # Initialize processor
    processor = ImageProcessor()

    # Sidebar controls
    st.sidebar.header("Settings")
    circular_mask = st.sidebar.checkbox("Apply Circular Mask", value=False)
    strict_mode = st.sidebar.checkbox(
        "Strict Mode (More accurate but may miss faces)", value=False
    )

    # File uploader for multiple files
    uploaded_files = st.file_uploader(
        "Choose images...",
        type=["jpg", "jpeg", "png", "webp"],
        accept_multiple_files=True,
    )

    if uploaded_files:
        # Create a container for all images
        image_container = st.container()

        # Create a zip buffer for all processed images
        zip_buffer = io.BytesIO()
        successful_processes = 0
        processed_images = []  # Store processed images for zip creation

        # Process each uploaded file
        for uploaded_file in uploaded_files:
            with image_container:
                st.markdown(f"### Processing: {uploaded_file.name}")
                col1, col2 = st.columns(2)

                # Read and display original image
                file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
                img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

                with col1:
                    st.subheader("Original Image")
                    st.image(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

                # Process image
                with tempfile.NamedTemporaryFile(
                    suffix=".png", delete=False
                ) as tmp_input, tempfile.NamedTemporaryFile(
                    suffix=".png", delete=False
                ) as tmp_output:
                    # Save uploaded file to temporary location
                    cv2.imwrite(tmp_input.name, img)

                    # Process the image
                    success = processor.process_image(
                        tmp_input.name,
                        tmp_output.name,
                        circular_mask=circular_mask,
                        strict=strict_mode,
                    )

                    if success:
                        successful_processes += 1
                        with col2:
                            st.subheader("Processed Image")
                            processed_img = Image.open(tmp_output.name)
                            st.image(processed_img)

                            # Store processed image data for zip
                            output_filename = f"processed_{os.path.splitext(uploaded_file.name)[0]}.png"
                            with open(tmp_output.name, "rb") as f:
                                processed_images.append((output_filename, f.read()))

                            # Individual download button
                            with open(tmp_output.name, "rb") as file:
                                btn = st.download_button(
                                    label=f"Download processed {uploaded_file.name}",
                                    data=file,
                                    file_name=output_filename,
                                    mime="image/png",
                                )
                    else:
                        with col2:
                            st.error(
                                f"No face detected in {uploaded_file.name}. Try disabling strict mode or uploading a different image."
                            )

                    # Cleanup temporary files
                    os.unlink(tmp_input.name)
                    os.unlink(tmp_output.name)

                # Add a separator between images
                st.markdown("---")

        # Create zip file after processing all images
        if successful_processes > 0:
            with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
                for filename, data in processed_images:
                    zf.writestr(filename, data)

            # Add download all button
            st.sidebar.markdown("### Batch Download")
            zip_buffer.seek(0)
            st.sidebar.download_button(
                label=f"Download All Processed Images ({successful_processes})",
                data=zip_buffer.getvalue(),
                file_name="processed_images.zip",
                mime="application/zip",
            )


if __name__ == "__main__":
    main()
