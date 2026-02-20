import time
import cv2
import numpy as np
import pandas as pd
from time_acumulador import TimeAcumulador
from detector import detect_pose, detect_cell_phone, is_using_phone

acc = TimeAcumulador()
cap = cv2.VideoCapture("video 3.mp4")
Persona_id = 1
if not cap.isOpened():
    print("Error: No se pudo abrir camara")
    exit()

buffer_estatus = []
while True:
    ret, frame = cap.read()

    if not ret:
        break

    keypoints = detect_pose(frame)
    phones = detect_cell_phone(frame)
    using = is_using_phone(frame, keypoints, phones)
    instant_using = using(window=10)
    stable_using = instant_using.mean()

    acc.update(Persona_id, stable_using)

    cv2.imshow("Frame", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

print("Persona 1:", acc.get_total_time(1))

