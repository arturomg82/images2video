# Image2Video: Creating a video from image sequences.

This script shows how to create a video, in MP4 format, from image sequences (in PNG or JPG format)
of different resolution.

## Dependencies.

Python 3.8, scikit-image 0.18.1, scikit-video 1.1.11, click 7.1.2

## Examples.

To create a video from images, use the following instructions:

```
python main.py \
--input-path "images_path" \
--output-path "None" \
--image-extension "png" \
--video-filename "my_video.mp4" \
--background-color "noise" \
--verbose
```

Where:

- `input-path`: Path where a sequence of images are located (e.g., PNG or JPG files).
- `output-path`: Path to save the video file.
- `image-extension`: Image extension. Use: "png", "jpg".
- `video-filename`: Output video filename (MP4). Default: "video.mp4".
- `background-color`: Background color used for the video. Use: "black" or "noise".
- `verbose`: If True, messages will be displayed.
