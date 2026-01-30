import cv2
import numpy as np

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
            Filtered image, or None if input is invalid
        """
        if img is None:
            return None

        filtered_img = cv2.GaussianBlur(img, kernel_size, sigma)
        return filtered_img
    
    def apply_bilateral_filter(self, img, diameter=9, sigma_color=75, sigma_space=75):
        """
        Apply bilateral filter (edge-preserving blur)
        
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
        
        filtered_img = cv2.bilateralFilter(img, diameter, sigma_color, sigma_space)
        return filtered_img
    
    def apply_median_filter(self, img, kernel_size=5):
        """
        Apply median filter (noise reduction)
        
        Args:
            img: Input image
            kernel_size: Size of median filter kernel (must be odd)
            
        Returns:
            Filtered image, or None if input is invalid
        """
        if img is None:
            return None
        
        filtered_img = cv2.medianBlur(img, kernel_size)
        return filtered_img
    
    def apply_morphological_opening(self, img, kernel_size=5):
        """
        Apply morphological opening (erosion followed by dilation)
        Removes small objects and noise
        
        Args:
            img: Input image
            kernel_size: Size of morphological kernel
            
        Returns:
            Filtered image, or None if input is invalid
        """
        if img is None:
            return None
        
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))
        filtered_img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
        return filtered_img
    
    def apply_morphological_closing(self, img, kernel_size=5):
        """
        Apply morphological closing (dilation followed by erosion)
        Fills small holes and gaps
        
        Args:
            img: Input image
            kernel_size: Size of morphological kernel
            
        Returns:
            Filtered image, or None if input is invalid
        """
        if img is None:
            return None
        
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))
        filtered_img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
        return filtered_img
    
    def apply_sobel_filter(self, img, ksize=3):
        """
        Apply Sobel edge detection filter
        
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
        
        # Apply Sobel in X and Y directions
        sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=ksize)
        sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=ksize)
        
        # Combine X and Y gradients
        magnitude = np.sqrt(sobelx**2 + sobely**2)
        magnitude = np.clip(magnitude, 0, 255).astype(np.uint8)
        
        return magnitude
    
    def apply_laplacian_filter(self, img):
        """
        Apply Laplacian edge detection filter
        
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
        laplacian = np.clip(np.abs(laplacian), 0, 255).astype(np.uint8)
        
        return laplacian
    
    def apply_canny_edge_detection(self, img, threshold1=100, threshold2=200):
        """
        Apply Canny edge detection
        
        Args:
            img: Input image (preferably grayscale)
            threshold1: Lower threshold for edge linking
            threshold2: Upper threshold for strong edges
            
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
        
        edges = cv2.Canny(gray, threshold1, threshold2)
        return edges
    