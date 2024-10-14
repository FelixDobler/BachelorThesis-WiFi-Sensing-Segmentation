#!/usr/bin/python
from datetime import datetime
import subprocess
import os
from sys import stdout, stderr
import signal
import time

record_manager = None

def stop_handler(signum, frame):
    stop_actions()

def stop_actions():
    global record_manager
    print("\n------------\nexiting...")
    record_manager.stop()
    FNULL.close()
    exit(0)

def run(*popenargs, **kwargs):
    input = kwargs.pop("input", None)
    check = kwargs.pop("handle", False)

    if input is not None:
        if "stdin" in kwargs:
            raise ValueError("stdin and input arguments may not both be used.")
        kwargs["stdin"] = subprocess.PIPE

    process = subprocess.Popen(*popenargs, **kwargs)
    try:
        stdout, stderr = process.communicate(input)
    except:
        process.kill()
        process.wait()
        raise
    retcode = process.poll()
    if check and retcode:
        raise subprocess.CalledProcessError(retcode, stdout, stderr)
    return retcode, stdout, stderr


FNULL = open(os.devnull, "rw")


class RecordManager:
    user = "user1"
    ffmpeg = None
    record_video_enabled = True
    record_dir = "/root/record/recordings"
    record_dir_csi = os.path.join(record_dir, "csi", user)
    record_dir_video = os.path.join(record_dir, "video", user)

    record_sequence = None

    is_recording = False
    HOSTAPD_TIMEOUT = 10

    activities = {
        1: "boxing",
        2: "hand swing",
        3: "picking up",
        4: "hand raising",
        5: "running",
        6: "pushing",
        7: "squatting",
        8: "drawing O",
        9: "walking",
        10: "drawing X",
    }
    recording_sequences = [
        ("iw", (1, 2)),
        ("ph", (3, 4)),
        ("rp", (5, 6)),
        ("sd", (7, 8)),
        ("wd", (9, 10)),
    ]

    def __init__(self):
        self.hostapd = None
        if not self.is_connection_established():
            self.establish_connection()

    def start(self):
        while True:
            self.wait_for_keyboard_input()
            self.start_stop()

    def stop(self):
        if self.is_recording:
            self.stop_record()
            
        ret = subprocess.call(
            ["ssh", "BaProj1-Lan", "pkill", "-f", "-SIGTERM", "hostapd.*hostapd.conf"]
        )
        if ret != 0:
            print("Error terminating hostapd")
        if self.hostapd:
            # print("hostapd is still running, terminating...")
            self.hostapd.terminate()
            self.hostapd.wait()

    def start_record(self):
        print("Starting recording")

        self.select_record_sequence()
                
        self.recording_name = datetime.now().isoformat().replace(":", "-").replace(".", "-")
        if self.record_sequence:
            self.recording_name += "_seq-" + self.record_sequence[0]

        print(
            "Recording name: {recording_name}".format(
                recording_name=self.recording_name
            )
        )
        # Start Camera recording
        if self.record_video_enabled:
            self.ffmpeg = subprocess.Popen(
                [
                    "ffmpeg",
                    "-v",
                    "error",
                    "-f",
                    "v4l2",
                    "-input_format",
                    "mjpeg",
                    "-framerate",
                    "60",
                    "-video_size",
                    "1280x720",
                    "-i",
                    "/dev/video0",
                    os.path.join(self.record_dir_video, self.recording_name + ".mp4"),
                ],
                stdout=FNULL,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE,
            )

        # Start CSI recording
        self.csi_rec = subprocess.Popen(
            [
                "/root/Atheros-CSI-Tool-UserSpace-APP/recvCSI/recv_csi",
                os.path.join(self.record_dir_csi, self.recording_name + ".raw"),
            ]
        )
        # Start CSI sending
        self.csi_send = subprocess.Popen(
            ["ssh", "BaProj1-Lan", "/root/sendData.sh", "-1"],
            stdin=FNULL,
            stdout=subprocess.PIPE,
        )
        self.is_recording = True

    def stop_record(self):
        ret = subprocess.call(
            ["ssh", "BaProj1-Lan", "pkill", "-SIGINT", "send_Data"],
        )

        self.csi_send.wait()

        if ret != 0:
            print("Error stopping sendData.sh")

        # Stop CSI recording
        if self.csi_rec.poll() is None:
            self.csi_rec.terminate()

        self.csi_rec.wait()

        # Stop Camera recording
        if self.record_video_enabled:
            try:
                self.ffmpeg.stdin.write(b"q")
                self.ffmpeg.stdin.flush()

                print("Waiting for ffmpeg to finish")
                self.ffmpeg.wait()
            except Exception:
                print(self.ffmpeg.stderr.readlines())

        with open(
            os.path.join(self.record_dir, "sendTimings", self.recording_name) + ".txt",
            "wb",
        ) as f:
            f.write(self.csi_send.stdout.read())

        print(
            "Recording written to file {recording_name}(.raw|.mp4)".format(
                recording_name=self.recording_name
            )
        )
        self.recording_name = None
        self.is_recording = False
        self.record_sequence = None

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
            self.hostapd = subprocess.Popen(
                ["ssh", "BaProj1-Lan", "/root/start_hostapd.sh"],
                stdin=FNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

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
        else:
            stderr.write("Network is already active, unexpected state")

        # connect
        run(["/root/activate_wifi.sh"], handle=True, stdout=FNULL)

        if not self.is_connection_established():
            print("Connection to BaProj1 could not be established")
            stop_actions()

    def start_stop(self):
        if self.is_recording:
            self.stop_record()
        else:
            self.start_record()

    def wait_for_keyboard_input(self):
        raw_input(
            "Press 'enter' to {action} recording:\n".format(
                action="stop" if self.is_recording else "start"
            )
        )
    
    def select_record_sequence(self):
        print("Select the sequence that is being recorded: [1-5]")
        for i, (s_name, s_activities) in enumerate(self.recording_sequences):
            print("{i}: {s_name} -> {activity1} and {activity2}".format(
                i=i+1, 
                s_name=s_name, 
                activity1=self.activities[s_activities[0]], 
                activity2=self.activities[s_activities[1]]
            ))
        num = raw_input("")
        # check if num sting is integer
        if not num:
            print("Continuing without recording sequence")
            return
        
        try:
            num = int(num)
        except ValueError:
            print("Please enter a valid number")
            return self.select_record_sequence()

        self.record_sequence = self.recording_sequences[num-1]


if __name__ == "__main__":
    signal.signal(signal.SIGINT, stop_handler)
    record_manager = RecordManager()
    record_manager.start()
