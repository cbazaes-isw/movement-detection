from PIL import Image
import io
import cv2
import numpy as np

def convertCvFrame2Bytes(cvFrame):
    stream = convertCvFrame2Stream(cvFrame)
    bin_img = stream.getvalue()
    return bin_img

def convertCvFrame2Stream(cvFrame):
    pil_img = Image.fromarray(cvFrame)
    stream = io.BytesIO()
    pil_img.save(stream, format='JPEG')
    return stream

def get_difference_percentage(cvFrame1, cvFrame2):
    # cvFrame1 = cv2.imread("D:\Documentos\drone\DJI MAVIC PRO\cajon_del_maipo\DJI_0002.JPG")
    # cvFrame2 = cv2.imread("D:\Documentos\drone\DJI MAVIC PRO\cajon_del_maipo\DJI_0002.JPG")
    res = cv2.absdiff(cvFrame1, cvFrame2)
    res = res.astype(np.uint8)
    percentage = (np.count_nonzero(res) * 100)/ res.size

    return percentage

