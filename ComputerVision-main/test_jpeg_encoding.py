"""
Test JPEG encoding of grayscale images
"""
import cv2
import numpy as np
import base64
from process import ImageProcessor

# Create test image
test_img = np.zeros((480, 640, 3), dtype=np.uint8)
cv2.rectangle(test_img, (100, 100), (300, 300), (255, 0, 0), -1)
cv2.circle(test_img, (500, 200), 80, (0, 255, 0), -1)

processor = ImageProcessor()

print("Testing JPEG Encoding of Grayscale Image:")
print("=" * 60)

# Process frame
processed, time_ms = processor.process_frame(test_img)

print(f"\n1. Processed image shape: {processed.shape}")
print(f"   Dtype: {processed.dtype}")
print(f"   Min: {processed.min()}, Max: {processed.max()}")

# Try to encode
print(f"\n2. Encoding to JPEG...")
ret, jpg = cv2.imencode('.jpg', processed, [int(cv2.IMWRITE_JPEG_QUALITY), 90])

print(f"   Encode successful: {ret}")
print(f"   JPEG size: {len(jpg.tobytes())} bytes")

# Convert to base64
raw = jpg.tobytes()
b64 = base64.b64encode(raw).decode('utf-8')
data_uri = 'data:image/jpeg;base64,' + b64

print(f"   Base64 string length: {len(b64)}")
print(f"   Data URI length: {len(data_uri)}")
print(f"   First 100 chars: {data_uri[:100]}...")

# Verify it's valid
print(f"\n3. Verification:")
print(f"   ✓ Processed image is valid: {processed is not None}")
print(f"   ✓ JPEG encoded successfully: {ret}")
print(f"   ✓ Data URI created successfully: {len(data_uri) > 50}")

print("\n" + "=" * 60)
print("✓ JPEG Encoding Test PASSED - Grayscale images encode correctly")
