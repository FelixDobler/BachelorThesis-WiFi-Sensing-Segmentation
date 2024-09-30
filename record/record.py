#!/usr/bin/python
from datetime import datetime
import subprocess
import os
from sys import stdout, stderr
import signal
import time

def stop_handler(signum, frame):
    stop()
    
def stop():
    print("\n------------")
    record_manager.exit()
    FNULL.close()
    exit(0)

def run(*popenargs, **kwargs):
    input = kwargs.pop("input", None)
    check = kwargs.pop("handle", False)

    if input is not None:
        if 'stdin' in kwargs:
            raise ValueError('stdin and input arguments may not both be used.')
        kwargs['stdin'] = subprocess.PIPE

    process = subprocess.Popen(*popenargs, **kwargs)
    try:
        stdout, stderr = process.communicate(input)
    except:
        process.kill()
        process.wait()
        raise
    retcode = process.poll()
    if check and retcode:
        raise subprocess.CalledProcessError(
            retcode, stdout, stderr)
    return retcode, stdout, stderr

FNULL = open(os.devnull, 'rw')

class RecordManager:
    ffmpeg = None
    record_video_enabled = False
    record_dir = "/root/record/recordings"
    record_dir_csi = os.path.join(record_dir, "csi")
    record_dir_video = os.path.join(record_dir, "video")

    is_recording = False
    HOSTAPD_TIMEOUT = 10

    def __init__(self):
        self.hostapd = None
        if not self.is_connection_established():
            self.establish_connection()
        

    def start_record(self):
        print("Starting recording")
        self.recording_name = datetime.now().isoformat().replace(':', '-').replace('.', '_') # timespec="seconds"
        print("Recording name: {recording_name}".format(recording_name=self.recording_name))
        # Start Camera recording
        if self.record_video_enabled:
            self.ffmpeg = subprocess.Popen(["ffmpeg", "-v", "error", "-f", "v4l2", "-input_format", "mjpeg", "-framerate", "60", "-video_size", "1280x720", "-i", "/dev/video0", 
                                        os.path.join(self.record_dir_video, self.recording_name + ".mp4")],
                                        stdout=FNULL, stderr=subprocess.PIPE, stdin=subprocess.PIPE)

        # Start CSI recording
        self.csi_rec = subprocess.Popen(["/root/Atheros-CSI-Tool-UserSpace-APP/recvCSI/recv_csi", os.path.join(self.record_dir_csi, self.recording_name + ".raw")])
        # Start CSI sending
        self.csi_send = subprocess.Popen(["ssh", "BaProj1-Lan", "/root/sendData.sh", "-1"], stdin=FNULL, stdout=subprocess.PIPE)
        self.is_recording = True

    def stop_record(self):
        # print("Stopping recording")
        # Stop CSI sending
        # self.csi_send.send_signal(signal.SIGINT)
        ret = subprocess.call(['ssh', 'BaProj1-Lan', 'pkill', '-SIGINT', 'send_Data'], )
        # print("sent sigint to send_Data")
        # print(self.csi_send.poll())
        
        self.csi_send.wait()
        
        if ret != 0:
            print("Error stopping sendData.sh")
        
        # Stop CSI recording
        # self.csi_rec.terminate()
        # self.csi_send.terminate()
        if self.csi_rec.poll() is None:
            self.csi_rec.terminate()
        # print("sent SIGINT to csi_rec")

        # Wait for CSI sending and recording to finish
        # print("Waiting for csi_send to finish")
        self.csi_send.wait()
        # print("Waiting for csi_rec to finish")
        self.csi_rec.wait()
        
        # Stop Camera recording
        if self.record_video_enabled:
            try:
                self.ffmpeg.stdin.write(b'q')
                self.ffmpeg.stdin.flush()

                print("Waiting for ffmpeg to finish")
                self.ffmpeg.wait()
            except Exception:
                print(self.ffmpeg.stderr.readlines())


        # print(self.csi_send.stdout.readlines())
        with open(os.path.join(self.record_dir, "sendTimings", self.recording_name) + '.txt', "wb") as f:
            f.write(self.csi_send.stdout.read())

        print("Recording written to file {recording_name}(.raw|.mp4)".format(recording_name=self.recording_name))
        self.recording_name = None
        self.is_recording = False

    def exit(self):
        if self.is_recording:
            self.stop_record()
        # if self.hostapd is not None:
        # print("hostapd was created by this process")
        ret = subprocess.call(["ssh", "BaProj1-Lan", "pkill", "-f", "-SIGTERM", "hostapd.*hostapd.conf"])
        if ret != 0:
            print("Error terminating hostapd")
        if self.hostapd:
            # print("hostapd is still running, terminating...")
            self.hostapd.terminate()
            self.hostapd.wait()
        # else:
        #     # TODO don't only kill hostapd but also disable wifi
        #     end_hostapd = subprocess.Popen(["ssh", "BaProj1-Lan", "pkill", "-SIGTERM", "hostapd"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #     ret = end_hostapd.wait()
        #     if ret == 0:
        #         print("Hostapd terminated")
        #     else:
        #         print(end_hostapd.stderr.readlines())
        #         print("Error terminating hostapd")
            

    def is_connection_established(self):
        try:
            run(["ping", "-c", "1", "-w", "1", "BaProj1"], handle=True, stdout=FNULL)
            return True
        except subprocess.CalledProcessError as e:
            return False
    
    def establish_connection(self):
        ret, _, _ = run(["ssh", "BaProj1-Lan", "pgrep hostapd"])
        if ret == 1:
            print("Network is not active, starting...")
            self.hostapd = subprocess.Popen(["ssh", "BaProj1-Lan", "/root/start_hostapd.sh"], stdin=FNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            self.timeout_reached = False
            def timeout(signum, frame):
                self.timeout_reached = True
            signal.signal(signal.SIGALRM, timeout)
            signal.alarm(self.HOSTAPD_TIMEOUT)

            while not self.timeout_reached:
                line = self.hostapd.stdout.readline()
                if "AP-ENABLED" in line:
                    print("Hostapd started")
                    break
            # signal.alarm(0)
        else:
            stderr.write("Network is already active, unexpected state")


        # connect
        run(["/root/activate_wifi.sh"], handle=True, stdout=FNULL)

        if not self.is_connection_established():
            print("Connection to BaProj1 could not be established")
            stop()

    def start_stop(self):
        if self.is_recording:
            self.stop_record()
        else:
            self.start_record()


    def wait_for_keyboard_input(self):
        raw_input("Press 'enter' to {action} recording:\n".format(action="stop" if self.is_recording else "start"))
    
    def start(self):
        while True:
            self.wait_for_keyboard_input()
            self.start_stop()


if __name__ == "__main__":
    signal.signal(signal.SIGINT, stop_handler)
    record_manager = RecordManager()
    record_manager.start()
