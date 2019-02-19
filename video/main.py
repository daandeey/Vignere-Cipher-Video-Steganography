import os
import cv2
from subprocess import call,STDOUT
from binary import *
from PIL import Image
import shutil

file_video = input("masukkan nama file video: ")
file_text = input("masukkan nama file text yang akan disembunyikan: ")
LSB_BIT = int(input("masukkan bit LSB yang ingin dipakai (1 atau 2): "))

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
text_open = open(file_text, "r")
text_to_hide = repr(text_open.read())
bits_to_hide = text_to_bits(text_to_hide)
#print(len(bits_to_hide))

# Check if file > max_payload
frame_check = Image.open("temp/0.png")
width, height = frame_check.size
#print(str(width)+"/"+str(height))
max_payload = width*height*LSB_BIT*count*3
max_payload_per_frame = width*height*LSB_BIT*3
if len(bits_to_hide) > max_payload:
    print("-----------------------")
    print("file tidak dapat diproses (terlalu besar)")
    exit()

# Encrypt text


# Put text bits into frame
#hide_code = 11
bits_to_hide_chopped = split2len(bits_to_hide,max_payload_per_frame)
#print(len(bits_to_hide_chopped))

frame_index = 0
for bits in bits_to_hide_chopped:
    frame = Image.open(str(temp_folder)+"/"+str(frame_index)+".png")
    frame.save(str(temp_folder)+"/"+str(frame_index)+"_copy.png")
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
        encoded.save(str(temp_folder)+"/"+str(frame_index) + "_encoded.png")
    frame_index += 1

print("Encode Done!")

# decode text in frame
