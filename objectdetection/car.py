import cv2
import numpy as np

from roboflow import Roboflow
rf = Roboflow(api_key="jq1i9HuBA1xDxaFEhTQX")
project = rf.workspace().project("cardetection-itakj")
model = project.version(1).model

def DetectCars(frame):
    robodata = model.predict(frame, confidence=40, overlap=30).json()
    for data in robodata['predictions']:
        start = (int(data['x']), int(data['y']))
        color = (0, 0, 255)
        thickness = -1
        print(data)
        frame = cv2.circle(frame, start, 5, color, thickness)
        font = cv2.FONT_HERSHEY_SIMPLEX
        org = (int(data['x'])+15, int(data['y']))
        fontScale = 0.40
        frame = cv2.putText(frame, 'Car', org, font,
                   fontScale, color, 1, cv2.LINE_AA)


    return frame

def ShowCarVideo(filename):
    cap = cv2.VideoCapture("uploads/"+filename)
    if (cap.isOpened()== False):
        print("Error opening video file")

    while True:
        ret, frame = cap.read()
        if ret == False:
            print("No (more) frames")
            break
        frame = cv2.resize(frame, (640,360))
        frame = DetectCars(frame)
        output_frame = np.array(frame)

        ret, buffer = cv2.imencode('.jpg', output_frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
