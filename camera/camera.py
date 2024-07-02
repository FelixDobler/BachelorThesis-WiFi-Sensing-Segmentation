import cv2 as cv
from datetime import datetime, timezone
from typing import Tuple
from getkey import getkey, keys

class VideoManager:
    
    def capSetAndCheck(self, prop, target_value):
        self.cap.set(prop, target_value)
        real_value = self.cap.get(prop)
        if real_value != target_value:
            raise Exception(f"Failed to set {prop} to {target_value}: got {real_value} instead")
        return target_value
    


    def __init__(self, codec: str | Tuple[str, str], resolution: Tuple[int, int], framerate: int) -> None:
        self.isRecording = False

        # set codecs
        if isinstance(codec, str):
            self.capture_codec = self.store_codec = codec
        else:
            # set capture and store codecs respectively
            self.capture_codec, self.store_codec = codec
        
        self.targetCapConfig = {
            cv.CAP_PROP_FOURCC: cv.VideoWriter.fourcc(*self.capture_codec),
            cv.CAP_PROP_FRAME_WIDTH: resolution[0],
            cv.CAP_PROP_FRAME_HEIGHT: resolution[1],
            cv.CAP_PROP_FPS: framerate
        }

        self.cap = cv.VideoCapture(0)
        if not self.cap.isOpened():
            raise Exception("Cannot open camera")

        for prop, value in self.targetCapConfig.items():
            self.cap.set(prop, value)
        
        # read a single frame to check the settings
        self.cap.read()

        for prop in self.targetCapConfig.keys():
            real_value = self.cap.get(prop)
            if real_value != self.targetCapConfig[prop]:
                raise Exception(f"Failed to set {prop} to {self.targetCapConfig[prop]}: got {real_value} instead")
        
        print("Camera settings applied successfully")
        print(f"framerate: {self.cap.get(cv.CAP_PROP_FPS)}")

        self.width = self.targetCapConfig[cv.CAP_PROP_FRAME_WIDTH]
        self.height = self.targetCapConfig[cv.CAP_PROP_FRAME_HEIGHT]
        self.framerate = self.targetCapConfig[cv.CAP_PROP_FPS]
        self.resolution = (self.width, self.height)

        self.frameTimes = []


    def videoStart(self):
        self.startTimestamp = datetime.now(timezone.utc)
        self.firstFramePos = self.cap.get(cv.CAP_PROP_POS_MSEC)
        self.lastFrameTimestamp = self.startTimestamp.timestamp()
        self.frameTimes.append(0)

    def posToTime(self, pos):
        delta = pos - self.firstFramePos
        return delta / 1000

    def startCapture(self):
        print("startCapture called")
        self.isRecording = True

        # get the current time as tz aware string in utc
        now = datetime.now(timezone.utc)

        # define video writer
        self.out = cv.VideoWriter(f'{now.isoformat()}.avi', cv.VideoWriter.fourcc(*self.store_codec), self.framerate, self.resolution)

        # initialize stats
        self.startTimestamp = -1
        self.firstFramePos = -1
        self.frameNumber = -1

        self.recordVideo()


    def captureEnded(self):
        print("captureEnded")
        self.isRecording = False
        self.out.release()
        cv.destroyAllWindows()
        print("Press 's' to start/stop recording, 'q' to quit")


    def recordVideo(self):
        print("recordVideo called")
        while True:
            # if cv.waitKey(1) == ord("q"):
                # print("Stopping capture")
                # break
            # Check if new frame is available
            if not self.cap.grab():
                continue

            currentFrameTimestamp = datetime.now(timezone.utc).timestamp()
            
            self.frameNumber += 1
            # is this the first frame we got?
            if self.frameNumber == 0:
                self.videoStart()
            else:
                self.frameTimes.append(currentFrameTimestamp - self.lastFrameTimestamp)
            
            self.lastFrameTimestamp = currentFrameTimestamp

            ret, frame = self.cap.retrieve()
            # if frame is read correctly ret is True
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break
            

            # write the frame
            self.out.write(frame)

            print(f"Frame number {self.frameNumber}, time {currentFrameTimestamp - self.startTimestamp.timestamp()}")

            # Display the resulting frame
            # cv.imshow('frame', frame)
        
        self.captureEnded()
    
    def __del__(self):
        print('__del__ called')
        # When everything done, release the capture

        self.cap.release()
        if self.out:
            self.out.release()
        cv.destroyAllWindows()

if __name__ == "__main__":
    vm = VideoManager("MJPG", (1920, 1080), 60)
    # vm.startCapture()
    print("Press 's' to start/stop recording, 'q' to quit")

    vm.startCapture()
    
    print(vm.frameTimes)
    with open("frameTimes.txt", "w") as f:
        f.write("\n".join(map(str, vm.frameTimes)))
    print("Exiting...")

