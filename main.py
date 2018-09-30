import cv2
from time import sleep
import util
import numpy as np
from datetime import datetime
import collections

text_format_stdev = "Desviacion estandar {}"
percentages = collections.deque(maxlen=10)
TOLERANCIA_MOVIMIENTO = 0.13

video_capture = cv2.VideoCapture(0)
frameWidth = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
frameHeight = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
ret, prev_frame = video_capture.read()

while True:
    if not video_capture.isOpened():
        print('Unable to load camera.')
        sleep(5)
        pass

    # Capture frame-by-frame
    ret, frame = video_capture.read()

    perc = util.get_difference_percentage(frame, prev_frame)
    percentages.append(perc)
    stdev = np.std(percentages)

    if (stdev >= TOLERANCIA_MOVIMIENTO):
        cv2.circle(
            frame,
            center=(int(frameWidth / 15), int(frameHeight / 15)),
            radius=10,
            thickness=-1,
            color=(0, 0, 255)
        )

    img_text_stdev = text_format_stdev.format(stdev)
    cv2.putText(
        img=frame,
        text=img_text_stdev,
        org=(10, int(frameHeight - 10)),
        fontFace=cv2.FONT_HERSHEY_PLAIN,
        fontScale=1,
        color=(0, 255, 0)
    )
    cv2.putText(
        img=frame,
        text=str(datetime.now()),
        org=(int(frameWidth / 5) * 3, int(frameHeight - 10)),
        fontFace=cv2.FONT_HERSHEY_PLAIN,
        fontScale=1,
        color=(0, 255, 0)
    )

    # Display the resulting frame
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    prev_frame = frame

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
