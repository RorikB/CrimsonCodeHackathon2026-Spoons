import cv2  
import mediapipe as mp  
import os  

# Initialize MediaPipe face detection module
mp_face_detection = mp.tasks.vision

# Construct the path to the face detection model file
base_path = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(base_path, 'models', 'blaze_face_short_range.tflite')

# Configure the base options with the model path
base_options = mp.tasks.BaseOptions(model_asset_path=model_path)

options = mp_face_detection.FaceDetectorOptions(
    base_options=base_options,
    running_mode=mp.tasks.vision.RunningMode.VIDEO,
    min_detection_confidence=0.7,
)

# Create the face detector instance
detector = mp_face_detection.FaceDetector.create_from_options(options)
cap = cv2.VideoCapture(0)
frame_timestamp_ms = 0  # Timestamp tracker for video processing
face_detected = False
# Main video processing loop
# while cap.isOpened():
#     detect, frame = cap.read()
#     if not detect:
#         break 
# 
#     #BGR to RGB
#     rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
# 
#     # Create MediaPipe Image object
#     mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
#     
#     # Detect faces in the video frame with timestamp
#     detection_result = detector.detect_for_video(mp_image, frame_timestamp_ms)
#     
#     # Increment timestamp by ~33ms (approximately 30 FPS)
#     frame_timestamp_ms += 33
# 
#     # Draw bounding boxes around detected faces
#     for detection in detection_result.detections:
#         bbox = detection.bounding_box
#         cv2.rectangle(
#             frame,
#             (bbox.origin_x, bbox.origin_y),
#             (bbox.origin_x + bbox.width, bbox.origin_y + bbox.height),
#             (0, 255, 0), 
#             2  
#         )
#     cv2.imshow("Face Detection", frame)
# 
#     if cv2.waitKey(1) & 0xFF == ord("q"):
#         break

# cap.release()  # Release the camera
# cv2.destroyAllWindows()  # Close all OpenCV windows

def check_for_face():
    return check_for_faces(cap)

def check_for_faces(cap):
    global frame_timestamp_ms
    global face_detected
    if cap.isOpened():
        
        ret, frame = cap.read()  # Unpack the tuple
        if ret and frame is not None:
            #BGR to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Create MediaPipe Image object
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
            
            # Detect faces in the video frame with timestamp
            detection_result = detector.detect_for_video(mp_image, frame_timestamp_ms)
            
            # Increment timestamp by ~33ms (approximately 30 FPS)
            frame_timestamp_ms += 33
            
            if detection_result.detections:
                face_detected = True
            else:
                face_detected = False

            # Draw bounding boxes around detected faces
            for detection in detection_result.detections:
                bbox = detection.bounding_box
                cv2.rectangle(
                    frame,
                    (bbox.origin_x, bbox.origin_y),
                    (bbox.origin_x + bbox.width, bbox.origin_y + bbox.height),
                    (0, 255, 0), 
                    2  
                )
            cv2.imshow("Face Detection", frame)
            

        if cv2.waitKey(1) & 0xFF == ord("q"):
            cap.release()  # Release the camera
            cv2.destroyAllWindows()
        return face_detected

