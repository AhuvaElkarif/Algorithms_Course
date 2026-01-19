import cv2
import numpy as np
import matplotlib.pyplot as plt

# ========== Question 1 ==========
def create_gradient_image(height, width):
    """
    Creates a grayscale image with a gradual transition from black to white
    Pixel at (0,0) is black (0), pixel at (width,height) is white (255)
    """
    img = np.zeros((height, width), dtype=np.uint8)
    
    for y in range(height):
        for x in range(width):
            # Formula for creating diagonal gradient
            value = int(((x + y) / (width + height - 2)) * 255)
            img[y, x] = value
    
    return img


# ========== Question 2 ==========
def brighten(img, b, func):
    """
    Brightens an image by adding value b to each pixel
    
    Parameters:
    img: grayscale image
    b: integer value to add to all pixels
    func: "np" or "cv2" - chooses which function to use
    
    Returns:
    brightened image
    """
    if func == "np":
        return np.add(img, b)
    elif func == "cv2":
        return cv2.add(img, b)
    else:
        raise ValueError("func must be 'np' or 'cv2'")


# ========== Question 3 ==========
def test_brighten():
    """
    Tests the differences between np.add and cv2.add
    """
    # Create gradient image
    img = create_gradient_image(300, 400)
    
    # Add 100 to each pixel
    b = 100
    
    # Using np.add
    result_np = brighten(img, b, "np")
    
    # Using cv2.add
    result_cv2 = brighten(img, b, "cv2")
    
    # Display results
    plt.figure(figsize=(15, 5))
    
    plt.subplot(1, 3, 1)
    plt.imshow(img, cmap='gray')
    plt.title('Original Image')
    plt.axis('off')
    
    plt.subplot(1, 3, 2)
    plt.imshow(result_np, cmap='gray')
    plt.title('np.add - allows overflow')
    plt.axis('off')
    
    plt.subplot(1, 3, 3)
    plt.imshow(result_cv2, cmap='gray')
    plt.title('cv2.add - saturates at 255')
    plt.axis('off')
    
    plt.tight_layout()
    plt.show()
    
    print("Difference between np.add and cv2.add:")
    print("- np.add allows overflow - values above 255 wrap around (modulo 256)")
    print("- cv2.add performs saturation - values above 255 stay at 255")
    print(f"\nExample: 200 + 100 =")
    print(f"  np.add: {np.uint8(200 + 100)} (overflow)")
    print(f"  cv2.add: {cv2.add(np.uint8(200), np.uint8(100))[0][0]} (saturation)")


