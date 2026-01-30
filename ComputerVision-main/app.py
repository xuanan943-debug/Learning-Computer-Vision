from flask import Flask, render_template, Response, request, jsonify
import cv2
import threading
import time
import base64
import numpy as np
from process import ImageProcessor
from camera import VideoCamera
app = Flask(__name__)


# initialize processor and two camera handlers (two columns)
processor = ImageProcessor()
cameras = {
    1: VideoCamera(),
    2: VideoCamera()
}

# --- Routes ---
@app.route('/')
def index():
    return render_template('index.html')

def mjpeg_generator(cam_id):
    cam = cameras.get(cam_id)
    if cam is None:
        return
    boundary = b'--frame'
    while True:
        frame_bytes = cam.get_frame_jpeg()
        if frame_bytes:
            yield b'%s\r\nContent-Type: image/jpeg\r\nContent-Length: %d\r\n\r\n%s\r\n' % (boundary, len(frame_bytes), frame_bytes)
        else:
            # serve a small blank JPEG fallback so client doesn't break
            blank = create_blank_jpeg()
            yield b'%s\r\nContent-Type: image/jpeg\r\nContent-Length: %d\r\n\r\n%s\r\n' % (boundary, len(blank), blank)
        time.sleep(0.04)

def create_blank_jpeg():
    # create gray placeholder
    img = 128 * np.ones((240, 320, 3), dtype=np.uint8)
    ret, jpeg = cv2.imencode('.jpg', img)
    return jpeg.tobytes() if ret else b''

