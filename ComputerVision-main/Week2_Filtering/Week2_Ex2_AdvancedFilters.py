import cv2
import numpy as np
import os


class MedianBlur:
    """Median Blur filter to reduce noise while preserving edges"""
    
    def __init__(self, kernel_size=5):
        """
        Initialize Median Blur filter
        
        Args:
            kernel_size: Size of the median filter kernel (must be odd)
        """
        self.kernel_size = kernel_size
    
    def apply(self, img):
        """
        Apply Median Blur filter
        
        Args:
            img: Input image
            
        Returns:
            Filtered image
        """
        if img is None:
            return None
        
        filtered_img = cv2.medianBlur(img, self.kernel_size)
        return filtered_img


class SobelEdgeDetection:
    """Sobel Edge Detection in X direction"""
    
    def __init__(self):
        pass
    
    def apply(self, img):
        """
        Apply Sobel Edge Detection in X direction
        
        Args:
            img: Input image (preferably grayscale)
            
        Returns:
            Edge-detected image in X direction
        """
        if img is None:
            return None
        
        # Convert to grayscale if needed
        if len(img.shape) == 3:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Apply Sobel operator in X direction
        sobelx = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=3)
        sobelx = cv2.convertScaleAbs(sobelx)
        return sobelx


class LaplacianEdgeDetection:
    """Laplacian Edge Detection"""
    
    def __init__(self):
        pass
    
    def apply(self, img):
        """
        Apply Laplacian Edge Detection
        
        Args:
            img: Input image (preferably grayscale)
            
        Returns:
            Edge-detected image using Laplacian
        """
        if img is None:
            return None
        
        # Convert to grayscale if needed
        if len(img.shape) == 3:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Apply Laplacian operator
        laplacian = cv2.Laplacian(img, cv2.CV_64F)
        laplacian = cv2.convertScaleAbs(laplacian)
        return laplacian


class SharpeningFilter:
    """Sharpening Filter to enhance edges"""
    
    def __init__(self):
        # Define sharpening kernel
        self.kernel = np.array([[-1, -1, -1],
                               [-1,  9, -1],
                               [-1, -1, -1]]) / 1.0
    
    def apply(self, img):
        """
        Apply Sharpening Filter
        
        Args:
            img: Input image
            
        Returns:
            Sharpened image
        """
        if img is None:
            return None
        
        # Apply sharpening filter
        sharpened = cv2.filter2D(img, -1, self.kernel)
        return sharpened


class BilateralFilter:
    """Bilateral Filter for edge-preserving smoothing"""
    
    def __init__(self, diameter=9, sigma_color=75, sigma_space=75):
        """
        Initialize Bilateral Filter
        
        Args:
            diameter: Diameter of each pixel neighborhood
            sigma_color: Filter sigma in the color space
            sigma_space: Filter sigma in the coordinate space
        """
        self.diameter = diameter
        self.sigma_color = sigma_color
        self.sigma_space = sigma_space
    
    def apply(self, img):
        """
        Apply Bilateral Filter
        
        Args:
            img: Input image
            
        Returns:
            Filtered image
        """
        if img is None:
            return None
        
        # Apply bilateral filter
        filtered_img = cv2.bilateralFilter(img, self.diameter, self.sigma_color, self.sigma_space)
        return filtered_img


class BinaryThresholding:
    """Binary Thresholding for image binarization"""
    
    def __init__(self, threshold_value=127):
        """
        Initialize Binary Thresholding
        
        Args:
            threshold_value: Threshold value for binarization
        """
        self.threshold_value = threshold_value
    
    def apply(self, img):
        """
        Apply Binary Thresholding
        
        Args:
            img: Input image (preferably grayscale)
            
        Returns:
            Binary image (0 or 255)
        """
        if img is None:
            return None
        
        # Convert to grayscale if needed
        if len(img.shape) == 3:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Apply binary threshold
        _, binary_img = cv2.threshold(img, self.threshold_value, 255, cv2.THRESH_BINARY)
        return binary_img


