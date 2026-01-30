import cv2
import numpy as np


class ImageEnhancementProcessor:
    """Image enhancement techniques for improving image quality"""
    
    def __init__(self):
        pass
    
    def apply_histogram_equalization(self, img):
        """
        Histogram Equalization
        Improves image contrast by spreading intensity values
        
        Args:
            img: Input image (preferably grayscale)
            
        Returns:
            Enhanced image, or None if input is invalid
        """
        if img is None:
            return None
        
        # Convert to grayscale if needed
        if len(img.shape) == 3:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            gray = img
        
        equalized = cv2.equalizeHist(gray)
        
        return equalized
    
    def apply_clahe(self, img, clip_limit=2.0, tile_size=(8, 8)):
        """
        CLAHE (Contrast Limited Adaptive Histogram Equalization)
        Advanced histogram equalization that prevents noise amplification
        
        Args:
            img: Input image (preferably grayscale)
            clip_limit: Contrast limit threshold
            tile_size: Size of grid cells
            
        Returns:
            Enhanced image, or None if input is invalid
        """
        if img is None:
            return None
        
        # Convert to grayscale if needed
        if len(img.shape) == 3:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            gray = img
        
        clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_size)
        enhanced = clahe.apply(gray)
        
        return enhanced
    
    def apply_brightness_contrast(self, img, brightness=0, contrast=1.0):
        """
        Adjust brightness and contrast of image
        
        Args:
            img: Input image
            brightness: Brightness adjustment (-100 to 100)
            contrast: Contrast adjustment (0.5 to 3.0)
            
        Returns:
            Adjusted image, or None if input is invalid
        """
        if img is None:
            return None
        
        adjusted = cv2.convertScaleAbs(img, alpha=contrast, beta=brightness)
        adjusted = np.clip(adjusted, 0, 255).astype(np.uint8)
        
        return adjusted
    
    def apply_gamma_correction(self, img, gamma=1.0):
        """
        Gamma Correction
        Adjusts image brightness using gamma curve
        
        Args:
            img: Input image
            gamma: Gamma value (0.5 = brighter, 2.0 = darker)
            
        Returns:
            Gamma corrected image, or None if input is invalid
        """
        if img is None:
            return None
        
        inv_gamma = 1.0 / gamma
        table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in np.arange(0, 256)]).astype(np.uint8)
        
        corrected = cv2.LUT(img, table)
        
        return corrected
    
    def apply_adaptive_threshold(self, img, block_size=11, constant=2):
        """
        Adaptive Thresholding
        Threshold value depends on the neighborhood (useful for varying lighting)
        
        Args:
            img: Input image (preferably grayscale)
            block_size: Size of neighborhood area (must be odd)
            constant: Constant subtracted from mean
            
        Returns:
            Thresholded image, or None if input is invalid
        """
        if img is None:
            return None
        
        # Convert to grayscale if needed
        if len(img.shape) == 3:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            gray = img
        
        thresholded = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                            cv2.THRESH_BINARY, block_size, constant)
        
        return thresholded
