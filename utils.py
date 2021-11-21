import matplotlib.pylab as plt
import matplotlib
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import ffmpeg
import cv2
from skimage.transform import warp, swirl


def check_rotation(path_video_file):
    # this returns meta-data of the video file in form of a dictionary
    meta_dict = ffmpeg.probe(path_video_file)
    # from the dictionary, meta_dict['streams'][0]['tags']['rotate'] is the key
    # we are looking for
    rotate_code = None
    rotate = meta_dict.get('streams', [dict(tags=dict())])[0].get('tags', dict()).get('rotate', 0)
    return round(int(rotate) / 90.0) * 90


def correct_rotation(frame, rotateCode):
    return cv2.rotate(frame, rotateCode)


def plot_3d(X, Y, Z, name, cmap):
    # implement this function to plot the channel pixel values in 3D
    matplotlib.rcParams['figure.figsize'] = (20.0, 10.0)
    fig = plt.figure()  # figsize=(15, 10)
    ax = Axes3D(fig)
    ax.plot_surface(Z, np.tile(X, (Y.shape[0], 1)), np.tile(Y, (X.shape[0], 1)).transpose(), cmap=cmap,
                    rcount=40, ccount=40, alpha=0.3)
    ax.plot_wireframe(Z, np.tile(X, (Y.shape[0], 1)), np.tile(Y, (X.shape[0], 1)).transpose(), color=cmap[:-1].lower(),
                      rcount=40, ccount=40)

    ax.view_init(0, 5)
    fig.tight_layout()
    plt.axis('off')
    plt.savefig(name, dpi=150)


def get_plot_3d(im, name, channel_to_plot=0):
    #im = plt.imread(image_path)
    Y = np.arange(im.shape[0])
    X = np.arange(im.shape[1])
    Z1 = im[..., channel_to_plot]
    plot_3d(X, -Y, Z1, name, cmap='Greys')


def wavelet(xy, t=10, sigma=30):
    kappa_sigma = np.exp(-0.5 * (sigma ** 2))
    c_sigma = np.sqrt(1 + np.exp(-(sigma ** 2)) - 2 * np.exp(-0.75 * (sigma ** 2)))
    xy[:, 1] += 50 * c_sigma * (np.pi ** -0.25) * np.exp(-0.5 * ((xy[:, 1] - t) ** 2)) * (
                np.cos(2 * np.pi * (xy[:, 1] - t) / sigma) - kappa_sigma)
    return xy


def add_wavelet(frame, tilt, name):
    im = warp(frame, wavelet, map_args={'t': tilt})
    plt.imsave(name, im)


def wave(xy, tilt=1):
    xy[:, 1] += 10*np.sin((2*np.pi*xy[:, 1]/128)-(2*np.pi*tilt/32)) + 10*np.sin((2*np.pi*xy[:, 1]/64)-(2*np.pi*tilt/32))
    return xy


def plot_wave(frame, tilt, name):
    im = np.empty_like(frame)
    plt.imsave('test.png', frame)
    for i in range(3):
        im[:, :, i] = warp(frame[:, :, i], wave, map_args={'tilt': tilt})*255
    im = im.astype(np.uint8)
    plt.imsave(name, im)


def plot_swirl(frame, tilt, name, centers):

    im = swirl(frame, rotation=0, strength=5, radius=20 + tilt, center=centers[0])
    if tilt >= 20:
        im = swirl(im, rotation=0, strength=5, radius=tilt - 20, center=centers[1])
    if tilt >= 40:
        im = swirl(im, rotation=0, strength=5, radius=tilt - 40, center=centers[2])
    if tilt >= 60:
        im = swirl(im, rotation=0, strength=5, radius=tilt - 60, center=centers[3])
    if tilt >= 80:
        im = swirl(im, rotation=0, strength=5, radius=tilt - 80, center=centers[4])
    if tilt >= 100:
        im = swirl(im, rotation=0, strength=5, radius=tilt - 100, center=centers[5])
    if tilt >= 120:
        im = swirl(im, rotation=0, strength=5, radius=tilt - 120, center=centers[6])
    if tilt >= 140:
        im = swirl(im, rotation=0, strength=5, radius=tilt - 140, center=centers[7])
    if tilt >= 160:
        im = swirl(im, rotation=0, strength=5, radius=tilt - 160, center=centers[8])
    if tilt >= 180:
        im = swirl(im, rotation=0, strength=5, radius=tilt - 180, center=centers[9])
    plt.imsave(name, im)
