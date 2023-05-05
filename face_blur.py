import cv2
import imutils
import numpy as np
from imutils.video import VideoStream

def load_face_detector():
    # Load the pre-trained OpenCV face detector model
    prototxt_path = "deploy.prototxt"
    weights_path = "res10_300x300_ssd_iter_140000.caffemodel"
    face_detector = cv2.dnn.readNet(prototxt_path, weights_path)
    return face_detector

def anonymize_face(face, method, params):
    if method == "simple":
        # Gaussian blurring
        face = cv2.GaussianBlur(face, (params['k'], params['k']), params['sigma'])
    elif method == "pixelated":
        # Pixelated blurring
        (h, w) = face.shape[:2]
        face = cv2.resize(face, (params['blocks'], params['blocks']), interpolation=cv2.INTER_LINEAR)
        face = cv2.resize(face, (w, h), interpolation=cv2.INTER_NEAREST)
    else:
        raise ValueError("Invalid anonymization method")
    return face

def process_frame(frame, face_detector, method, params, confidence=0.5):
    # Grab the dimensions of the frame and construct a blob from it
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), (104.0, 177.0, 123.0))

    # Pass the blob through the network and obtain the face detections
    face_detector.setInput(blob)
    detections = face_detector.forward()

    # Loop over the detections
    for i in range(0, detections.shape[2]):
        # Extract the confidence (i.e., probability) associated with the detection
        conf = detections[0, 0, i, 2]

        # Filter out weak detections by ensuring the confidence is greater than the minimum confidence
        if conf > confidence:
            # Compute the (x, y)-coordinates of the bounding box for the object
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            # Ensure the bounding boxes fall within the dimensions of the frame
            (startX, startY) = (max(0, startX), max(0, startY))
            (endX, endY) = (min(w - 1, endX), min(h - 1, endY))

            # Extract the face ROI and anonymize it
            face = frame[startY:endY, startX:endX]
            anonymized_face = anonymize_face(face, method, params)

            # Store the anonymized face back in the frame
            frame[startY:endY, startX:endX] = anonymized_face

    return frame

def main():
    # Load the face detector
    face_detector = load_face_detector()

    # Set the anonymization method and parameters
    method = "pixelated"
    params = {"k": 99, "sigma": 30, "blocks": 20}

    # Initialize the video stream
    vs = cv2.VideoCapture('haley.mp4')
    output_file = "output_video.mp4"
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    
    # Get the input video's FPS
    fps = int(vs.get(cv2.CAP_PROP_FPS))

    out_video = None

    # Main loop to read frames and process them
    while True:
        ret, frame = vs.read()
        if not ret or frame is None:
             break
        frame = imutils.resize(frame, width=400)
        
        # Initialize the output video writer with the resized frame size
        if out_video is None:
            (h, w) = frame.shape[:2]
            out_video = cv2.VideoWriter(output_file, fourcc, fps, (w, h), True)
 
        # Process the frame and anonymize faces
        processed_frame = process_frame(frame, face_detector, method, params)
        out_video.write(processed_frame)

        # Display the processed frame
        cv2.imshow("Anonymized Video", processed_frame)

        # Exit the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # Clean up
    vs.release()
    if out_video is not None:
        out_video.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
