from PIL import Image
from argparse import ArgumentParser
import numpy as np
import random
import sys
import subprocess
import os
from hackerfx import parse_color, random_bit, random_hex, process

if __name__ == "__main__":
    parser = ArgumentParser(
        prog="hackerfx_video.py",
        description="Binarizes videos in the hacker format"
    )
    parser.add_argument('input', metavar='input_video', type=str,
                        help="Path to input video")
    parser.add_argument('-x', '--hex', action='store_true',
                        help="Encode Video in Hex")
    parser.add_argument('-c', '--color', type=parse_color, default="0x39FF14",
                        help="RGB Hex Output Video color (default: Hacker Green - 0x39FF14)")
    parser.add_argument('-o', '--output', type=str, default='output.mp4',
                        help="Output file name")

    args = parser.parse_args(sys.argv[1:])
    data_func = random_bit
    if args.hex:
        data_func = random_hex
    subprocess.run(['ffmpeg', '-i', args.input, 'frames_input/img%d.png', '-hide_banner'])
    subprocess.run(['ffmpeg', '-i', args.input, '-vn', '-acodec', 'copy', 'audio.m4a'])
    frames = eval(subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries',
                                  'stream=avg_frame_rate', '-of', 'default=nw=1:nk=1', args.input],
                                 stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout)
    img_list = os.listdir("frames_input")
    for img in img_list:
        process("frames_input\\" + img, color=args.color, outpath="frames_processed\\" + img, data_gen=data_func)
        print(img + " converted")
    subprocess.call(['ffmpeg', '-i', 'frames_processed/img%d.png', '-i', 'audio.m4a', '-c:v', 'libx264', '-r',
                                     str(frames), '-pix_fmt', 'yuv420p', '-c:a', 'copy', '-shortest', args.output])
    cleanup = os.listdir("frames_processed")
    for img in img_list:
        os.remove("frames_input\\"+img)
    for img in cleanup:
        os.remove("frames_processed\\"+img)
    os.remove("audio.m4a")
