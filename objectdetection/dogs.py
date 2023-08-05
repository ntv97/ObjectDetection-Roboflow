import cv2
import numpy as np

from roboflow import Roboflow
rf = Roboflow(api_key="ywxH5PqpTZEaEGpV3zTL")
project = rf.workspace().project("test-wqt3z")
model = project.version(1).model


def DetectDogs(frame):
    robodata = model.predict(frame, confidence=40, overlap=30).json()
    for data in robodata['predictions']:
    #start = (int(data['x']), int(data['y']))
        start = (int(data['x']), int(data['y']))
        color = (0, 0, 255)
        thickness = -1
        print(data)
        frame = cv2.circle(frame, start, 5, color, thickness)
        font = cv2.FONT_HERSHEY_SIMPLEX
        org = (int(data['x'])+15, int(data['y']))
        fontScale = 0.45
        frame = cv2.putText(frame, 'Dog', org, font,
                   fontScale, color, 1, cv2.LINE_AA)


    return frame

def ShowDogVideo(filename):
    cap = cv2.VideoCapture("uploads/"+filename)
    if (cap.isOpened()== False):
        print("Error opening video file")

    while True:
        ret, frame = cap.read()
        if ret == False:
            print("No (more) frames")
            break
        frame = cv2.resize(frame, (640,360))
        frame = DetectDogs(frame)
        output_frame = np.array(frame)

        ret, buffer = cv2.imencode('.jpg', output_frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
