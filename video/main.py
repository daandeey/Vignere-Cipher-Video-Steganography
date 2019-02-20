import os
import cv2
from subprocess import call,STDOUT
from binary import *
from PIL import Image
import shutil
from cipher import *
import random

def split2len(s, n):
    def _f(s, n):
        while s:
            yield s[:n]
            s = s[n:]
    return list(_f(s, n))

file_video = input("masukkan nama file video: ")
file_text = input("masukkan nama file text yang akan disembunyikan: ")
LSB_BIT = int(input("masukkan bit LSB yang ingin dipakai (1 atau 2): "))
print("Mode penyisipan")
print("11 - frame sekuensial, piksel sekuensial")
print("12 - frame sekuensial, piksel acak")
print("21 - frame acak, piksel sekuensial")
print("22 - frame acak, piksel acak")
hide_code = int(input("masukkan mode penyisipan: "))
cipher_key = input("masukkan kunci untuk enkripsi file: ")

# Check file video
try:
    open(file_video)
except IOError:
    print("-----------------------")
    print("tidak ada file")
    exit()

# Extract image
temp_folder = 'temp'
try:
    os.mkdir(temp_folder)
except OSError:
    shutil.rmtree(temp_folder)
    os.mkdir(temp_folder)

vidcap = cv2.VideoCapture(file_video)
count = 0

while True:
    success, image = vidcap.read()
    if not success:
        break
    cv2.imwrite(os.path.join(temp_folder, "{:d}.png".format(count)), image)
    count += 1

# Extract mp3
call(["ffmpeg", "-i", str(file_video), "-q:a", "0", "-map", "a", "temp/audio.mp3", "-y"], stdout=open(os.devnull, "w"), stderr=STDOUT, shell=True)

# Reading file
filename, file_ext = os.path.splitext(file_text)
text_open = open(file_text, "rb")
text_to_hide = VigenereCipherExtendedEncrypt(cipher_key,repr(text_open.read()))
bits_to_hide = text_to_bits(text_to_hide)
#print(len(bits_to_hide))

# Check if file > max_payload
frame_check = Image.open("temp/0.png")
width, height = frame_check.size
#print(str(width)+"/"+str(height))
max_payload = width*height*LSB_BIT*count-1*3
max_payload_per_frame = width*height*LSB_BIT*3
if len(bits_to_hide) > max_payload:
    print("-----------------------")
    print("file tidak dapat diproses (terlalu besar)")
    exit()

# Create seed for random pixel and random frame
seed = 0
for c in cipher_key:
    seed += ord(c)
random.seed(seed)
print(seed)

# Put file description into frame
file_size = len(bits_to_hide)
file_description = text_to_bits(str(hide_code) + "-" + str(file_ext) + "-" + str(file_size))
frame = Image.open(str(temp_folder)+"/"+str(0)+".png")
width, height = frame.size
encoded = frame.copy()
bit_index = 0
for row in range(height):
    for col in range(width):
        r,g,b = frame.getpixel((col,row))
        if bit_index > len(file_description)-1:
            r_new = r
            g_new = g
            b_new = b
        else:
            r_new = setLSB(r,int(file_description[bit_index]))
            bit_index += 1
            if bit_index <= len(file_description)-1:
                g_new = setLSB(g,int(file_description[bit_index]))
                bit_index += 1
            else:
                g_new = g
            if bit_index <= len(file_description)-1:
                b_new = setLSB(b,int(file_description[bit_index]))
                bit_index += 1
            else:
                b_new = b
        encoded.putpixel((col,row),(r_new,g_new,b_new))
if encoded:
    encoded.save(str(temp_folder)+"/"+str(0) + ".png")

# Put text bits into frame
if hide_code == 11:
    bits_to_hide_chopped = split2len(bits_to_hide,max_payload_per_frame)
    frame_index = 1
    for bits in bits_to_hide_chopped:
        frame = Image.open(str(temp_folder)+"/"+str(frame_index)+".png")
        width, height = frame.size
        encoded = frame.copy()
        bit_index = 0
        for row in range(height):
            for col in range(width):
                r,g,b = frame.getpixel((col,row))
                if bit_index > len(bits)-1:
                    r_new = r
                    g_new = g
                    b_new = b
                else:
                    r_new = setLSB(r,int(bits[bit_index]))
                    bit_index += 1
                    if bit_index <= len(bits)-1:
                        g_new = setLSB(g,int(bits[bit_index]))
                        bit_index += 1
                    else:
                        g_new = g
                    if bit_index <= len(bits)-1:
                        b_new = setLSB(b,int(bits[bit_index]))
                        bit_index += 1
                    else:
                        b_new = b
                encoded.putpixel((col,row),(r_new,g_new,b_new))
        if encoded:
            encoded.save(str(temp_folder)+"/"+str(frame_index) + ".png",compress_level=0)
        frame_index += 1