# ========== Question 4 ==========
def create_low_contrast_image(fg, bg, size=400):
    """
    Creates an image with low contrast
    
    Parameters:
    fg: pixel value for foreground (background)
    bg: pixel value for background (circle)
    size: image dimensions (size x size)
    
    Returns:
    low contrast image with a circle
    """
    img = np.full((size, size), fg, dtype=np.uint8)
    
    # Draw circle in the center
    center = (size // 2, size // 2)
    radius = size // 4
    cv2.circle(img, center, radius, int(bg), -1)
    
    return img


# ========== Question 5 ==========
def normalize(img):
    """
    Performs normalization on an image
    The minimum value in the image will be 0, and the maximum 255
    Implemented without using cv2.normalize()
    
    Parameters:
    img: input grayscale image
    
    Returns:
    normalized image
    """
    # Convert to float to prevent calculation issues
    src_float = img.astype(np.float32)
    
    # Calculate min and max
    min_val = np.min(src_float)
    max_val = np.max(src_float)
    mean_val = np.mean(src_float)
    
    print(f"Before normalization:")
    print(f"  Min: {min_val}")
    print(f"  Max: {max_val}")
    print(f"  Mean: {mean_val:.2f}")
    print(f"  Stretch factor: {255 / (max_val - min_val):.2f}")
    
    # Normalization formula
    if max_val - min_val != 0:
        dst_float = ((src_float - min_val) * 255) / (max_val - min_val)
    else:
        dst_float = src_float
    
    # Convert back to uint8
    dst = np.clip(dst_float, 0, 255).astype(np.uint8)
    
    print(f"\nAfter normalization:")
    print(f"  Min: {np.min(dst)}")
    print(f"  Max: {np.max(dst)}")
    print(f"  Mean: {np.mean(dst):.2f}")
    
    return dst


def test_normalization():
    """
    Tests normalization on a low contrast image
    """
    # Create low contrast image
    low_contrast = create_low_contrast_image(100, 105)
    
    # Normalize
    normalized = normalize(low_contrast)
    
    # Display
    plt.figure(figsize=(12, 5))
    
    plt.subplot(1, 2, 1)
    plt.imshow(low_contrast, cmap='gray')
    plt.title('Low Contrast (100-105)')
    plt.axis('off')
    
    plt.subplot(1, 2, 2)
    plt.imshow(normalized, cmap='gray')
    plt.title('After Normalization (0-255)')
    plt.axis('off')
    
    plt.tight_layout()
    plt.show()


# ========== Question 6 ==========
def test_normalization_with_outliers():
    """
    Tests the effect of outliers on normalization
    Adds extreme values (0 and 255) to a low contrast image
    """
    # Create low contrast image
    img = create_low_contrast_image(100, 105)
    
    # Modify individual pixels to create outliers
    img[0, 0] = 0
    img[0, 1] = 255
    
    print("=== Image with outliers ===")
    normalized = normalize(img)
    
    plt.figure(figsize=(12, 5))
    
    plt.subplot(1, 2, 1)
    plt.imshow(img, cmap='gray')
    plt.title('With Outliers (0, 100-105, 255)')
    plt.axis('off')
    
    plt.subplot(1, 2, 2)
    plt.imshow(normalized, cmap='gray')
    plt.title('After Normalization')
    plt.axis('off')
    
    plt.tight_layout()
    plt.show()
    
    print("\nExplanation:")
    print("Two individual pixels (0 and 255) cause normalization to stretch the entire range.")
    print("As a result, the small differences between 100 and 105 become very small (almost invisible).")
    print("This is a known problem with normalization - sensitivity to outliers.")


# ========== Question 7 ==========
def calculate_histogram(img):
    """
    Calculates the histogram of a grayscale image
    Without using library functions
    
    Parameters:
    img: grayscale image
    
    Returns:
    histogram array with 256 elements (one for each gray level)
    """
    # Create array of 256 bins (for each gray level)
    histogram = np.zeros(256, dtype=np.int32)
    
    # Count each pixel value
    height, width = img.shape
    for y in range(height):
        for x in range(width):
            pixel_value = img[y, x]
            histogram[pixel_value] += 1
    
    return histogram


def display_histogram(img):
    """
    Displays the histogram of an image
    
    Parameters:
    img: grayscale image
    """
    # Calculate histogram
    hist = calculate_histogram(img)
    
    # Display
    plt.figure(figsize=(15, 5))
    
    plt.subplot(1, 2, 1)
    plt.imshow(img, cmap='gray')
    plt.title('Image')
    plt.axis('off')
    
    plt.subplot(1, 2, 2)
    plt.bar(range(256), hist, width=1, edgecolor='none')
    plt.title('Histogram')
    plt.xlabel('Pixel Value')
    plt.ylabel('Frequency')
    plt.xlim([0, 255])
    
    plt.tight_layout()
    plt.show()


# ========== Running all questions ==========
def main():
    print("=== Question 1: Creating gradient image ===")
    gradient = create_gradient_image(300, 400)
    plt.figure(figsize=(8, 6))
    plt.imshow(gradient, cmap='gray')
    plt.title('Gradient Image')
    plt.axis('off')
    plt.show()
    
    print("\n=== Question 3: Comparing np.add and cv2.add ===")
    test_brighten()
    
    print("\n=== Question 4: Low contrast image ===")
    low_contrast = create_low_contrast_image(100, 105)
    plt.figure(figsize=(6, 6))
    plt.imshow(low_contrast, cmap='gray')
    plt.title('Low Contrast Image (fg=100, bg=105)')
    plt.axis('off')
    plt.show()
    
    print("\n=== Question 5: Normalization ===")
    test_normalization()
    
    print("\n=== Question 6: Effect of Outliers ===")
    test_normalization_with_outliers()
    
    print("\n=== Question 7: Calculating and displaying histogram ===")
    test_img = create_gradient_image(200, 300)
    display_histogram(test_img)


if __name__ == "__main__":
    main()