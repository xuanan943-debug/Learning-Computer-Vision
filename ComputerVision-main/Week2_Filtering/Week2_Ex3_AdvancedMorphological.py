import cv2
import numpy as np


class AdvancedMorphologicalProcessor:
    """Advanced morphological operations for image processing"""
    
    def __init__(self):
        pass
    
    def apply_morphological_opening(self, img, kernel_size=5):
        """
        Morphological Opening: Erosion followed by Dilation
        Removes small objects and noise while preserving larger structures
        
        Args:
            img: Input image
            kernel_size: Size of morphological kernel
            
        Returns:
            Opened image, or None if input is invalid
        """
        if img is None:
            return None
        
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))
        opened = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
        
        return opened
    
    def apply_morphological_closing(self, img, kernel_size=5):
        """
        Morphological Closing: Dilation followed by Erosion
        Fills small holes and gaps in objects
        
        Args:
            img: Input image
            kernel_size: Size of morphological kernel
            
        Returns:
            Closed image, or None if input is invalid
        """
        if img is None:
            return None
        
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))
        closed = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
        
        return closed
    
    def apply_morphological_gradient(self, img, kernel_size=5):
        """
        Morphological Gradient: Dilation - Erosion
        Highlights object boundaries and edges
        
        Args:
            img: Input image
            kernel_size: Size of morphological kernel
            
        Returns:
            Gradient image, or None if input is invalid
        """
        if img is None:
            return None
        
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))
        gradient = cv2.morphologyEx(img, cv2.MORPH_GRADIENT, kernel)
        
        return gradient
    
    def apply_top_hat_transform(self, img, kernel_size=5):
        """
        Top Hat Transform: Original - Opening
        Extracts small elements and details from images
        
        Args:
            img: Input image
            kernel_size: Size of morphological kernel
            
        Returns:
            Top hat transformed image, or None if input is invalid
        """
        if img is None:
            return None
        
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))
        tophat = cv2.morphologyEx(img, cv2.MORPH_TOPHAT, kernel)
        
        return tophat
    
    def apply_black_hat_transform(self, img, kernel_size=5):
        """
        Black Hat Transform: Closing - Original
        Extracts small holes and dark details
        
        Args:
            img: Input image
            kernel_size: Size of morphological kernel
            
        Returns:
            Black hat transformed image, or None if input is invalid
        """
        if img is None:
            return None
        
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))
        blackhat = cv2.morphologyEx(img, cv2.MORPH_BLACKHAT, kernel)
        
        return blackhat
