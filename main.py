"""

This script shows how to create a video, in MP4 format, from image sequences (in PNG or JPG format)
of different resolution.

"""

import click
import os
import glob
import numpy as np
from skimage.io import imread
from skimage.transform import resize
import skvideo.io


@click.command()
@click.option(
    '--input-path',
    type=click.Path(),
    default=None,
    metavar='INPUT_PATH',
    help='Path where a sequence of images are located (e.g., PNG or JPG files).'
)
@click.option(
    '--output-path',
    type=click.Path(),
    default=None,
    metavar='OUTPUT_PATH',
    help='Path to save the video file.'
)
@click.option(
    '--image-extension',
    type=str,
    default='png',
    metavar='IMAGE_EXTENSION',
    help='Image extension. Use: "png", "jpg". '
)
@click.option(
    '--video-filename',
    type=str,
    default='video.mp4',
    metavar='VIDEO_FILENAME',
    help='Output video filename (MP4).'
)
@click.option(
    '--background-color',
    type=str,
    default='noise',
    metavar='BACKGROUND_COLOR',
    help='Background color used for the video. Use: "black" or "noise".'
)
@click.option(
    '--verbose',
    is_flag=True,
    default=False,
    help='If True, messages will be displayed.'
)
def main(
    input_path,
    output_path,
    image_extension,
    video_filename,
    background_color,
    verbose
):

    ####################################################################################################################
    #
    # Initialization.
    #
    ####################################################################################################################

    if verbose:
        print('[ Loading image data ]')
        print('\t- Input path: {}'.format(input_path))
        print('\t- Format: {}'.format(image_extension))
        print('\t- Images: ')

    image_files = []
    image_size = []

    # Load a sequence of images from the specified path.
    for index, file in enumerate(glob.glob("{}/*.{}".format(input_path, image_extension))):
        img = imread(file)
        image_size.append(img.shape)
        image_files.append(file)
        if verbose:
            print('\t\t[ {} ][ Image shape: {} ] File: {}'.format(index, img.shape, file))

    if verbose:
        print(' ')

    # Ger the maximum size.
    max_image_size = np.max(np.array(image_size), axis=0)

    # Dimensions of the array to store every frame in the video.
    output_data = np.zeros((1, max_image_size[0], max_image_size[1], 3), dtype=np.uint8)

    if verbose:
        print('[ 4D array to store a single frame ] Array shape: {}\n'.format(output_data.shape))

    # Create the output path to store the video if it doesn't exist.
    output_path = None if output_path == "None" else output_path

    if output_path is not None:
        if not os.path.exists(output_path):
            os.makedirs(output_path)

    # Path and filename used to store the video.
    output_ffname = video_filename if output_path is None else "{}/{}".format(output_path, video_filename)

    if verbose:
        print('[ Video file (MP4) to be created ] File: {}\n'.format(output_ffname))

    ####################################################################################################################
    #
    # Create a video from image sequences...
    #
    ####################################################################################################################

    # Create a writer object to create a video.
    writer = skvideo.io.FFmpegWriter(
        output_ffname,
        inputdict={'-r': '4'},
        outputdict={'-r': '4'}
    )

    if verbose:
        print('[ Creating video from image sequences ] --> Start')

    num_frames = len(image_files)

    # Loop over frames...
    for i, file in enumerate(image_files):

        if background_color == 'noise':
            output_data[0, :, :, :] = (np.random.random(output_data.shape) * 255.0).astype(np.uint8)
        elif background_color == 'black':
            output_data[0, :, :, :] = 0

        if file.endswith(".png"):
            img = imread(file)[:, :, 0:3].astype(np.uint8)
        elif file.endswith(".jpg"):
            img = imread(file, plugin='matplotlib')[:, :, 0:3].astype(np.uint8)

        current_rows = img.shape[0]
        current_cols = img.shape[1]
        ratio = float(current_rows / current_cols)
        max_cols = max_image_size[1]
        max_rows = max_image_size[0]

        scaled_rows = max_rows
        scaled_cols = min(max_cols, int(max_rows / ratio))

        scaled_image_size = (
            scaled_rows,
            scaled_cols
        )

        img = resize(img, scaled_image_size, preserve_range=True, anti_aliasing=True).astype(np.uint8)

        min_value = np.min(img)
        max_value = np.max(img)

        delta_x = int(
            (max_image_size[1] - img.shape[1]) / 2.
        )

        delta_y = int(
            (max_image_size[0] - img.shape[0]) / 2.
        )

        print('\t[ Frame {} of {} ] Image Size = ({}, {}) | Image Range = [ {}, {} ] | Ratio = {:0.2f}'.format(
                i+1,
                num_frames,
                img.shape[0],
                img.shape[1],
                min_value,
                max_value,
                ratio
            )
        )

        output_data[0, delta_y:delta_y + img.shape[0], delta_x:delta_x + img.shape[1], 0:3] = img[:, :, 0:3]

        # Write a single frame on disk.
        writer.writeFrame(output_data[0, :, :, :])

    # Close the writer object.
    writer.close()

    if verbose:
        print('[ Creating video from image sequences ] --> End\n')


if __name__ == '__main__':
    main()
