import cv2
import numpy as np


class GrayscaleProcessor:
    def __init__(self):
        pass
    
    # =============================================================================
    # STEP 1: BASIC IMAGE CAPTURE (Weeks 1-2)
    # Topic: Introduction to Computer Vision, Images as Functions & Filtering
    # Assignment: Implement 10 Image Filtering Techniques
    # =============================================================================
    
    def convert_to_grayscale(self, bgr_img):
        """
        1. Grayscale Conversion
        Convert BGR image to grayscale
        
        Args:
            bgr_img: Input image in BGR format (numpy array)
            
        Returns:
            numpy array: Grayscale image, or None if input is invalid
        """
        if bgr_img is None:
            return None

        # Convert BGR to Grayscale
        gray_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2GRAY)
        return gray_img
    
    def apply_gaussian_blur(self, img, kernel_size=(5, 5), sigma=1.0):
        """
        2. Gaussian Blur
        Apply Gaussian blur filter for noise reduction
        
        Args:
            img: Input image
            kernel_size: Size of Gaussian kernel (must be odd)
            sigma: Standard deviation
            
        Returns:
            Blurred image, or None if input is invalid
        """
        if img is None:
            return None
        
        blurred = cv2.GaussianBlur(img, kernel_size, sigma)
        return blurred
    
    def apply_median_blur(self, img, kernel_size=5):
        """
        3. Median Blur
        Apply median filter for noise reduction (especially salt-and-pepper noise)
        
        Args:
            img: Input image
            kernel_size: Size of median filter kernel (must be odd)
            
        Returns:
            Blurred image, or None if input is invalid
        """
        if img is None:
            return None
        
        blurred = cv2.medianBlur(img, kernel_size)
        return blurred
    
    def apply_sobel_x_detection(self, img, ksize=3):
        """
        4. Sobel Edge Detection (X Direction)
        Apply Sobel filter in X direction for horizontal edge detection
        
        Args:
            img: Input image (preferably grayscale)
            ksize: Size of Sobel kernel
            
        Returns:
            Edge detected image, or None if input is invalid
        """
        if img is None:
            return None
        
        # Convert to grayscale if needed
        if len(img.shape) == 3:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            gray = img
        
        # Apply Sobel in X direction
        sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=ksize)
        sobelx = np.absolute(sobelx)
        sobelx = np.clip(sobelx, 0, 255).astype(np.uint8)
        
        return sobelx
    
    def apply_laplacian_detection(self, img):
        """
        5. Laplacian Edge Detection
        Apply Laplacian filter for edge detection
        
        Args:
            img: Input image (preferably grayscale)
            
        Returns:
            Edge detected image, or None if input is invalid
        """
        if img is None:
            return None
        
        # Convert to grayscale if needed
        if len(img.shape) == 3:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            gray = img
        
        laplacian = cv2.Laplacian(gray, cv2.CV_64F)
        laplacian = np.absolute(laplacian)
        laplacian = np.clip(laplacian, 0, 255).astype(np.uint8)
        
        return laplacian
    
    def apply_sharpening_filter(self, img):
        """
        6. Sharpening Filter
        Apply sharpening filter to enhance edges and details
        
        Args:
            img: Input image
            
        Returns:
            Sharpened image, or None if input is invalid
        """
        if img is None:
            return None
        
        # Define sharpening kernel
        kernel = np.array([
            [0, -1, 0],
            [-1, 5, -1],
            [0, -1, 0]
        ], dtype=np.float32)
        
        sharpened = cv2.filter2D(img, -1, kernel)
        sharpened = np.clip(sharpened, 0, 255).astype(np.uint8)
        
        return sharpened
    
    def apply_bilateral_filter(self, img, diameter=9, sigma_color=75, sigma_space=75):
        """
        7. Bilateral Filter
        Apply bilateral filter for edge-preserving smoothing
        
        Args:
            img: Input image
            diameter: Diameter of pixel neighborhood
            sigma_color: Filter sigma in the color space
            sigma_space: Filter sigma in the coordinate space
            
        Returns:
            Filtered image, or None if input is invalid
        """
        if img is None:
            return None
        
        # Convert to grayscale if needed for bilateral filter
        if len(img.shape) == 3:
            filtered = cv2.bilateralFilter(img, diameter, sigma_color, sigma_space)
        else:
            filtered = cv2.bilateralFilter(img, diameter, sigma_color, sigma_space)
        
        return filtered
    
    def apply_binary_threshold(self, img, threshold_value=127, max_value=255):
        """
        8. Thresholding (Binary)
        Apply binary thresholding to convert image to black and white
        
        Args:
            img: Input image (preferably grayscale)
            threshold_value: Threshold value
            max_value: Maximum value for pixels above threshold
            
        Returns:
            Binary image, or None if input is invalid
        """
        if img is None:
            return None
        
        # Convert to grayscale if needed
        if len(img.shape) == 3:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            gray = img
        
        _, binary = cv2.threshold(gray, threshold_value, max_value, cv2.THRESH_BINARY)
        
        return binary
    
    def apply_erosion(self, img, kernel_size=5, iterations=1):
        """
        9. Erosion (Morphological Filtering)
        Apply erosion to remove small objects and thin structures
        
        Args:
            img: Input image
            kernel_size: Size of erosion kernel
            iterations: Number of erosion iterations
            
        Returns:
            Eroded image, or None if input is invalid
        """
        if img is None:
            return None
        
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))
        eroded = cv2.erode(img, kernel, iterations=iterations)
        
        return eroded
    
    def apply_dilation(self, img, kernel_size=5, iterations=1):
        """
        10. Dilation (Morphological Filtering)
        Apply dilation to fill small holes and connect nearby objects
        
        Args:
            img: Input image
            kernel_size: Size of dilation kernel
            iterations: Number of dilation iterations
            
        Returns:
            Dilated image, or None if input is invalid
        """
        if img is None:
            return None
        
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))
        dilated = cv2.dilate(img, kernel, iterations=iterations)
        
        return dilated
    