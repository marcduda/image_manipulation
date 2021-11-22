import argparse
from handler import VideoHandler
from manipulation import WaveletManipulation, ThreeDPlotManipulation, SwirlManipulation, WaveManipulation,\
ColorizeManipulation

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--is_video", help="is input data a video", type=bool)
    parser.add_argument("--input_data", help="input data to process", type=str)
    parser.add_argument("--output_dir", help="output directory to which save the data", type=str)
    parser.add_argument("--manipulation_type", help="the type of transformation to apply"
                        , nargs='?', default=False, type=str,
                        choices=['wavelet', '3d_plot', 'swirl', 'wave', 'colorize'])
    parser.add_argument("--output_video", help="compute a video from the processed data"
                        , nargs='?', default=False, type=bool)
    args = parser.parse_args()

    if args.is_video:

        handler = VideoHandler(args.input_data, args.output_dir)
        manipulation_dict = {'wavelet': WaveletManipulation(args.manipulation_type),
                             '3d_plot': ThreeDPlotManipulation(args.manipulation_type),
                             'swirl': SwirlManipulation(args.manipulation_type, handler.cam),
                             'wave': WaveManipulation(args.manipulation_type),
                             'colorize': ColorizeManipulation(args.manipulation_type)
                             }
        manipulation = manipulation_dict[args.manipulation_type]
        handler.transform(manipulation)
        '''
        if args.plot_swirl:
            centers = [(np.random.randint(20, cam.get(cv2.CAP_PROP_FRAME_WIDTH)-20),
                        np.random.randint(20, cam.get(cv2.CAP_PROP_FRAME_HEIGHT)-20))
                       for i in range(10)]
        tilt = 0
        while True:
            # reading from frame
            ret, frame = cam.read()
            if rotateCode is not None:
                frame = correct_rotation(frame, rotateCode)
            name = args.output_dir + '/frame_' + str(tilt) + '.png'

            if args.plot_3d & ret:
                get_plot_3d(frame, name, 0)

            if args.plot_wavelet & ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                add_wavelet(frame, tilt, name)

            if args.plot_wave & ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                plot_wave(frame, tilt, name)

            if args.plot_swirl & ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                if tilt == 0:
                    print(frame.shape)
                plot_swirl(frame, tilt, name, centers)

            if not ret:
                break
            else:
                tilt += 1
        '''
    else:  # process image_by_image
        print("continue")

    if args.output_video:
        handler.recompose()
        #cmd = "ffmpeg -i " + args.output_dir + "/frame_%01d.png -y " + args.output_dir + "/res.mp4"
        #returned_value = subprocess.call(cmd, shell=True)

