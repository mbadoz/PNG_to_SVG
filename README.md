# PNG to SVG Converter 🖼️➡️✏️

Convert raster PNG images into scalable vector graphics (SVG) using Python and OpenCV.

This tool traces the contours of shapes in your image to create clean, scalable vector paths.

## Features ✨

- **Drag & Drop Interface**: Simple web GUI powered by Streamlit.
- **Contour Tracing**: Uses OpenCV to detect and vectorize shapes.
- **Command Line Tool**: Batch process images via terminal.
- **Instant Preview**: See the original and download the result immediately.

## Installation 📦

1. Clone this repository.
2. Install the required dependencies:

```bash
pip install opencv-python svgwrite streamlit numpy
```

## Usage 🚀

### 1. Graphical Interface (Recommended)

Run the web app locally:

```bash
streamlit run app.py
```

This will open your browser. Simply drag and drop a PNG image to convert it!

### 2. Command Line

You can also use the script directly in your terminal:

```bash
python converter.py path/to/your/image.png
```

It will generate a `.svg` file in the same directory.

## How it Works ⚙️

The script performs the following steps:
1. **Grayscale Conversion**: Simplifies the image data.
2. **Thresholding**: Converts the image to strictly black and white (binary).
3. **Contour Detection**: Finds the "borders" of independent shapes.
4. **Vectorization**: Draws these contours as SVG polygons.

> **Note**: This tool works best with high-contrast images, logos, and icons. Complex photos may not yield perfect results.


## License

MIT
