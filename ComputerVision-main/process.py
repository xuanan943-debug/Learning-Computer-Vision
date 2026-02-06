import time
import cv2
import numpy as np
import os
from Week1_Capturing.Week1_captureSaveImg import CaptureSaveImgProcessor
from Week2_Filtering.Week2_Ex1_Grayscale import GrayscaleProcessor
from Week2_Filtering.Week2_Ex1_Gaussian import GaussianProcessor
from Week2_Filtering.Week2_Ex2_AdvancedFilters import (
    MedianBlur, SobelEdgeDetection, LaplacianEdgeDetection,
    SharpeningFilter, BilateralFilter, BinaryThresholding,
    Erosion, Dilation
)


class ImageProcessor:
    """
    Class for processing images from camera feed
    Implements computer vision techniques from ProjectProgress.txt
    """
    
    def __init__(self):
        """Initialize image processor with calibration parameters"""
        self.camera_matrix = None  # Camera calibration matrix
        self.dist_coeffs = None    # Distortion coefficients
        self.homography_matrix = None  # Homography transformation matrix
        self.previous_frame = None  # For motion detection
        self.tracked_objects = []   # For object tracking
        pass
    
    
    # =============================================================================
    # STEP 10: SYSTEM INTEGRATION (Week 14)
    # Topic: All Course Concepts
    # =============================================================================
    
    def process_frame(self, bgr_img):


        if bgr_img is None:
            raise ValueError("Input frame is None")
        
        start_time = time.perf_counter()
        results = {}
        

        
        ###################### WRITE YOUR PROCESS PIPELINE HERE #########################
        saveImg = CaptureSaveImgProcessor()
        
        step1_image = saveImg.capture_and_save_image(bgr_img, "test_capture.bmp") ## Step 1: Capture and Save Image
        ######################## IMAGE FILTERING ########################################
        ## Step 2: Convert to Grayscale
        grayScaleProcessor = GrayscaleProcessor()
        processed_img = grayScaleProcessor.convert_to_grayscale(bgr_img)
        ## Save Processed Image
        step3_image = saveImg.capture_and_save_image(processed_img, "processed_capture.bmp")
        #################################################################################
        
        process_time_ms = (time.perf_counter() - start_time) * 1000
        return processed_img, results, process_time_ms
    
    def apply_filter(self, bgr_img, filter_type='grayscale'):
        """
        Apply a specific filter to the image
        
        Args:
            bgr_img: Input image in BGR format
            filter_type: Type of filter to apply
            
        Returns:
            filtered_img: Processed image
            process_time_ms: Processing time in milliseconds
        """
        
        if bgr_img is None:
            raise ValueError("Input frame is None")
        
        start_time = time.perf_counter()
        filtered_img = bgr_img.copy()
        
        try:
            if filter_type == 'none':
                filtered_img = bgr_img
            
            elif filter_type == 'grayscale':
                processor = GrayscaleProcessor()
                gray = processor.convert_to_grayscale(bgr_img)
                # Convert back to 3-channel for display
                filtered_img = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
            
            elif filter_type == 'gaussian':
                processor = GaussianProcessor()
                filtered_img = processor.apply_gaussian_filter(bgr_img, kernel_size=(5, 5), sigma=1.0)
            
            elif filter_type == 'median':
                median = MedianBlur(kernel_size=5)
                filtered_img = median.apply(bgr_img)
            
            elif filter_type == 'sobel':
                sobel = SobelEdgeDetection()
                edge_img = sobel.apply(bgr_img)
                # Convert to 3-channel
                filtered_img = cv2.cvtColor(edge_img, cv2.COLOR_GRAY2BGR)
            
            elif filter_type == 'laplacian':
                laplacian = LaplacianEdgeDetection()
                edge_img = laplacian.apply(bgr_img)
                # Convert to 3-channel
                filtered_img = cv2.cvtColor(edge_img, cv2.COLOR_GRAY2BGR)
            
            elif filter_type == 'canny':
                gray = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2GRAY)
                edges = cv2.Canny(gray, 100, 200)
                filtered_img = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
            
            elif filter_type == 'sharpening':
                sharpening = SharpeningFilter()
                filtered_img = sharpening.apply(bgr_img)
            
            elif filter_type == 'bilateral':
                bilateral = BilateralFilter(diameter=9, sigma_color=75, sigma_space=75)
                filtered_img = bilateral.apply(bgr_img)
            
            elif filter_type == 'binary_threshold':
                threshold = BinaryThresholding(threshold_value=127)
                binary_img = threshold.apply(bgr_img)
                # Convert to 3-channel
                filtered_img = cv2.cvtColor(binary_img, cv2.COLOR_GRAY2BGR)
            
            elif filter_type == 'erosion':
                gray = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2GRAY)
                _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
                erosion = Erosion(kernel_size=5)
                eroded = erosion.apply(binary)
                filtered_img = cv2.cvtColor(eroded, cv2.COLOR_GRAY2BGR)
            
            elif filter_type == 'dilation':
                gray = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2GRAY)
                _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
                dilation = Dilation(kernel_size=5)
                dilated = dilation.apply(binary)
                filtered_img = cv2.cvtColor(dilated, cv2.COLOR_GRAY2BGR)
            
            elif filter_type == 'opening':
                gray = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2GRAY)
                _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
                kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
                opened = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
                filtered_img = cv2.cvtColor(opened, cv2.COLOR_GRAY2BGR)
            
            elif filter_type == 'closing':
                gray = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2GRAY)
                _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
                kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
                closed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
                filtered_img = cv2.cvtColor(closed, cv2.COLOR_GRAY2BGR)
            
            elif filter_type == 'histogram_eq':
                gray = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2GRAY)
                equalized = cv2.equalizeHist(gray)
                filtered_img = cv2.cvtColor(equalized, cv2.COLOR_GRAY2BGR)
            
            elif filter_type == 'clahe':
                gray = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2GRAY)
                clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
                enhanced = clahe.apply(gray)
                filtered_img = cv2.cvtColor(enhanced, cv2.COLOR_GRAY2BGR)
            
            elif filter_type == 'adaptive_threshold':
                gray = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2GRAY)
                adaptive = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                                cv2.THRESH_BINARY, 11, 2)
                filtered_img = cv2.cvtColor(adaptive, cv2.COLOR_GRAY2BGR)
            
            elif filter_type == 'contour':
                gray = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2GRAY)
                _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
                contours, _ = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                filtered_img = bgr_img.copy()
                cv2.drawContours(filtered_img, contours, -1, (0, 255, 0), 2)
            
            else:
                filtered_img = bgr_img
        
        except Exception as e:
            print(f"Error applying filter {filter_type}: {str(e)}")
            filtered_img = bgr_img
        
        process_time_ms = (time.perf_counter() - start_time) * 1000
        return filtered_img, process_time_ms
    
        """
        Visualize all processing results on image
        
        Args:
            bgr_img: Original image
            results: Dictionary of results from process_frame
            
        Returns:
            Annotated image
        """

        pass