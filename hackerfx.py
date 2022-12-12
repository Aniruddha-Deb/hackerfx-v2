from PIL import Image
from argparse import ArgumentParser
import numpy as np
import random
import sys
import subprocess
import os
import shutil

zero = np.array([
    [0,0,0,0,0,0],
    [0,0,1,1,1,0],
    [0,1,0,0,0,1],
    [0,1,0,0,0,1],
    [0,1,0,0,0,1],
    [0,0,1,1,1,0],
])
one = np.array([
    [0,0,0,0,0,0],
    [0,0,1,1,0,0],
    [0,0,0,1,0,0],
    [0,0,0,1,0,0],
    [0,0,0,1,0,0],
    [0,1,1,1,1,1],
])
two = np.array([
    [0,0,0,0,0,0],
    [0,1,1,1,1,0],
    [0,0,0,0,0,1],
    [0,0,1,1,1,0],
    [0,1,0,0,0,0],
    [0,1,1,1,1,1],
])
three = np.array([
    [0,0,0,0,0,0],
    [0,1,1,1,1,0],
    [0,0,0,0,0,1],
    [0,0,0,1,1,1],
    [0,0,0,0,0,1],
    [0,1,1,1,1,0],
])
four = np.array([
    [0,0,0,0,0,0],
    [0,1,0,0,0,0],
    [0,1,0,0,1,0],
    [0,1,1,1,1,1],
    [0,0,0,0,1,0],
    [0,0,0,0,1,0],
])
five = np.array([
    [0,0,0,0,0,0],
    [0,1,1,1,1,1],
    [0,1,0,0,0,0],
    [0,1,1,1,1,0],
    [0,0,0,0,0,1],
    [0,1,1,1,1,0],
])
six = np.array([
    [0,0,0,0,0,0],
    [0,0,1,1,1,0],
    [0,1,0,0,0,0],
    [0,1,1,1,1,0],
    [0,1,0,0,0,1],
    [0,0,1,1,1,0],
])
seven = np.array([
    [0,0,0,0,0,0],
    [0,1,1,1,1,1],
    [0,0,0,0,0,1],
    [0,0,0,0,0,1],
    [0,0,0,0,0,1],
    [0,0,0,0,0,1],
])
eight = np.array([
    [0,0,0,0,0,0],
    [0,0,1,1,1,0],
    [0,1,0,0,0,1],
    [0,0,1,1,1,0],
    [0,1,0,0,0,1],
    [0,0,1,1,1,0],
])
nine = np.array([
    [0,0,0,0,0,0],
    [0,0,1,1,1,0],
    [0,1,0,0,0,1],
    [0,0,1,1,1,1],
    [0,0,0,0,0,1],
    [0,0,0,0,0,1],
])
A = np.array([
    [0,0,0,0,0,0],
    [0,0,1,1,1,0],
    [0,1,0,0,0,1],
    [0,1,1,1,1,1],
    [0,1,0,0,0,1],
    [0,1,0,0,0,1],
])
B = np.array([
    [0,0,0,0,0,0],
    [0,1,1,1,1,0],
    [0,1,0,0,0,1],
    [0,1,1,1,1,0],
    [0,1,0,0,0,1],
    [0,1,1,1,1,0],
])
C = np.array([
    [0,0,0,0,0,0],
    [0,0,1,1,1,1],
    [0,1,0,0,0,0],
    [0,1,0,0,0,0],
    [0,1,0,0,0,0],
    [0,0,1,1,1,1],
])
D = np.array([
    [0,0,0,0,0,0],
    [0,1,1,1,1,0],
    [0,1,0,0,0,1],
    [0,1,0,0,0,1],
    [0,1,0,0,0,1],
    [0,1,1,1,1,0],
])
E = np.array([
    [0,0,0,0,0,0],
    [0,1,1,1,1,1],
    [0,1,0,0,0,0],
    [0,1,1,1,0,0],
    [0,1,0,0,0,0],
    [0,1,1,1,1,1],
])
F = np.array([
    [0,0,0,0,0,0],
    [0,1,1,1,1,1],
    [0,1,0,0,0,0],
    [0,1,1,1,0,0],
    [0,1,0,0,0,0],
    [0,1,0,0,0,0],
])

chars = [ a[...,np.newaxis].repeat(3,axis=2)
    for a in [zero, one, two, three, four, five, six, seven, eight, nine, A, B,
              C, D, E, F]
]

def render_char(i,j,mat,char,intensity,color):
    mat[i:i+6,j:j+6,:] += chars[char]*intensity*color

def random_bit():
    return random.randint(0,1)

def random_hex():
    return random.randint(0,15)

def parse_color(color_hex):
    if color_hex.startswith('0x'):
        color_hex = color_hex[2:]

    return np.array([[[
        int(color_hex[0:2],base=16),
        int(color_hex[2:4],base=16),
        int(color_hex[4:6],base=16)
    ]]])

