# HackerFX v2

If you've seen [HackerFX](https://github.com/Aniruddha-Deb/HackerFX), this is 
a rewrite in python with a bunch of new features:

- Support for multicoloured images
- Square output characters (no more resizing images before passing them in)
- Hex character support
- Serialize a file and write the bitstream to the image
- Support for videos(requires ffmpeg and ffprobe)

Some examples:

![monochrome](examples/monochrome.png)
![looks pretty good](examples/monochrome_out.png)

![multicoloured](examples/jojo.jpg)
![multicoloured output](examples/jojo_out.png)

![different colour](examples/initiald.jpg)
![and hex output](examples/initiald_out.jpg)

![video file](examples/bad_apple.gif)
![and hex output](examples/bad_apple_out.gif)

Installation:

1. (Optional) Create a virtual environment using `venv` or `virtualenv`.
2. Run `pip install -r requirements.txt`.
3. Invoke the script with appropriate arguments as per usage given below.   

Usage for images:
```
usage: hackerfx.py [-h] [-x] [-c COLOR] [-o OUTPUT] [-d DATA] input_image

Binarizes images in the hacker format

positional arguments:
  input_image           Path to input image

optional arguments:
  -h, --help            show this help message and exit
  -x, --hex             Encode Image in Hex
  -c COLOR, --color COLOR
                        RGB Hex Output Image color (default: Hacker Green - 0x39FF14)
  -o OUTPUT, --output OUTPUT
                        Output file name
  -d DATA, --data DATA  Data file to encode into image
```

Usage for videos(requires ffmpeg and ffprobe)
```
usage: hackerfx_video.py [-h] [-x] [-c COLOR] [-o OUTPUT] input_video

Binarizes videos in the hacker format

positional arguments:
  input_video           Path to input video

options:
  -h, --help            show this help message and exit
  -x, --hex             Encode Video in Hex
  -c COLOR, --color COLOR
                        RGB Hex Output Video color (default: Hacker Green - 0x39FF14)
  -o OUTPUT, --output OUTPUT
                        Output file name
```
