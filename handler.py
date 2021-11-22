import cv2
from manipulation import VideoManipulation
from utils import check_rotation, correct_rotation
import subprocess


class VideoHandler:
    def __init__(self, input_data, output_dir):
        # So we can quit the window from within the functions
        self.input_data = input_data
        self.cam = cv2.VideoCapture(input_data)
        self.rotateCode = check_rotation(input_data)
        self.output_dir = output_dir

    def transform(self, video_manipulation: VideoManipulation):
        tilt = 0
        while True:
            # reading from frame
            ret, frame = self.cam.read()
            name = self.output_dir + '/frame_' + str(tilt) + '.png'

            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                if self.rotateCode is not None:
                    frame = correct_rotation(frame, self.rotateCode)
                video_manipulation.manipulate_and_save(frame, name, tilt)
            if not ret:
                break
            else:
                tilt += 1

    def recompose(self):
        cmd = "ffmpeg -i " + self.output_dir + "/frame_%01d.png -y " + self.output_dir + "/res.mp4"
        returned_value = subprocess.call(cmd, shell=True)