import time
import cv2
import numpy as np
import pandas as pd
from time_acumulador import TimeAcumulador
from detector import detect_pose, detect_cell_phone, is_using_phone

acc = TimeAcumulador()
cap = cv2.VideoCapture("video 4.mp4")
Persona_id = 1
if not cap.isOpened():
    print("Error: No se pudo abrir camara")
    exit()

buffer_estatus = []
stable_using = False
fps = cap.get(cv2.CAP_PROP_FPS)
while True:
    ret, frame = cap.read()

    if not ret:
        break

    keypoints = detect_pose(frame)
    phones = detect_cell_phone(frame)
    using = is_using_phone(frame, keypoints, phones)
    buffer_estatus.append(using)
    if len(buffer_estatus) > 10:
        buffer_estatus.pop(0)
    true_count = buffer_estatus.count(True)

    if true_count > len(buffer_estatus) / 2:
        stable_using = True
    elif true_count < len(buffer_estatus) / 2:
        stable_using = False
    # Precisión de tiempo    
    frame_number = cap.get(cv2.CAP_PROP_POS_FRAMES)
    timestamp = frame_number / fps
    acc.update(Persona_id, stable_using, timestamp)

    cv2.imshow("Frame", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# Mejora de reporte de tiempo    
final_timestamp = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0
acc.close_all(final_timestamp)
cap.release()
cv2.destroyAllWindows()

print("Persona 1:", acc.get_total_time(1))