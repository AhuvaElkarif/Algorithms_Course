import sys
import numpy as np
import cv2

def rgb_to_hsv_manual(r, g, b):
    """
    Manual conversion from RGB to HSV color space.
    
    Args:
        r, g, b: RGB values in range [0, 255]
    
    Returns:
        h: Hue in degrees [0, 360)
        s: Saturation in percentage [0, 100]
        v: Value in percentage [0, 100]
    """
    # Normalize RGB values to [0, 1]
    r_norm = r / 255.0
    g_norm = g / 255.0
    b_norm = b / 255.0
    
    # Calculate max, min, and delta
    max_val = max(r_norm, g_norm, b_norm)
    min_val = min(r_norm, g_norm, b_norm)
    delta = max_val - min_val
    
    # Calculate Value
    v = max_val
    
    # Calculate Saturation
    if max_val == 0:
        s = 0
    else:
        s = delta / max_val
    
    # Calculate Hue
    if delta == 0:
        h = 0
    elif max_val == r_norm:
        h = 60 * (((g_norm - b_norm) / delta) % 6)
    elif max_val == g_norm:
        h = 60 * (((b_norm - r_norm) / delta) + 2)
    else:  # max_val == b_norm
        h = 60 * (((r_norm - g_norm) / delta) + 4)
    
    # Return H in degrees, S and V in percentage
    return h, s * 100, v * 100

def rgb_to_hsl_manual(r, g, b):
    """
    Manual conversion from RGB to HSL color space.
    
    Args:
        r, g, b: RGB values in range [0, 255]
    
    Returns:
        h: Hue in degrees [0, 360)
        s: Saturation in percentage [0, 100]
        l: Lightness in percentage [0, 100]
    """
    # Normalize RGB values to [0, 1]
    r_norm = r / 255.0
    g_norm = g / 255.0
    b_norm = b / 255.0
    
    # Calculate max, min, and delta
    max_val = max(r_norm, g_norm, b_norm)
    min_val = min(r_norm, g_norm, b_norm)
    delta = max_val - min_val
    
    # Calculate Lightness
    l = (max_val + min_val) / 2
    
    # Calculate Saturation
    if delta == 0:
        s = 0
    else:
        s = delta / (1 - abs(2 * l - 1))
    
    # Calculate Hue
    if delta == 0:
        h = 0
    elif max_val == r_norm:
        h = 60 * (((g_norm - b_norm) / delta) % 6)
    elif max_val == g_norm:
        h = 60 * (((b_norm - r_norm) / delta) + 2)
    else:  # max_val == b_norm
        h = 60 * (((r_norm - g_norm) / delta) + 4)
    
    # Return H in degrees, S and L in percentage
    return h, s * 100, l * 100

def rgb_to_ycrcb_manual(r, g, b):
    """
    Manual conversion from RGB to YCrCb color space (ITU-R BT.601 standard).
    
    Args:
        r, g, b: RGB values in range [0, 255]
    
    Returns:
        y: Luma component [0, 255]
        cr: Red-difference chroma component [0, 255]
        cb: Blue-difference chroma component [0, 255]
    """
    # ITU-R BT.601 conversion formula
    y = 0.299 * r + 0.587 * g + 0.114 * b
    cr = 128 + 0.713 * (r - y)
    cb = 128 + 0.564 * (b - y)
    
    return y, cr, cb

def rgb_to_hsv_opencv(r, g, b):
    """
    Conversion from RGB to HSV using OpenCV's cv2.cvtColor function.
    
    Args:
        r, g, b: RGB values in range [0, 255]
    
    Returns:
        h: Hue in degrees [0, 360)
        s: Saturation in percentage [0, 100]
        v: Value in percentage [0, 100]
    """
    # Create a single pixel in BGR format (OpenCV uses BGR instead of RGB)
    rgb_pixel = np.uint8([[[b, g, r]]])
    
    # Convert to HSV
    hsv_pixel = cv2.cvtColor(rgb_pixel, cv2.COLOR_BGR2HSV)
    h, s, v = hsv_pixel[0][0]
    
    # Convert to standard format: OpenCV uses H∈[0,180], S,V∈[0,255]
    # We convert to H∈[0,360), S,V∈[0,100]
    return float(h) * 2, float(s) / 255 * 100, float(v) / 255 * 100

def rgb_to_hls_opencv(r, g, b):
    """
    Conversion from RGB to HLS using OpenCV's cv2.cvtColor function.
    Note: OpenCV returns HLS (Hue, Lightness, Saturation), not HSL.
    
    Args:
        r, g, b: RGB values in range [0, 255]
    
    Returns:
        h: Hue in degrees [0, 360)
        s: Saturation in percentage [0, 100]
        l: Lightness in percentage [0, 100]
    """
    # Create a single pixel in BGR format (OpenCV uses BGR instead of RGB)
    rgb_pixel = np.uint8([[[b, g, r]]])
    
    # Convert to HLS
    hls_pixel = cv2.cvtColor(rgb_pixel, cv2.COLOR_BGR2HLS)
    h, l, s = hls_pixel[0][0]  # Note: OpenCV returns HLS order
    
    # Convert to standard format: OpenCV uses H∈[0,180], L,S∈[0,255]
    # We convert to H∈[0,360), L,S∈[0,100]
    return float(h) * 2, float(s) / 255 * 100, float(l) / 255 * 100

