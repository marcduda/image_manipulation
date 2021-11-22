from skimage.transform import warp, swirl
from utils import wavelet, wave, plot_3d
import matplotlib.pylab as plt
import numpy as np
import cv2
import subprocess


class VideoManipulation:

    def __init__(self, manipulation_type):
        self.manipulation_type = manipulation_type


class WaveletManipulation(VideoManipulation):

    def __init__(self, manipulation_type):
        super().__init__(manipulation_type)

    def manipulate_and_save(self, frame, name, tilt):
        im = warp(frame, wavelet, map_args={'t': tilt})
        plt.imsave(name, im)


class ThreeDPlotManipulation(VideoManipulation):

    def __init__(self, manipulation_type):
        super().__init__(manipulation_type)

    def manipulate_and_save(self, frame, name, tilt, channel_to_plot=0):
        Y = np.arange(frame.shape[0])
        X = np.arange(frame.shape[1])
        Z1 = im[..., channel_to_plot]
        plot_3d(X, -Y, Z1, name, cmap='Greys')


class SwirlManipulation(VideoManipulation):

    def __init__(self, manipulation_type, cam):
        super().__init__(manipulation_type)
        self.centers = [(np.random.randint(20, cam.get(cv2.CAP_PROP_FRAME_WIDTH)-20),
                        np.random.randint(20, cam.get(cv2.CAP_PROP_FRAME_HEIGHT)-20))
                        for i in range(10)]

    def manipulate_and_save(self, frame, name, tilt):
        im = swirl(frame, rotation=0, strength=5, radius=20 + tilt, center=self.centers[0])
        if tilt >= 20:
            im = swirl(im, rotation=0, strength=5, radius=tilt - 20, center=self.centers[1])
        if tilt >= 40:
            im = swirl(im, rotation=0, strength=5, radius=tilt - 40, center=self.centers[2])
        if tilt >= 60:
            im = swirl(im, rotation=0, strength=5, radius=tilt - 60, center=self.centers[3])
        if tilt >= 80:
            im = swirl(im, rotation=0, strength=5, radius=tilt - 80, center=self.centers[4])
        if tilt >= 100:
            im = swirl(im, rotation=0, strength=5, radius=tilt - 100, center=self.centers[5])
        if tilt >= 120:
            im = swirl(im, rotation=0, strength=5, radius=tilt - 120, center=self.centers[6])
        if tilt >= 140:
            im = swirl(im, rotation=0, strength=5, radius=tilt - 140, center=self.centers[7])
        if tilt >= 160:
            im = swirl(im, rotation=0, strength=5, radius=tilt - 160, center=self.centers[8])
        if tilt >= 180:
            im = swirl(im, rotation=0, strength=5, radius=tilt - 180, center=self.centers[9])
        plt.imsave(name, im)


class WaveManipulation(VideoManipulation):

    def __init__(self, manipulation_type):
        super().__init__(manipulation_type)

    def manipulate_and_save(self, frame, name, tilt):
        im = np.empty_like(frame)
        plt.imsave('test.png', frame)
        for i in range(3):
            im[:, :, i] = warp(frame[:, :, i], wave, map_args={'tilt': tilt}) * 255
        im = im.astype(np.uint8)
        plt.imsave(name, im)


class ColorizeManipulation(VideoManipulation):

    def __init__(self, manipulation_type):
        super().__init__(manipulation_type)
        import torch

        if not torch.cuda.is_available():
            print('GPU not available.')
            returned_value = subprocess.call("cd /content", shell=True)
            returned_value = subprocess.call("git clone https://github.com/jantic/DeOldify.git DeOldify", shell=True)
            returned_value = subprocess.call("cd DeOldify", shell=True)
            returned_value = subprocess.call("pip install - r colab_requirements.txt", shell=True)
            import fastai
            from deoldify.visualize import *

            torch.backends.cudnn.benchmark = True
            returned_value = subprocess.call("mkdir models", shell=True)
            returned_value = subprocess.call("wget https://www.dropbox.com/s/mwjep3vyqk5mkjc/ColorizeStable_gen.pth?dl=0-O./models/ColorizeStable_gen.pth", shell=True)

    def manipulate_and_save(self, frame, name, tilt):
        prefix = '/'.join(name.split('/')[:-1])
        suffix = name.split('/')[-1]
        plt.imsave('/tmp/'+suffix, frame)
        colorizer = get_image_colorizer(artistic=True)
        colorizer.plot_transformed_image('/tmp/'+suffix, render_factor=38,
                                         display_render_factor=True, figsize=(16, 16), results_dir=prefix)
