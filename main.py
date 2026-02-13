import time
import cv2
from time_acumulador import TimeAcumulador

acc = TimeAcumulador()

cap = cv2.VideoCapture("video 3.mp4")

if not cap.isOpened():
    print("Error: No se pudo abrir el video")
    exit()

Persona_id = 1

while True:
    ret, frame = cap.read()

    if not ret:
        break

    cv2.imshow("Frame", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

#simulación
acc.update(1, True)

print("Persona 1:", acc.get_total_time(1))

