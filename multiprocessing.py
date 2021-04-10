import cv2
import numpy as np
from multiprocessing import Process, Queue

video1 = 'video/red_circle.avi'
video2 = 'video/red_circle_2.avi'

def track_line(frame):
    h, w = frame.shape[:2]
    return np.zeros((h, w, 3), np.uint8)

def red_circle_video(q, video):

    cap = cv2.VideoCapture(video)
    hsv_min = np.array((5, 140, 150), np.uint8)
    hsv_max = np.array((180, 255, 255), np.uint8)

    x1 = None
    y1 = None

    ret, frame = cap.read()
    track = track_line(frame)

    while True:
        ret, frame = cap.read()
        if not ret:
             break
        blurred = cv2.medianBlur(frame, 5)
        red_circle_hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        only_red = cv2.inRange(red_circle_hsv, hsv_min, hsv_max)

        circles = cv2.HoughCircles(only_red, cv2.HOUGH_GRADIENT, 3, 1000, param1=100, param2=130, minRadius=10, maxRadius=150)
        if circles is not None:
            circles = np.uint16(np.around(circles))
            for x, y, r in circles[0, :]:
                cv2.circle(frame, (x, y), r, (0, 255, 0), 3)

                if r > 0:
                    if x1 is not None and y1 is not None:
                        cv2.line(track, (x1, y1), (x, y), (0, 255, 0), 3)
                    x1 = x
                    y1 = y
                else:
                    x1 = None
                    y1 = None

        frame = cv2.add(frame, track)

        q.put(frame)

q1 = Queue()
q2 = Queue()

p1 = Process(target = red_circle_video, args=(q1, video1))
p2 = Process(target = red_circle_video, args=(q2, video2))
p1.start()
p2.start()

cv2.namedWindow('red_circle_1', cv2.WINDOW_KEEPRATIO)
cv2.resizeWindow('red_circle_1', 1000, 1000)
cv2.moveWindow('red_circle_1', 1200,30)
cv2.namedWindow('red_circle_2', cv2.WINDOW_KEEPRATIO)
cv2.resizeWindow('red_circle_2', 1000, 1000)
cv2.moveWindow('red_circle_2', 30,30)

while True:
    try:
        a = q1.get(timeout=0.5)
        b = q2.get(timeout=0.5)
    except:
        break
    cv2.imshow('red_circle_1', a)
    cv2.imshow('red_circle_2', b)
    if cv2.waitKey(1) == ord('q'):
        break

cv2.destroyAllWindows()

p1.terminate()
p2.terminate()

