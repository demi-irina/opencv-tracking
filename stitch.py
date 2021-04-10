import cv2
import numpy as np

video1 = 'video/red_circle.avi'
video2 = 'video/red_circle_2.avi'

cap1 = cv2.VideoCapture(video1)
cap2 = cv2.VideoCapture(video2)

ret, frame1 = cap1.read()
ret, frame2 = cap2.read()

frame2 = np.transpose(frame2, axes=(1, 0, 2))
frame = np.vstack((frame1, frame2))
scale_percent = 60
width = int(frame.shape[1] * scale_percent / 100)
height = int(frame.shape[0] * scale_percent / 100)
dsize = (width, height)
frame = cv2.resize(frame, dsize)

fourcc = cv2.VideoWriter_fourcc(*'MP42')
out = cv2.VideoWriter('circles.avi', fourcc, 20.0, dsize)

while cap1.isOpened() and cap2.isOpened():

    ret, frame1 = cap1.read()
    ret, frame2 = cap2.read()

    if ret:

        frame2 = np.transpose(frame2, axes=(1, 0, 2))
        frame = np.vstack((frame1, frame2))
        frame = cv2.resize(frame, dsize)

        out.write(frame)
        cv2.imshow('Video', frame)
        if cv2.waitKey(1) == ord('q'):
            break
    else:
        break

cap1.release()
cap2.release()
out.release()
cv2.destroyAllWindows()