class Erosion:
    """Erosion - Morphological Filtering"""
    
    def __init__(self, kernel_size=5):
        """
        Initialize Erosion
        
        Args:
            kernel_size: Size of the morphological kernel
        """
        self.kernel_size = kernel_size
        self.kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
    
    def apply(self, img):
        """
        Apply Erosion (Morphological Filtering)
        Reduces white regions and enlarges black regions
        
        Args:
            img: Input image (preferably binary)
            
        Returns:
            Eroded image
        """
        if img is None:
            return None
        
        # Apply erosion
        eroded_img = cv2.erode(img, self.kernel, iterations=1)
        return eroded_img


class Dilation:
    """Dilation - Morphological Filtering"""
    
    def __init__(self, kernel_size=5):
        """
        Initialize Dilation
        
        Args:
            kernel_size: Size of the morphological kernel
        """
        self.kernel_size = kernel_size
        self.kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
    
    def apply(self, img):
        """
        Apply Dilation (Morphological Filtering)
        Enlarges white regions and reduces black regions
        
        Args:
            img: Input image (preferably binary)
            
        Returns:
            Dilated image
        """
        if img is None:
            return None
        
        # Apply dilation
        dilated_img = cv2.dilate(img, self.kernel, iterations=1)
        return dilated_img


def main():
    """
    Demo function to apply various advanced filters to an image
    - Loads an image from CapturedImage/ folder
    - Applies all implemented filters
    - Displays results for comparison
    """
    
    # Path to captured image
    image_path = "CapturedImage/capture_001.png"
    
    # Check if a captured image exists, otherwise use a test image
    if not os.path.exists(image_path):
        print(f"No image found at {image_path}")
        # Create a simple test image with patterns
        img = np.random.randint(50, 200, (300, 300, 3), dtype=np.uint8)
        # Add some edges for edge detection
        img[50:100, 50:100] = [0, 0, 255]  # Red square
        img[150:200, 150:200] = [0, 255, 0]  # Green square
    else:
        img = cv2.imread(image_path)
    
    if img is None:
        print("Error: Could not load image")
        return
    
    print("Initializing filter classes...")
    
    # Create filter instances
    median_blur = MedianBlur(kernel_size=5)
    sobel = SobelEdgeDetection()
    laplacian = LaplacianEdgeDetection()
    sharpening = SharpeningFilter()
    bilateral = BilateralFilter()
    threshold = BinaryThresholding(threshold_value=127)
    erosion = Erosion(kernel_size=5)
    dilation = Dilation(kernel_size=5)
    
    print("Applying filters to image...")
    
    # Apply all filters
    median_blurred = median_blur.apply(img)
    sobel_x = sobel.apply(img)
    laplacian_result = laplacian.apply(img)
    sharpened = sharpening.apply(img)
    bilateral_result = bilateral.apply(img)
    binary = threshold.apply(img)
    eroded = erosion.apply(binary)
    dilated = dilation.apply(binary)
    
    print("Filters applied successfully!")
    print("Displaying results...")
    print()
    print("Windows:")
    print("  1. Original Image")
    print("  2. Median Blur")
    print("  3. Sobel Edge Detection (X)")
    print("  4. Laplacian Edge Detection")
    print("  5. Sharpening Filter")
    print("  6. Bilateral Filter")
    print("  7. Binary Threshold")
    print("  8. Erosion (Morphological)")
    print("  9. Dilation (Morphological)")
    print()
    print("Press any key to close all windows.")
    
    # Display all images
    cv2.imshow("1. Original Image", img)
    cv2.imshow("2. Median Blur", median_blurred)
    cv2.imshow("3. Sobel Edge Detection (X)", sobel_x)
    cv2.imshow("4. Laplacian Edge Detection", laplacian_result)
    cv2.imshow("5. Sharpening Filter", sharpened)
    cv2.imshow("6. Bilateral Filter", bilateral_result)
    cv2.imshow("7. Binary Threshold", binary)
    cv2.imshow("8. Erosion (Morphological)", eroded)
    cv2.imshow("9. Dilation (Morphological)", dilated)
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    print("Demo completed.")


if __name__ == "__main__":
    main()
