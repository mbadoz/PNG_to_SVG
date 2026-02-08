import streamlit as st
import cv2
import numpy as np
import converter
import io

st.set_page_config(page_title="PNG to SVG Converter", layout="centered")

st.title("PNG to SVG Converter")
st.write("Upload a PNG image to convert it to SVG vector format.")

uploaded_file = st.file_uploader("Choose a PNG image", type=["png"])

if uploaded_file is not None:
    # 1. Read the file
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    if image is not None:
        col1, col2 = st.columns(2)
        
        with col1:
            st.image(image, channels="BGR", caption="Original Image", use_container_width=True)

        # 2. Convert
        with st.spinner("Converting..."):
            try:
                # convert_to_svg returns the SVG content as a string
                svg_content = converter.convert_to_svg(image)
                
                with col2:
                    st.success("Conversion Successful!")
                    st.write("您的 SVG 已准备好 (Your SVG is ready)")
                    
                    # Create a download button
                    st.download_button(
                        label="Download SVG",
                        data=svg_content,
                        file_name="converted.svg",
                        mime="image/svg+xml"
                    )
                    
                    # Optional: Display SVG code or preview (rendering SVG in streamlit is tricky without components)
                    with st.expander("View SVG Code"):
                        st.code(svg_content, language='xml')

            except Exception as e:
                st.error(f"An error occurred during conversion: {e}")
    else:
        st.error("Error loading image. Please try another file.")
