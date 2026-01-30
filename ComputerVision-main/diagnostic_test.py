"""
Diagnostic test to verify filtering is working in the app
"""
import cv2
import numpy as np
from process import ImageProcessor

# Create a simple test image
test_img = np.zeros((480, 640, 3), dtype=np.uint8)
cv2.rectangle(test_img, (100, 100), (300, 300), (255, 0, 0), -1)
cv2.circle(test_img, (500, 200), 80, (0, 255, 0), -1)

# Initialize processor
processor = ImageProcessor()

print("=" * 60)
print("DIAGNOSTIC TEST - Verify Filtering Works")
print("=" * 60)

print("\n1. Testing process_frame() method:")
print("-" * 60)
try:
    processed, time_ms = processor.process_frame(test_img)
    print(f"✓ process_frame() executed successfully")
    print(f"  - Input shape: {test_img.shape}")
    print(f"  - Output shape: {processed.shape}")
    print(f"  - Output dtype: {processed.dtype}")
    print(f"  - Processing time: {time_ms:.2f} ms")
    
    # Check if output is grayscale
    if len(processed.shape) == 2:
        print(f"  - ✓ Output is GRAYSCALE (as expected)")
    else:
        print(f"  - ✗ WARNING: Output is not grayscale!")
    
    # Check if output is valid
    if processed is not None and processed.size > 0:
        print(f"  - ✓ Output image is valid")
        print(f"  - Min value: {processed.min()}, Max value: {processed.max()}")
    else:
        print(f"  - ✗ ERROR: Output image is invalid!")
        
except Exception as e:
    print(f"✗ ERROR in process_frame(): {e}")
    import traceback
    traceback.print_exc()

print("\n2. Testing individual filters:")
print("-" * 60)

# Convert to grayscale
gray = processor.grayscale_processor.convert_to_grayscale(test_img)
print(f"✓ Grayscale: {gray.shape}, dtype={gray.dtype}")

# Apply Gaussian
gaussian = processor.grayscale_processor.apply_gaussian_blur(gray, (5, 5), 1.0)
print(f"✓ Gaussian Blur: {gaussian.shape}, dtype={gaussian.dtype}")

# Apply edge detection
laplacian = processor.grayscale_processor.apply_laplacian_detection(gray)
print(f"✓ Laplacian: {laplacian.shape}, dtype={laplacian.dtype}")

print("\n3. Testing apply_all_filters():")
print("-" * 60)
try:
    all_results = processor.apply_all_filters(test_img)
    print(f"✓ apply_all_filters() executed successfully")
    print(f"  - Total filters applied: {len(all_results)}")
    for i, (name, img) in enumerate(all_results.items(), 1):
        print(f"    {i}. {name}: {img.shape}")
except Exception as e:
    print(f"✗ ERROR in apply_all_filters(): {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("DIAGNOSTIC TEST COMPLETED")
print("=" * 60)
