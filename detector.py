
import tensorflow as tf
import tensorflow_hub as hub
import cv2
import numpy as np

# Modelo MoveNet
movenet = hub.load("https://tfhub.dev/google/movenet/singlepose/lightning/4")
movenet_fn = movenet.signatures['serving_default']

def detect_pose(frame):
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (192, 192))
    img = tf.convert_to_tensor(img, dtype=tf.int32)
    img = img[tf.newaxis, ...]

    outputs = movenet_fn(img)
    keypoints = outputs['output_0'].numpy()[0, 0, :, :]

    return keypoints  

NOSE = 0
LEFT_WRIST = 9
RIGHT_WRIST = 10
LEFT_SHOULDER = 5
RIGHT_SHOULDER = 6

detector = hub.load("https://tfhub.dev/tensorflow/ssd_mobilenet_v2/2")

def detect_cell_phone(frame, debug=False):
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (320, 320))
    img = tf.convert_to_tensor(img, dtype=tf.uint8)
    img = img[tf.newaxis, ...]

    result = detector(img)

    boxes = result['detection_boxes'][0].numpy()
    classes = result['detection_classes'][0].numpy()
    scores = result['detection_scores'][0].numpy()

    h, w, _ = frame.shape
    phones = []

    PHONE_LIKE_CLASSES = {
    77,  # cell phone
    67,  # remote
    73,  # laptop (a veces confunde)
    76,  # keyboard
    84   # book
}


    for box, cls, score in zip(boxes, classes, scores):
        if score > 0.2:
            y1, x1, y2, x2 = box
            x1, x2 = int(x1*w), int(x2*w)
            y1, y2 = int(y1*h), int(y2*h)

            if debug:
                label = f"ID:{int(cls)} {score:.2f}"
                cv2.rectangle(frame, (x1,y1), (x2,y2), (255,0,0), 2)
                cv2.putText(frame, label, (x1, y1-5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 2)

            if int(cls) in PHONE_LIKE_CLASSES and score > 0.45:
                phones.append(box)

    return phones

def keypoint_to_pixel(kp, w, h):
    y, x, conf = kp
    return np.array([int(x * w), int(y * h)]), conf

def is_using_phone(frame, keypoints, phone_boxes):
    h, w, _ = frame.shape

    nose, nose_conf = keypoint_to_pixel(keypoints[NOSE], w, h)
    lw, lw_conf = keypoint_to_pixel(keypoints[LEFT_WRIST], w, h)
    rw, rw_conf = keypoint_to_pixel(keypoints[RIGHT_WRIST], w, h)

    for box in phone_boxes:
        y1, x1, y2, x2 = box
        phone_center = np.array([
            int(((x1 + x2) / 2) * w),
            int(((y1 + y2) / 2) * h)
        ])

        if lw_conf > 0.3 and np.linalg.norm(phone_center - lw) < 80:
            return True
        if rw_conf > 0.3 and np.linalg.norm(phone_center - rw) < 80:
            return True
        if nose_conf > 0.3 and np.linalg.norm(phone_center - nose) < 100:
            return True

    return False