def process(imgpath, color=np.array([[[0x39,0xFF,0x14]]]), outpath='output.png', data_gen=random_bit):
    img = Image.open(imgpath)
    img = img.resize((img.size[0]//4,img.size[1]//4))
    img = img.convert('L')
    data = np.array(img) # 1-D image

    outimg = np.zeros((data.shape[0]*6,data.shape[1]*6))
    # outimg = outimg[np.newaxis,...].repeat(3,axis=0) # add 3 channels
    outimg = outimg[...,np.newaxis].repeat(3,axis=2)

    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            # discretizing
            intensity = data[i,j]/255
            render_char(i*6,j*6,outimg,data_gen(),intensity,color)

    output = Image.fromarray(np.uint8(outimg), mode='RGB')
    output.save(outpath)

class HexDataEncoder:

    def __init__(self, filepath):
        self.file = open(filepath, 'rb')
        self.eof_hit = False
        self.curr_byte_pos = 0
        self.nibble_mask = 0x0F
        self.curr_byte = None

    def get_next_token(self):
        if not self.eof_hit:
            if (not self.curr_byte) or (self.curr_byte_pos == 0):
                self.curr_byte = self.file.read(1)
            if self.curr_byte == b"":
                self.eof_hit = True
                return random_hex()
            nibble = (self.curr_byte[0] & (self.nibble_mask << (4*self.curr_byte_pos)))>>(4*self.curr_byte_pos)
            self.curr_byte_pos = (self.curr_byte_pos+1)%2
            return nibble
        else:
            return random_hex()

class BinaryDataEncoder:

    def __init__(self, filepath):
        self.file = open(filepath, 'rb')
        self.eof_hit = False
        self.bitmask = 0x01
        self.curr_byte_pos = 0
        self.curr_byte = None

    def get_next_token(self):
        if not self.eof_hit:
            if (not self.curr_byte) or (self.curr_byte_pos == 0):
                self.curr_byte = self.file.read(1)
            if self.curr_byte == b"":
                self.eof_hit = True
                return random_hex()
            nibble = (self.curr_byte[0] & (self.bitmask << self.curr_byte_pos))>>(self.curr_byte_pos)
            self.curr_byte_pos = (self.curr_byte_pos+1)%8
            return nibble
        else:
            return random_bit()

def process_video(vidpath, color=np.array([[[0x39,0xFF,0x14]]]), outpath='output.mp4', data_gen=random_bit):
    os.makedirs("frames_input", exist_ok=True)
    os.makedirs("frames_processed", exist_ok=True)

    subprocess.run(['ffmpeg', '-i', vidpath, 'frames_input/img%d.png', '-hide_banner'])
    subprocess.run(['ffmpeg', '-i', vidpath, '-vn', '-acodec', 'copy', 'audio.m4a'])
    frames = eval(subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries',
                                  'stream=avg_frame_rate', '-of', 'default=nw=1:nk=1', vidpath],
                                 stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout)
    img_list = os.listdir("frames_input")
    for img in img_list:
        process(f"frames_input/{img}", color=color, outpath=f"frames_processed/{img}", data_gen=data_gen)
        print(img + " converted")
    subprocess.call(['ffmpeg', '-i', 'frames_processed/img%d.png', '-i', 'audio.m4a', '-c:v', 'libx264', '-r',
                                     str(frames), '-pix_fmt', 'yuv420p', '-c:a', 'copy', '-shortest', outpath])

    shutil.rmtree('frames_input')
    shutil.rmtree('frames_processed')
    os.remove("audio.m4a")

if __name__ == "__main__":
    parser = ArgumentParser(
            prog = "hackerfx.py",
            description="Binarizes images/videos in a hacker-themed format"
            )
    parser.add_argument('input', metavar='input_image', type=str, 
                        help="Path to input image")
    parser.add_argument('-x', '--hex', action='store_true',
                        help="Encode using Hex digits")
    parser.add_argument('-v', '--video', action='store_true',
                        help="Encode video")
    parser.add_argument('-c', '--color', type=parse_color, default="0x39FF14",
                        help="RGB Output color in hex (default: Hacker Green - 0x39FF14)")
    parser.add_argument('-o', '--output', type=str, default='output.png',
                        help="Output file name")
    parser.add_argument('-d', '--data', type=str, 
                        help="Data file to encode into image")

    args = parser.parse_args(sys.argv[1:])
    data_func = random_bit
    if args.hex:
        data_func = random_hex
    if args.data:
        if args.hex:
            enc = HexDataEncoder(args.data)
        else:
            enc = BinaryDataEncoder(args.data)
        data_func = enc.get_next_token

    if args.video:
        process_video(args.input, color=args.color, outpath=args.output, data_gen=data_func)
    else:
        process(args.input, color=args.color, outpath=args.output, data_gen=data_func)

