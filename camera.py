import numpy as np
import cv2 as cv

FRAMERATE = 120
VIDEO_CODEC = cv.VideoWriter_fourcc(*'MJPG')

cap = cv.VideoCapture(0)
cap.set(cv.CAP_PROP_FOURCC, VIDEO_CODEC)
# cap.set(cv.CAP_PROP_FRAME_WIDTH, 1920)
# cap.set(cv.CAP_PROP_FRAME_HEIGHT, 1080)
cap.set(cv.CAP_PROP_FPS, FRAMERATE)

# define video writer
fourcc = VIDEO_CODEC
out = cv.VideoWriter('output.avi', fourcc, FRAMERATE, (640, 480))

if not cap.isOpened():
    print("Cannot open camera")
    exit()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    # write the frame
    out.write(frame)
    
    print("Current video time", cap.get(cv.CAP_PROP_POS_MSEC))
    print("Current frame number", cap.get(cv.CAP_PROP_POS_FRAMES))
    print("Current frame width", cap.get(cv.CAP_PROP_FRAME_WIDTH))
    print("Current frame height", cap.get(cv.CAP_PROP_FRAME_HEIGHT))
    print("Current frame rate", cap.get(cv.CAP_PROP_FPS))
    
    # Display the resulting frame
    cv.imshow('frame', frame)
    if cv.waitKey(1) == ord('q'):
        break
# When everything done, release the capture
cap.release()
cv.destroyAllWindows()