elif hide_code == 12:
    bits_to_hide_chopped = split2len(bits_to_hide,max_payload_per_frame)
    frame_index = 1
    for bits in bits_to_hide_chopped:
        frame = Image.open(str(temp_folder)+"/"+str(frame_index)+".png")
        width, height = frame.size
        encoded = frame.copy()
        bit_index = 0
        while(bit_index <= len(bits)-1):
            row = random.randint(0,height-1)
            col = random.randint(0,width-1)
            r,g,b = frame.getpixel((col,row))
            r_new = setLSB(r,int(bits[bit_index]))
            bit_index += 1
            if bit_index <= len(bits)-1:
                g_new = setLSB(g,int(bits[bit_index]))
                bit_index += 1
            else:
                g_new = g
            if bit_index <= len(bits)-1:
                b_new = setLSB(b,int(bits[bit_index]))
                bit_index += 1
            else:
                b_new = b
            encoded.putpixel((col,row),(r_new,g_new,b_new))
        if encoded:
            encoded.save(str(temp_folder)+"/"+str(frame_index) + ".png",compress_level=0)
        frame_index += 1    
elif hide_code == 21:
    bits_to_hide_chopped = split2len(bits_to_hide,max_payload_per_frame)
    frame_index = random.randint(1,count-1)
    for bits in bits_to_hide_chopped:
        frame = Image.open(str(temp_folder)+"/"+str(frame_index)+".png")
        width, height = frame.size
        encoded = frame.copy()
        bit_index = 0
        for row in range(height):
            for col in range(width):
                r,g,b = frame.getpixel((col,row))
                if bit_index > len(bits)-1:
                    r_new = r
                    g_new = g
                    b_new = b
                else:
                    r_new = setLSB(r,int(bits[bit_index]))
                    bit_index += 1
                    if bit_index <= len(bits)-1:
                        g_new = setLSB(g,int(bits[bit_index]))
                        bit_index += 1
                    else:
                        g_new = g
                    if bit_index <= len(bits)-1:
                        b_new = setLSB(b,int(bits[bit_index]))
                        bit_index += 1
                    else:
                        b_new = b
                encoded.putpixel((col,row),(r_new,g_new,b_new))
        if encoded:
            encoded.save(str(temp_folder)+"/"+str(frame_index) + ".png",compress_level=0)
        frame_index = random.randint(1,count-1)
else:
    bits_to_hide_chopped = split2len(bits_to_hide,max_payload_per_frame)
    frame_index = random.randint(1,count-1)
    for bits in bits_to_hide_chopped:
        frame = Image.open(str(temp_folder)+"/"+str(frame_index)+".png")
        width, height = frame.size
        encoded = frame.copy()
        bit_index = 0
        while(bit_index <= len(bits)-1):
            row = random.randint(0,height-1)
            col = random.randint(0,width-1)
            r,g,b = frame.getpixel((col,row))
            r_new = setLSB(r,int(bits[bit_index]))
            bit_index += 1
            if bit_index <= len(bits)-1:
                g_new = setLSB(g,int(bits[bit_index]))
                bit_index += 1
            else:
                g_new = g
            if bit_index <= len(bits)-1:
                b_new = setLSB(b,int(bits[bit_index]))
                bit_index += 1
            else:
                b_new = b
            encoded.putpixel((col,row),(r_new,g_new,b_new))
        if encoded:
            encoded.save(str(temp_folder)+"/"+str(frame_index) + ".png",compress_level=0)
        frame_index = random.randint(1,count-1)

new_video_name = input("masukkan nama file video yang sudah disisipi: ")
call(["ffmpeg", "-i", "temp/%d.png" , "-vcodec", "png", "temp/"+str(new_video_name)+".mov", "-y"],stdout=open(os.devnull, "w"), stderr=STDOUT, shell=True)
call(["ffmpeg", "-i", "temp/"+str(new_video_name)+".mov", "-i", "temp/audio.mp3", "-codec", "copy","temp/enc-" + str(new_video_name)+".mov", "-y"],stdout=open(os.devnull, "w"), stderr=STDOUT, shell=True)
print("Encode Done!")

# decode text in frame
