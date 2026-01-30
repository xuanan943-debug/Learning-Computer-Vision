"""
Test script to demonstrate all implemented image filters
"""
import cv2
import numpy as np
from process import ImageProcessor


def test_filters():
    """Test all implemented filters"""
    
    print("=" * 60)
    print("Image Filter Processing Test")
    print("=" * 60)
    
    # Create a simple test image (you can replace with actual camera frame)
    # Creating a test image with various patterns
    test_img = np.zeros((256, 256, 3), dtype=np.uint8)
    
    # Draw some shapes
    cv2.rectangle(test_img, (30, 30), (100, 100), (255, 0, 0), -1)  # Blue rectangle
    cv2.circle(test_img, (200, 80), 40, (0, 255, 0), -1)  # Green circle
    cv2.ellipse(test_img, (150, 200), (50, 30), 45, 0, 360, (0, 0, 255), -1)  # Red ellipse
    
    # Add some text
    cv2.putText(test_img, 'Test Image', (10, 250), cv2.FONT_HERSHEY_SIMPLEX, 
                0.7, (255, 255, 255), 2)
    
    # Initialize ImageProcessor
    processor = ImageProcessor()
    
    print("\n1. Testing Basic Grayscale Conversion")
    print("-" * 60)
    gray = processor.grayscale_processor.convert_to_grayscale(test_img)
    print(f"✓ Grayscale conversion successful")
    print(f"  Output shape: {gray.shape}")
    print(f"  Data type: {gray.dtype}")
    
    print("\n2. Testing Gaussian Filters")
    print("-" * 60)
    gaussian = processor.grayscale_processor.apply_gaussian_blur(gray)
    print(f"✓ Gaussian blur applied successfully")
    print(f"  Output shape: {gaussian.shape}")
    
    print("\n3. Testing Edge Detection")
    print("-" * 60)
    sobel = processor.grayscale_processor.apply_sobel_x_detection(gray)
    laplacian = processor.grayscale_processor.apply_laplacian_detection(gray)
    canny = processor.gaussian_processor.apply_canny_edge_detection(gray)
    print(f"✓ Sobel edge detection applied")
    print(f"✓ Laplacian edge detection applied")
    print(f"✓ Canny edge detection applied")
    
    print("\n4. Testing Morphological Operations")
    print("-" * 60)
    erosion = processor.grayscale_processor.apply_erosion(gray)
    dilation = processor.grayscale_processor.apply_dilation(gray)
    opening = processor.morphological_processor.apply_morphological_opening(gray)
    closing = processor.morphological_processor.apply_morphological_closing(gray)
    print(f"✓ Erosion applied")
    print(f"✓ Dilation applied")
    print(f"✓ Opening applied")
    print(f"✓ Closing applied")
    
    print("\n5. Testing Sharpening and Bilateral Filters")
    print("-" * 60)
    sharpened = processor.grayscale_processor.apply_sharpening_filter(gray)
    bilateral = processor.grayscale_processor.apply_bilateral_filter(gray)
    median = processor.grayscale_processor.apply_median_blur(gray)
    print(f"✓ Sharpening filter applied")
    print(f"✓ Bilateral filter applied")
    print(f"✓ Median blur applied")
    
    print("\n6. Testing Thresholding")
    print("-" * 60)
    binary = processor.grayscale_processor.apply_binary_threshold(gray, 127)
    adaptive = processor.enhancement_processor.apply_adaptive_threshold(gray)
    print(f"✓ Binary threshold applied")
    print(f"✓ Adaptive threshold applied")
    
    print("\n7. Testing Enhancement Filters")
    print("-" * 60)
    hist_eq = processor.enhancement_processor.apply_histogram_equalization(gray)
    clahe = processor.enhancement_processor.apply_clahe(gray)
    gamma = processor.enhancement_processor.apply_gamma_correction(gray, gamma=0.5)
    print(f"✓ Histogram equalization applied")
    print(f"✓ CLAHE applied")
    print(f"✓ Gamma correction applied")
    
    print("\n8. Testing Color Processing")
    print("-" * 60)
    hsv = processor.color_processor.convert_bgr_to_hsv(test_img)
    rgb = processor.color_processor.convert_bgr_to_rgb(test_img)
    lab = processor.color_processor.convert_bgr_to_lab(test_img)
    print(f"✓ BGR to HSV conversion applied")
    print(f"✓ BGR to RGB conversion applied")
    print(f"✓ BGR to LAB conversion applied")
    
    print("\n9. Testing Filter Sequences")
    print("-" * 60)
    gaussian_seq = processor.apply_filter_sequence(test_img, 'gaussian')
    edge_seq = processor.apply_filter_sequence(test_img, 'edge_detection')
    enhance_seq = processor.apply_filter_sequence(test_img, 'enhance')
    morph_seq = processor.apply_filter_sequence(test_img, 'morphological')
    print(f"✓ Gaussian filter sequence applied")
    print(f"✓ Edge detection sequence applied")
    print(f"✓ Enhancement sequence applied")
    print(f"✓ Morphological sequence applied")
    
    print("\n10. Testing apply_all_filters Method")
    print("-" * 60)
    all_filters = processor.apply_all_filters(test_img)
    print(f"✓ All filters applied successfully!")
    print(f"  Total filters applied: {len(all_filters)}")
    print(f"  Available filters:")
    for i, filter_name in enumerate(all_filters.keys(), 1):
        print(f"    {i}. {filter_name}")
    
    print("\n" + "=" * 60)
    print("ALL TESTS COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    
    return all_filters, test_img


def display_filter_results(all_filters, test_img):
    """Display filter results (optional visualization)"""
    
    print("\nCreating visualization of filter results...")
    
    # Create a grid to show all filtered images
    filter_list = list(all_filters.items())
    
    # Save a few key results
    key_filters = ['Original (Grayscale)', 'Gaussian Blur', 'Sobel X', 
                   'Laplacian', 'Binary Threshold', 'Canny Edges']
    
    print(f"\nKey filter results saved:")
    for filter_name in key_filters:
        if filter_name in all_filters:
            img = all_filters[filter_name]
            print(f"✓ {filter_name}: shape={img.shape}, dtype={img.dtype}")


if __name__ == "__main__":
    all_filters, test_img = test_filters()
    display_filter_results(all_filters, test_img)
