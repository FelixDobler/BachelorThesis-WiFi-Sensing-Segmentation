import subprocess
from time import sleep
import cv2 as cv
from numpy import std

# read file /home/felix/Documents/uni/BaProj/bachelorproject/record/recordings/2024-09-03T17-59-57+02-00.avi and display the nth frame

path = "/home/felix/Documents/uni/BaProj/bachelorproject/record/recordings/2024-09-03T17-59-57+02-00.avi"
# path = "/home/felix/Documents/uni/BaProj/bachelorproject/record/recordings/2024-09-03T18-52-52+02-00.mp4"

cap = cv.VideoCapture(path)
if not cap.isOpened():
    print("Error opening video stream or file")
    
print(f"Frame count: {cap.get(cv.CAP_PROP_FRAME_COUNT)}")

ffprobe_n_frames = subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-show_entries", "stream=nb_read_frames", "-of", "csv=p=0", path], stdout=subprocess.PIPE)
output = ffprobe_n_frames.stdout.decode("utf-8")

print(f"ffprobe frame count: {output}")
n_frames = int(output)

for i in range(n_frames):
    frame_n = n_frames - i - 1
    print(f"Frame {frame_n}")
    cap.set(cv.CAP_PROP_POS_FRAMES, frame_n)
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    cv.imshow(f"Frame", frame)
    cv.waitKey(1)

cap.release()
