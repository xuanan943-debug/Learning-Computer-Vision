#!/usr/bin/env python3
"""
Final Verification Script - Confirms all filters are working
Run this to verify the complete image processing pipeline
"""

import cv2
import numpy as np
from process import ImageProcessor

def create_test_image():
    """Create a diverse test image"""
    img = np.zeros((480, 640, 3), dtype=np.uint8)
    
    # Add various colored shapes
    cv2.rectangle(img, (50, 50), (200, 200), (255, 0, 0), -1)  # Blue
    cv2.circle(img, (500, 100), 60, (0, 255, 0), -1)          # Green
    cv2.ellipse(img, (300, 400), (100, 50), 45, 0, 360, (0, 0, 255), -1)  # Red
    
    # Add text
    cv2.putText(img, 'Test', (20, 250), cv2.FONT_HERSHEY_SIMPLEX, 
                1, (255, 255, 255), 2)
    
    # Add noise
    noise = np.random.randint(0, 50, img.shape, dtype=np.uint8)
    img = cv2.add(img, noise)
    
    return img

def main():
    print("\n" + "="*70)
    print("FINAL VERIFICATION - IMAGE FILTERING PIPELINE".center(70))
    print("="*70)
    
    # Create test image
    test_img = create_test_image()
    processor = ImageProcessor()
    
    print("\n[1] INPUT IMAGE")
    print("-" * 70)
    print(f"    Shape: {test_img.shape}")
    print(f"    Type: {test_img.dtype}")
    print(f"    Format: BGR (3 channels)")
    
    print("\n[2] PROCESSING PIPELINE")
    print("-" * 70)
    
    # Step 1: Process frame
    try:
        processed, time_ms = processor.process_frame(test_img)
        print(f"    ✓ process_frame() executed")
        print(f"      - Output shape: {processed.shape}")
        print(f"      - Output type: {processed.dtype}")
        print(f"      - Processing time: {time_ms:.2f} ms")
        print(f"      - Is Grayscale: {len(processed.shape) == 2}")
    except Exception as e:
        print(f"    ✗ ERROR in process_frame(): {e}")
        return False
    
    print("\n[3] INDIVIDUAL FILTERS TEST")
    print("-" * 70)
    
    filters_tested = 0
    filters_passed = 0
    
    # Test all filters
    test_cases = [
        ("Grayscale", lambda: processor.grayscale_processor.convert_to_grayscale(test_img)),
        ("Gaussian Blur", lambda: processor.grayscale_processor.apply_gaussian_blur(processed)),
        ("Median Blur", lambda: processor.grayscale_processor.apply_median_blur(processed)),
        ("Sobel X", lambda: processor.grayscale_processor.apply_sobel_x_detection(processed)),
        ("Laplacian", lambda: processor.grayscale_processor.apply_laplacian_detection(processed)),
        ("Sharpening", lambda: processor.grayscale_processor.apply_sharpening_filter(processed)),
        ("Bilateral", lambda: processor.grayscale_processor.apply_bilateral_filter(processed)),
        ("Binary Threshold", lambda: processor.grayscale_processor.apply_binary_threshold(processed)),
        ("Erosion", lambda: processor.grayscale_processor.apply_erosion(processed)),
        ("Dilation", lambda: processor.grayscale_processor.apply_dilation(processed)),
        ("Canny Edges", lambda: processor.gaussian_processor.apply_canny_edge_detection(processed)),
        ("Opening", lambda: processor.morphological_processor.apply_morphological_opening(processed)),
        ("Closing", lambda: processor.morphological_processor.apply_morphological_closing(processed)),
        ("Histogram Eq", lambda: processor.enhancement_processor.apply_histogram_equalization(processed)),
        ("CLAHE", lambda: processor.enhancement_processor.apply_clahe(processed)),
        ("Adaptive Threshold", lambda: processor.enhancement_processor.apply_adaptive_threshold(processed)),
    ]
    
    for filter_name, filter_func in test_cases:
        filters_tested += 1
        try:
            result = filter_func()
            if result is not None and result.size > 0:
                filters_passed += 1
                print(f"    ✓ {filter_name:25} {str(result.shape):15} {result.dtype}")
            else:
                print(f"    ✗ {filter_name:25} INVALID OUTPUT")
        except Exception as e:
            print(f"    ✗ {filter_name:25} ERROR: {str(e)[:40]}")
    
    print("\n[4] APPLY ALL FILTERS TEST")
    print("-" * 70)
    try:
        all_results = processor.apply_all_filters(test_img)
        print(f"    ✓ apply_all_filters() executed successfully")
        print(f"    ✓ {len(all_results)} filters applied")
        for i, (name, img) in enumerate(all_results.items(), 1):
            print(f"       {i:2}. {name:25} {str(img.shape):15}")
    except Exception as e:
        print(f"    ✗ ERROR in apply_all_filters(): {e}")
    
    print("\n[5] FILTER SEQUENCES TEST")
    print("-" * 70)
    sequences = ['gaussian', 'edge_detection', 'enhance', 'morphological']
    for seq in sequences:
        try:
            result = processor.apply_filter_sequence(test_img, seq)
            if result is not None:
                print(f"    ✓ {seq:20} {str(result.shape):15} SUCCESS")
            else:
                print(f"    ✗ {seq:20} {str(result.shape):15} FAILED")
        except Exception as e:
            print(f"    ✗ {seq:20} ERROR: {str(e)[:40]}")
    
    print("\n[6] SUMMARY")
    print("-" * 70)
    print(f"    Total Filters Tested: {filters_tested}")
    print(f"    Filters Passed: {filters_passed}")
    print(f"    Pass Rate: {(filters_passed/filters_tested)*100:.1f}%")
    
    if filters_passed == filters_tested:
        print(f"\n    ✅ ALL TESTS PASSED - FILTERING PIPELINE IS OPERATIONAL")
    else:
        print(f"\n    ⚠️  Some tests failed - Review errors above")
    
    print("\n" + "="*70)
    print("VERIFICATION COMPLETE".center(70))
    print("="*70 + "\n")
    
    return filters_passed == filters_tested

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
