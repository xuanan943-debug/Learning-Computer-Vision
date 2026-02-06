import cv2
import os

class GaussianProcessor:
    def __init__(self):
        pass
    
    # =============================================================================
    # STEP 1: BASIC IMAGE CAPTURE (Weeks 1-2)
    # Topic: Introduction to Computer Vision, Images as Functions & Filtering
    # =============================================================================
    
    def apply_gaussian_filter(self, img, kernel_size=(5, 5), sigma=1.0):
        """
        Apply Gaussian filtering to reduce noise
        
        Args:
            img: Input image
            kernel_size: Size of Gaussian kernel (must be odd)
            sigma: Standard deviation
            
        Returns:
            Filtered image
        """
        # TODO: Implement Gaussian filtering
        # Hint: Use cv2.GaussianBlur

        if img is None:
            return None

        filtered_img = cv2.GaussianBlur(img, kernel_size, sigma)
        return filtered_img


def main():
    """
    Demo function to apply Gaussian filter to an image
    - Loads an image from CapturedImage/ folder
    - Applies Gaussian filter with different kernel sizes
    - Displays original and filtered images side by side
    """
    
    # Path to captured image
    image_path = "CapturedImage/capture_001.png"
    
    # Check if a captured image exists, otherwise use a test image
    if not os.path.exists(image_path):
        print(f"No image found at {image_path}")
        # Create a simple test image
        import numpy as np
        img = np.random.randint(0, 256, (300, 300, 3), dtype=np.uint8)
    else:
        img = cv2.imread(image_path)
    
    if img is None:
        print("Error: Could not load image")
        return
    
    # Create processor instance
    processor = GaussianProcessor()
    
    # Apply Gaussian filter with different kernel sizes
    filtered_img_small = processor.apply_gaussian_filter(img, kernel_size=(3, 3), sigma=0.5)
    filtered_img_medium = processor.apply_gaussian_filter(img, kernel_size=(5, 5), sigma=1.0)
    filtered_img_large = processor.apply_gaussian_filter(img, kernel_size=(11, 11), sigma=2.0)
    
    # Display results
    cv2.imshow("Original Image", img)
    cv2.imshow("Gaussian Filter (3x3)", filtered_img_small)
    cv2.imshow("Gaussian Filter (5x5)", filtered_img_medium)
    cv2.imshow("Gaussian Filter (11x11)", filtered_img_large)
    
    print("Displaying original and Gaussian filtered images.")
    print("Press any key to close the windows.")
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
