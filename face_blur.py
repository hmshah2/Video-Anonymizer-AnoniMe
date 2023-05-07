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

def process_frame(frame, face_detector, method, params, coords, confidence=0.5):
    # Loop over the detections
    for tuple in coords:
        startX, startY, endX, endY = tuple
        # Extract the face ROI and anonymize it
        face = frame[startY:endY, startX:endX]
        anonymized_face = anonymize_face(face, method, params)
        # Store the anonymized face back in the frame
        frame[startY:endY, startX:endX] = anonymized_face

    return frame

def get_face_coords(frame, face_detector, method, params, confidence=0.5):
    # Grab the dimensions of the frame and construct a blob from it
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), (104.0, 177.0, 123.0))

    # Pass the blob through the network and obtain the face detections
    face_detector.setInput(blob)
    detections = face_detector.forward()
    detections = detections[detections[:,:,:,2] > confidence]
    coords = []

    # Loop over the detectionsha
    for i in range(0, detections.shape[0]):
        # Compute the (x, y)-coordinates of the bounding box for the object
        box = detections[i, 3:7] * np.array([w, h, w, h])
        (startX, startY, endX, endY) = box.astype("int")

        # Ensure the bounding boxes fall within the dimensions of the frame
        (startX, startY) = (max(0, startX), max(0, startY))
        (endX, endY) = (min(w - 1, endX), min(h - 1, endY))
        
        coords.append((startX, startY, endX, endY))
    return coords

def process_video(input_filename, output_filename):
    # Load the face detector
    face_detector = load_face_detector()

    # Set the anonymization method and ``parameters``
    method = "pixelated"
    params = {"k": 99, "sigma": 30, "blocks": 10}


    vs = cv2.VideoCapture(input_filename)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    # Get the input video's FPS
    fps = int(vs.get(cv2.CAP_PROP_FPS))

    out_video = None

    coords = []
    while True:
        ret, frame = vs.read()
        if not ret or frame is None:
             break
        frame = imutils.resize(frame, width=400)

        # Process the frame and anonymize faces
        coords.append(get_face_coords(frame, face_detector, method, params))
        # Exit the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # Main loop to read frames and process them
    vs = cv2.VideoCapture(input_filename)
    i=0
    while True:
        ret, frame = vs.read()
        if not ret or frame is None:
             break
        frame = imutils.resize(frame, width=400)
        
        # Initialize the output video writer with the resized frame size
        if out_video is None:
            (h, w) = frame.shape[:2]
            out_video = cv2.VideoWriter(output_filename, fourcc, fps, (w, h), True)
 
        # Process the frame and anonymize faces
        all_coords = []
        for index in range(max(0, i - 5), min(len(coords) - 1, i + 5), 1):
            all_coords += coords[index]
        processed_frame = process_frame(frame, face_detector, method, params, all_coords)

        i += 1
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

def main():
    # Get the input video file from the user
    input_file = input("Enter the path to the video file: ")
    output_file = "output_video2.mp4"
    process_video(input_file, output_file)

if __name__ == "__main__":
    main()
