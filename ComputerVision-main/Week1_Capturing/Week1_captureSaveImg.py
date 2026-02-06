import cv2
import os
import numpy as np

class CaptureSaveImgProcessor:
    def __init__(self):
        pass
    
    # =============================================================================
    # STEP 1: BASIC IMAGE CAPTURE (Weeks 1-2)
    # Topic: Introduction to Computer Vision, Images as Functions & Filtering
    # =============================================================================
    def capture_and_save_image(self, bgr_img, filename):
        """
        Capture and save static image from camera
        
        Args:
            bgr_img: Input image in BGR format (numpy array)
            filename: Path to save the image
            
        Returns:
            bool: True if successful, False otherwise
        """
        # TODO: Implement image capture and saving
        # Sinh viên cần:
        # 1. Kiểm tra bgr_img có hợp lệ không
        # 2. Lưu ảnh vào thư mục CapturedImage/
        # 3. Trả về True nếu thành công, False nếu thất bại
        
        try:
            # 1. Kiểm tra ảnh đầu vào có hợp lệ không
            if bgr_img is None or not isinstance(bgr_img, np.ndarray):
                return False

            # 2. Tạo thư mục CapturedImage nếu chưa tồn tại
            save_dir = "CapturedImage"
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)

            # Ghép đường dẫn lưu ảnh
            save_path = os.path.join(save_dir, filename)

            # 3. Lưu ảnh
            success = cv2.imwrite(save_path, bgr_img)

            return success

        except Exception as e:
            print("Error saving image:", e)
            return False


def main():
    """
    Simple demo:
    - Opens the default camera
    - Shows live video
    - Press 's' to capture and save an image into CapturedImage/
    - Press 'q' to quit
    """
    # Open default camera (index 0)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Cannot open camera.")
        return

    processor = CaptureSaveImgProcessor()
    img_count = 0

    while True:
        # Read frame from camera
        ret, frame = cap.read()
        if not ret:
            print("Warning: Cannot receive frame (stream end?). Exiting...")
            break

        # Show the current frame
        cv2.imshow("Camera - Press 's' to save, 'q' to quit", frame)

        # Wait for key press (1 ms)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('s'):
            # Generate filename for captured image
            img_count += 1
            filename = f"capture_{img_count:03d}.png"

            # Use the processor to save the current frame
            if processor.capture_and_save_image(frame, filename):
                print(f"Image saved as CapturedImage/{filename}")
            else:
                print("Failed to save image.")

        elif key == ord('q'):
            # Quit the loop
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
