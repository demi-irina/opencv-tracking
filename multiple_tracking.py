import cv2
import numpy as np

video = 'video/circles.avi'

def track_line(frame):
    h, w = frame.shape[:2]
    return np.zeros((h, w, 3), np.uint8)

cap = cv2.VideoCapture(video)

hsv_min = np.array((5, 140, 150), np.uint8)
hsv_max = np.array((180, 255, 255), np.uint8)

ret, frame = cap.read()

track = track_line(frame)

a = []

while True:
    ret, frame = cap.read()
    if not ret:
         break

    blurred = cv2.medianBlur(frame, 5)
    red_circle_hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    only_red = cv2.inRange(red_circle_hsv, hsv_min, hsv_max)

    circles = cv2.HoughCircles(only_red, cv2.HOUGH_GRADIENT, 3, 800, param1=10, param2=120, minRadius=10, maxRadius=200)

    if circles is not None:
        circles = np.uint16(np.around(circles))

        for x, y, r in circles[0, :]:
            cv2.circle(frame, (x, y), r, (0, 255, 0), 3)

            if r > 0:
                if a == []:
                    a.append((x, y))
                else:
                    t = 0
                    hyp = 500
                    for i in a:
                        s = np.sqrt(((int(x)-int(i[0]))**2)+((int(y)-int(i[1]))**2))
                        if s < hyp:
                            cv2.line(track, (i[0], i[1]), (x, y), (0, 255, 0), 3)
                            a.remove(i)
                            a.append((x, y))
                            t += 1
                    if t == 0:
                         a.append((x, y))

    frame = cv2.add(frame, track)

    cv2.imshow('red_circle', frame)
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
