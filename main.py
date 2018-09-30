import cv2
from time import sleep
import util

video_capture = cv2.VideoCapture(0)
ret, prev_frame = video_capture.read()

while True:
    if not video_capture.isOpened():
        print('Unable to load camera.')
        sleep(5)
        pass

    # Capture frame-by-frame
    ret, frame = video_capture.read()

    perc = util.get_difference_percentage(frame, prev_frame)
    print("Porcentaje de movimiento en la captura {}%".format(perc),end='\r')

    # Display the resulting frame
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    prev_frame = frame

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
