from Week1_Capturing.Week1_captureSaveImg import CaptureSaveImgProcessor
from Week2_Filtering.Week2_Ex1_Grayscale import GrayscaleProcessor
from Week2_Filtering.Week2_Ex2_Gausian import GaussianProcessor
from Week2_Filtering.Week2_Ex3_AdvancedMorphological import AdvancedMorphologicalProcessor
from Week2_Filtering.Week2_Ex4_Enhancement import ImageEnhancementProcessor
from Week2_Filtering.Week2_Ex5_ColorProcessing import ColorProcessingProcessor
import time
import cv2
import numpy as np


class ImageProcessor:
    """
    Class for processing images from camera feed
    """
    frame = None  # BGR numpy array
    def __init__(self, frame=None):
        """Initialize image processor"""
        self.frame = frame
        self.grayscale_processor = GrayscaleProcessor()
        self.gaussian_processor = GaussianProcessor()
        self.morphological_processor = AdvancedMorphologicalProcessor()
        self.enhancement_processor = ImageEnhancementProcessor()
        self.color_processor = ColorProcessingProcessor()
    
    def process_frame(self, bgr_img):
        """
        Process a single frame
        
        Args:
            bgr_img: Input image in BGR format (numpy array)
            
        Returns:
            tuple: (Processed image, process time in ms)
        """
        if bgr_img is None:
            raise ValueError("Input frame is None")

        start_time = time.perf_counter()

        h, w = bgr_img.shape[:2]
        side = int(min(h, w) * 0.5)
        cx, cy = w // 2, h // 2
        x0 = max(0, cx - side // 2)
        y0 = max(0, cy - side // 2)
        crop = bgr_img[y0:y0+side, x0:x0+side].copy()

        processed = cv2.resize(crop, (256, 256))
        
        # Convert to grayscale
        processed = self.grayscale_processor.convert_to_grayscale(processed)
        
        # Apply Gaussian filter to reduce noise
        processed = self.gaussian_processor.apply_gaussian_filter(processed, kernel_size=(5, 5), sigma=1.0)

        process_time_ms = (time.perf_counter() - start_time) * 1000

        return processed, process_time_ms
    def preprocess(self, bgr_img):
        """
        Preprocess image (e.g., resize, normalize)
        
        Args:
            bgr_img: Input image in BGR format
            
        Returns:
            Preprocessed image
        """
        if bgr_img is None:
            return None
        
        # Normalize image to 0-1 range
        preprocessed = bgr_img.astype(np.float32) / 255.0
        
        return preprocessed
    
    def postprocess(self, result):
        """
        Postprocess results
        
        Args:
            result: Processed result
            
        Returns:
            Postprocessed result (denormalized)
        """
        if result is None:
            return None
        
        # Denormalize result back to 0-255 range if it's in float format
        if result.dtype == np.float32 or result.dtype == np.float64:
            postprocessed = np.clip(result * 255.0, 0, 255).astype(np.uint8)
        else:
            postprocessed = result
        
        return postprocessed    
    def apply_all_filters(self, bgr_img):
        """
        Apply all implemented filters to image for demonstration
        
        Args:
            bgr_img: Input image in BGR format
            
        Returns:
            Dictionary of filtered images with filter names as keys
        """
        if bgr_img is None:
            return None
        
        results = {}
        
        # Convert to grayscale
        gray = self.grayscale_processor.convert_to_grayscale(bgr_img)
        results['Original (Grayscale)'] = gray
        
        # Basic Filters (from Week2_Ex1_Grayscale)
        results['Gaussian Blur'] = self.grayscale_processor.apply_gaussian_blur(gray)
        results['Median Blur'] = self.grayscale_processor.apply_median_blur(gray)
        results['Sobel X'] = self.grayscale_processor.apply_sobel_x_detection(gray)
        results['Laplacian'] = self.grayscale_processor.apply_laplacian_detection(gray)
        results['Sharpening'] = self.grayscale_processor.apply_sharpening_filter(gray)
        results['Bilateral'] = self.grayscale_processor.apply_bilateral_filter(gray)
        results['Binary Threshold'] = self.grayscale_processor.apply_binary_threshold(gray)
        results['Erosion'] = self.grayscale_processor.apply_erosion(gray)
        results['Dilation'] = self.grayscale_processor.apply_dilation(gray)
        
        # Advanced Gaussian Filters (from Week2_Ex2_Gausian)
        results['Canny Edges'] = self.gaussian_processor.apply_canny_edge_detection(gray)
        
        # Advanced Morphological Filters (from Week2_Ex3_AdvancedMorphological)
        results['Opening'] = self.morphological_processor.apply_morphological_opening(gray)
        results['Closing'] = self.morphological_processor.apply_morphological_closing(gray)
        results['Gradient'] = self.morphological_processor.apply_morphological_gradient(gray)
        
        # Enhancement Filters (from Week2_Ex4_Enhancement)
        results['Histogram Eq'] = self.enhancement_processor.apply_histogram_equalization(gray)
        results['CLAHE'] = self.enhancement_processor.apply_clahe(gray)
        results['Adaptive Threshold'] = self.enhancement_processor.apply_adaptive_threshold(gray)
        
        # Color Processing (from Week2_Ex5_ColorProcessing)
        results['HSV'] = self.color_processor.convert_bgr_to_hsv(bgr_img)
        
        return results
    
    def apply_filter_sequence(self, bgr_img, filter_name='gaussian'):
        """
        Apply a specific filter sequence to image
        
        Args:
            bgr_img: Input image in BGR format
            filter_name: Name of filter sequence to apply
            
        Returns:
            Filtered image
        """
        if bgr_img is None:
            return None
        
        # Convert to grayscale first
        gray = self.grayscale_processor.convert_to_grayscale(bgr_img)
        
        if filter_name == 'gaussian':
            # Gaussian blur sequence
            result = self.grayscale_processor.apply_gaussian_blur(gray, (5, 5), 1.0)
            
        elif filter_name == 'edge_detection':
            # Edge detection sequence
            result = self.grayscale_processor.apply_gaussian_blur(gray, (3, 3), 0.5)
            result = self.grayscale_processor.apply_laplacian_detection(result)
            
        elif filter_name == 'enhance':
            # Enhancement sequence
            result = self.enhancement_processor.apply_histogram_equalization(gray)
            result = self.grayscale_processor.apply_bilateral_filter(result)
            
        elif filter_name == 'morphological':
            # Morphological sequence
            result = self.grayscale_processor.apply_gaussian_blur(gray, (5, 5), 1.0)
            result = self.grayscale_processor.apply_binary_threshold(result, 127)
            result = self.morphological_processor.apply_morphological_closing(result)
            
        else:
            result = gray
        
        return result