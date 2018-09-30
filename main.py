import cv2
from time import sleep
import util
import numpy as np
from datetime import datetime
import collections

# Formato de texto para mostrar en cada cuadro la
# desviación estándar de cambio entre cuadros.
text_format_stdev = "Desviacion estandar {}"

# Lista de largo fijo para calcular la desviación estándar
# en función del porcentaje de cambio de los últimos cuadros
# procesados.
percentages = collections.deque(maxlen=10)

# Máxima desviación estándar tolerable, luego de la cual
# se considera que los cuadros tienen movimiento.
TOLERANCIA_MOVIMIENTO = 0.13

# Se establece comunicación con la cámara
# se obtiene el alto y ancho de cada cuadro
# y se captura el primer cuadro.
video_capture = cv2.VideoCapture(0)
frameWidth = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
frameHeight = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
ret, prev_frame = video_capture.read()

while True:
    if not video_capture.isOpened():
        print('Unable to load camera.')
        sleep(5)
        pass

    # Captura un cuadro
    ret, frame = video_capture.read()

    # Se determina el porcentaje de diferencia entre el cuadro actual
    # y el capturado en la iteración anterior. Además se determina
    # la desviación estándar en función de la cual se determinará
    # si hay movimiento entre cuadro y cuadro.
    perc = util.get_difference_percentage(frame, prev_frame)
    percentages.append(perc)
    stdev = np.std(percentages)

    # Si la desviación estándar de cambio entre cuadros es mayor
    # o igual al factor de tolerancia se dibuja un círculo rojo
    # en el cuadro actual.
    if (stdev >= TOLERANCIA_MOVIMIENTO):
        cv2.circle(
            frame,
            center=(int(frameWidth / 15), int(frameHeight / 15)),
            radius=10,
            thickness=-1,
            color=(0, 0, 255)
        )

    # Escribo la desviación estándar de cambio entre cuadros y
    # la fecha/hora de captura
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

    # Se muestra el frame resultante
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Capturo el frame actual para compararlo con el
    # frame capturado en la siguiente iteración
    prev_frame = frame

# Cuando todo ha finalizado, libero la cámara
video_capture.release()
cv2.destroyAllWindows()
