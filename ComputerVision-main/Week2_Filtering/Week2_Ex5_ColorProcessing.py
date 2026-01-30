import cv2
import numpy as np


class ColorProcessingProcessor:
    """Color space conversions and color-based processing"""
    
    def __init__(self):
        pass
    
    def convert_bgr_to_hsv(self, bgr_img):
        """
        Convert BGR image to HSV color space
        Useful for color-based segmentation and detection
        
        Args:
            bgr_img: Input image in BGR format
            
        Returns:
            HSV image, or None if input is invalid
        """
        if bgr_img is None:
            return None
        
        hsv_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2HSV)
        
        return hsv_img
    
    def convert_bgr_to_rgb(self, bgr_img):
        """
        Convert BGR image to RGB color space
        
        Args:
            bgr_img: Input image in BGR format
            
        Returns:
            RGB image, or None if input is invalid
        """
        if bgr_img is None:
            return None
        
        rgb_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2RGB)
        
        return rgb_img
    
    def convert_bgr_to_lab(self, bgr_img):
        """
        Convert BGR image to LAB color space
        LAB is more perceptually uniform for color analysis
        
        Args:
            bgr_img: Input image in BGR format
            
        Returns:
            LAB image, or None if input is invalid
        """
        if bgr_img is None:
            return None
        
        lab_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2LAB)
        
        return lab_img
    
    def extract_color_channel(self, img, channel=0):
        """
        Extract a single color channel from image
        
        Args:
            img: Input image (BGR format)
            channel: Channel index (0=Blue, 1=Green, 2=Red)
            
        Returns:
            Single channel image, or None if input is invalid
        """
        if img is None:
            return None
        
        if len(img.shape) != 3:
            return None
        
        channel_img = img[:, :, channel]
        
        return channel_img
    
    def apply_color_range_mask(self, bgr_img, lower_bgr, upper_bgr):
        """
        Create mask based on color range in BGR space
        
        Args:
            bgr_img: Input image in BGR format
            lower_bgr: Lower bound [B, G, R]
            upper_bgr: Upper bound [B, G, R]
            
        Returns:
            Binary mask, or None if input is invalid
        """
        if bgr_img is None:
            return None
        
        lower = np.array(lower_bgr, dtype=np.uint8)
        upper = np.array(upper_bgr, dtype=np.uint8)
        
        mask = cv2.inRange(bgr_img, lower, upper)
        
        return mask
    
    def apply_color_range_mask_hsv(self, bgr_img, lower_hsv, upper_hsv):
        """
        Create mask based on color range in HSV space
        More intuitive for color-based detection
        
        Args:
            bgr_img: Input image in BGR format
            lower_hsv: Lower bound [H, S, V]
            upper_hsv: Upper bound [H, S, V]
            
        Returns:
            Binary mask, or None if input is invalid
        """
        if bgr_img is None:
            return None
        
        hsv_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2HSV)
        
        lower = np.array(lower_hsv, dtype=np.uint8)
        upper = np.array(upper_hsv, dtype=np.uint8)
        
        mask = cv2.inRange(hsv_img, lower, upper)
        
        return mask