@app.route('/video_feed/<int:cam_id>')
def video_feed(cam_id):
    # returns multipart mjpeg stream
    return Response(mjpeg_generator(cam_id),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/set_source', methods=['POST'])
def set_source():
    # payload: { cam_id: int, source: str }
    data = request.get_json()
    cam_id = int(data.get('cam_id'))
    source = data.get('source', '').strip()
    if cam_id not in cameras:
        return jsonify({'ok': False, 'error': 'invalid cam_id'}), 400
    if source == '':
        # stop camera if empty
        cameras[cam_id].stop()
        return jsonify({'ok': True, 'msg': 'stopped'})
    try:
        cameras[cam_id].start(source)
        return jsonify({'ok': True})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500

@app.route('/capture', methods=['POST'])
def capture():
    # payload: { cam_id: int }
    data = request.get_json()
    cam_id = int(data.get('cam_id'))
    if cam_id not in cameras:
        return jsonify({'ok': False, 'error': 'invalid cam_id'}), 400
    cam = cameras[cam_id]
    frame = cam.get_frame_bgr()
    if frame is None:
        return jsonify({'ok': False, 'error': 'no frame yet'}), 400

    print(f"\n[CAPTURE] Camera {cam_id} - Original frame shape: {frame.shape}")

    # Convert BGR -> JPEG base64 for immediate display
    ret, jpg = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
    if not ret:
        return jsonify({'ok': False, 'error': 'encode_failed'}), 500
    raw = jpg.tobytes()
    b64 = base64.b64encode(raw).decode('utf-8')
    data_uri = 'data:image/jpeg;base64,' + b64
    print(f"[CAPTURE] Original image encoded: {len(data_uri)} bytes")

    # Process image with filters
    processed, process_time_ms = process_image_placeholder(frame)
    print(f"[CAPTURE] Processed frame shape: {processed.shape}, dtype: {processed.dtype}")
    print(f"[CAPTURE] Processing time: {process_time_ms:.2f} ms")

    # Encode processed image
    ret2, jpg2 = cv2.imencode('.jpg', processed, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
    if not ret2:
        print(f"[ERROR] Failed to encode processed image")
        return jsonify({'ok': False, 'error': 'encode_processed_failed'}), 500
    
    raw2 = jpg2.tobytes()
    b642 = base64.b64encode(raw2).decode('utf-8')
    processed_uri = 'data:image/jpeg;base64,' + b642
    print(f"[CAPTURE] Processed image encoded: {len(processed_uri)} bytes")
    
    response = jsonify({
        'ok': True, 
        'image': data_uri, 
        'processed': processed_uri, 
        'process_time_ms': round(process_time_ms, 2)
    })
    
    print(f"[CAPTURE] Response sent successfully\n")
    return response

def process_image_placeholder(bgr_img):
    """
    Process image using ImageProcessor filters:
    - crop center square at 50% of min(height,width)
    - convert to grayscale
    - apply gaussian blur
    """
    print("Processing image with filters...")
    try:
        processed_frame, process_time_ms = processor.process_frame(bgr_img)
        return processed_frame, process_time_ms
    except Exception as e:
        print(f"Error processing frame: {e}")
        return bgr_img, 0

@app.route('/apply_filter', methods=['POST'])
def apply_filter():
    """Apply selected filter to captured image"""
    data = request.get_json()
    cam_id = int(data.get('cam_id'))
    filter_type = data.get('filter_type', 'none')
    
    if cam_id not in cameras:
        return jsonify({'ok': False, 'error': 'invalid cam_id'}), 400
    
    # Get the captured image from the camera
    cam = cameras[cam_id]
    frame = cam.get_frame_bgr()
    
    if frame is None:
        return jsonify({'ok': False, 'error': 'no frame captured'}), 400
    
    print(f"\n[APPLY_FILTER] Camera {cam_id}, Filter: {filter_type}")
    start_time = time.perf_counter()
    
    try:
        # First, crop and resize like normal processing
        h, w = frame.shape[:2]
        side = int(min(h, w) * 0.5)
        cx, cy = w // 2, h // 2
        x0 = max(0, cx - side // 2)
        y0 = max(0, cy - side // 2)
        crop = frame[y0:y0+side, x0:x0+side].copy()
        processed = cv2.resize(crop, (256, 256))
        
        # Apply selected filter
        if filter_type == 'none':
            result = processed
        elif filter_type == 'grayscale':
            result = processor.grayscale_processor.convert_to_grayscale(processed)
        elif filter_type == 'gaussian':
            result = processor.grayscale_processor.convert_to_grayscale(processed)
            result = processor.grayscale_processor.apply_gaussian_blur(result)
        elif filter_type == 'median':
            result = processor.grayscale_processor.convert_to_grayscale(processed)
            result = processor.grayscale_processor.apply_median_blur(result)
        elif filter_type == 'sobel':
            result = processor.grayscale_processor.apply_sobel_x_detection(processed)
        elif filter_type == 'laplacian':
            result = processor.grayscale_processor.apply_laplacian_detection(processed)
        elif filter_type == 'canny':
            result = processor.gaussian_processor.apply_canny_edge_detection(processed)
        elif filter_type == 'sharpening':
            result = processor.grayscale_processor.convert_to_grayscale(processed)
            result = processor.grayscale_processor.apply_sharpening_filter(result)
        elif filter_type == 'bilateral':
            result = processor.grayscale_processor.convert_to_grayscale(processed)
            result = processor.grayscale_processor.apply_bilateral_filter(result)
        elif filter_type == 'binary_threshold':
            result = processor.grayscale_processor.apply_binary_threshold(processed)
        elif filter_type == 'erosion':
            result = processor.grayscale_processor.convert_to_grayscale(processed)
            result = processor.grayscale_processor.apply_erosion(result)
        elif filter_type == 'dilation':
            result = processor.grayscale_processor.convert_to_grayscale(processed)
            result = processor.grayscale_processor.apply_dilation(result)
        elif filter_type == 'opening':
            result = processor.grayscale_processor.convert_to_grayscale(processed)
            result = processor.morphological_processor.apply_morphological_opening(result)
        elif filter_type == 'closing':
            result = processor.grayscale_processor.convert_to_grayscale(processed)
            result = processor.morphological_processor.apply_morphological_closing(result)
        elif filter_type == 'histogram_eq':
            result = processor.enhancement_processor.apply_histogram_equalization(processed)
        elif filter_type == 'clahe':
            result = processor.enhancement_processor.apply_clahe(processed)
        elif filter_type == 'adaptive_threshold':
            result = processor.enhancement_processor.apply_adaptive_threshold(processed)
        elif filter_type == 'contour':
            # Contour detection using Canny + threshold
            gray = processor.grayscale_processor.convert_to_grayscale(processed)
            result = processor.gaussian_processor.apply_canny_edge_detection(gray, 50, 150)
        else:
            result = processed
        
        # Ensure result is valid
        if result is None:
            result = processed
        
        # Encode result
        ret, jpg = cv2.imencode('.jpg', result, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
        if not ret:
            return jsonify({'ok': False, 'error': 'encode_failed'}), 500
        
        raw = jpg.tobytes()
        b64 = base64.b64encode(raw).decode('utf-8')
        result_uri = 'data:image/jpeg;base64,' + b64
        
        process_time_ms = (time.perf_counter() - start_time) * 1000
        print(f"[APPLY_FILTER] Filter applied in {process_time_ms:.2f} ms")
        
        return jsonify({
            'ok': True,
            'result': result_uri,
            'process_time_ms': round(process_time_ms, 2)
        })
        
    except Exception as e:
        print(f"[ERROR] Filter application failed: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'ok': False, 'error': str(e)}), 500

if __name__ == '__main__':
    # debug mode off in production
    app.run(host='0.0.0.0', port=5000, threaded=True)