def rgb_to_ycrcb_opencv(r, g, b):
    """
    Conversion from RGB to YCrCb using OpenCV's cv2.cvtColor function.
    
    Args:
        r, g, b: RGB values in range [0, 255]
    
    Returns:
        y: Luma component [0, 255]
        cr: Red-difference chroma component [0, 255]
        cb: Blue-difference chroma component [0, 255]
    """
    # Create a single pixel in BGR format (OpenCV uses BGR instead of RGB)
    rgb_pixel = np.uint8([[[b, g, r]]])
    
    # Convert to YCrCb
    ycrcb_pixel = cv2.cvtColor(rgb_pixel, cv2.COLOR_BGR2YCrCb)
    y, cr, cb = ycrcb_pixel[0][0]
    
    return float(y), float(cr), float(cb)

def main():
    """
    Main function to convert RGB color to HSV, HSL, and YCrCb color spaces.
    Compares manual calculation with OpenCV's cv2.cvtColor function.
    """
    # Check command line arguments
    if len(sys.argv) != 4:
        print("Usage: python color_converter.py R G B")
        print("Example: python color_converter.py 255 128 64")
        sys.exit(1)
    
    # Parse and validate RGB values
    try:
        r = int(sys.argv[1])
        g = int(sys.argv[2])
        b = int(sys.argv[3])
        
        if not (0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255):
            print("Error: RGB values must be in range [0, 255]")
            sys.exit(1)
    except ValueError:
        print("Error: RGB values must be integers")
        sys.exit(1)
    
    # Print header
    print(f"\n{'='*60}")
    print(f"Converting RGB({r}, {g}, {b}) to different color spaces")
    print(f"{'='*60}\n")
    
    # HSV Conversion
    print("HSV Conversion:")
    print("-" * 60)
    h_manual, s_manual, v_manual = rgb_to_hsv_manual(r, g, b)
    print(f"Manual calculation:  H={h_manual:.2f}°, S={s_manual:.2f}%, V={v_manual:.2f}%")
    
    h_cv, s_cv, v_cv = rgb_to_hsv_opencv(r, g, b)
    print(f"OpenCV cv2.cvtColor: H={h_cv:.2f}°, S={s_cv:.2f}%, V={v_cv:.2f}%")
    
    h_diff = abs(h_manual - h_cv)
    s_diff = abs(s_manual - s_cv)
    v_diff = abs(v_manual - v_cv)
    print(f"Differences:         ΔH={h_diff:.2f}°, ΔS={s_diff:.2f}%, ΔV={v_diff:.2f}%\n")
    
    # HSL Conversion
    print("HSL Conversion:")
    print("-" * 60)
    h_manual, s_manual, l_manual = rgb_to_hsl_manual(r, g, b)
    print(f"Manual calculation:  H={h_manual:.2f}°, S={s_manual:.2f}%, L={l_manual:.2f}%")
    
    h_cv, s_cv, l_cv = rgb_to_hls_opencv(r, g, b)
    print(f"OpenCV cv2.cvtColor: H={h_cv:.2f}°, S={s_cv:.2f}%, L={l_cv:.2f}%")
    
    h_diff = abs(h_manual - h_cv)
    s_diff = abs(s_manual - s_cv)
    l_diff = abs(l_manual - l_cv)
    print(f"Differences:         ΔH={h_diff:.2f}°, ΔS={s_diff:.2f}%, ΔL={l_diff:.2f}%\n")
    
    # YCrCb Conversion
    print("YCrCb Conversion:")
    print("-" * 60)
    y_manual, cr_manual, cb_manual = rgb_to_ycrcb_manual(r, g, b)
    print(f"Manual calculation:  Y={y_manual:.2f}, Cr={cr_manual:.2f}, Cb={cb_manual:.2f}")
    
    y_cv, cr_cv, cb_cv = rgb_to_ycrcb_opencv(r, g, b)
    print(f"OpenCV cv2.cvtColor: Y={y_cv:.2f}, Cr={cr_cv:.2f}, Cb={cb_cv:.2f}")
    
    y_diff = abs(y_manual - y_cv)
    cr_diff = abs(cr_manual - cr_cv)
    cb_diff = abs(cb_manual - cb_cv)
    print(f"Differences:         ΔY={y_diff:.2f}, ΔCr={cr_diff:.2f}, ΔCb={cb_diff:.2f}\n")
    
    # Print footer
    print("=" * 60)
    print("See 'answers.txt' for analysis of differences")
    print("=" * 60)

if __name__ == "__main__":
    main()