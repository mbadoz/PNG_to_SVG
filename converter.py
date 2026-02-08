import cv2
import svgwrite
import numpy as np
import argparse
import os

def convert_to_svg(image, output_path=None):
    """
    Converts a PNG image (numpy array or file path) to an SVG string or file.
    
    Args:
        image: Path to image (str) or numpy array (cv2 image).
        output_path: If provided, saves the SVG to this path.
        
    Returns:
        The SVG content as a string.
    """
    # 1. Load the image
    if isinstance(image, str):
        img = cv2.imread(image)
        if img is None:
            raise FileNotFoundError(f"Could not open or find the image: {image}")
    else:
        img = image

    # 2. Preprocess (Grayscale + Thresholding)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Simple binary thresholding (invert if needed based on background)
    # Assuming dark object on light background, we use binary_inv to get object as white (255)
    # Adjust threshold value (127) as needed or use Otsu's binarization
    _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)

    # 3. Find Contours
    # RETR_EXTERNAL retrieves only the extreme outer contours
    # CHAIN_APPROX_SIMPLE compresses horizontal, vertical, and diagonal segments
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 4. Create SVG
    height, width = img.shape[:2]
    # Use memory buffer instead of file path for svgwrite if output_path is None or we want string
    dwg = svgwrite.Drawing(filename=output_path if output_path else "temp.svg", profile='tiny', size=(width, height))

    print(f"Found {len(contours)} contours.")

    for contour in contours:
        # Approximate contour to reduce points (smoother curve)
        epsilon = 0.005 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        
        # Convert contour points to a list of tuples for svgwrite
        # contour is shape (N, 1, 2), we need list of (x, y)
        points = [(float(pt[0][0]), float(pt[0][1])) for pt in approx]
        
        if len(points) > 2:
            # Draw the polygon
            # fill='black' ensures the shape is filled
            dwg.add(dwg.polygon(points, fill='black'))

    if output_path:
        dwg.save()
        print(f"SVG saved to {output_path}")
        return dwg.tostring()
    else:
        return dwg.tostring()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert PNG to SVG using Contour Tracing")
    parser.add_argument("input", help="Path to input PNG file")
    parser.add_argument("--output", "-o", help="Path to output SVG file (optional)")
    
    args = parser.parse_args()
    
    try:
        convert_to_svg(args.input, args.output)
    except Exception as e:
        print(f"Error: {e}")
