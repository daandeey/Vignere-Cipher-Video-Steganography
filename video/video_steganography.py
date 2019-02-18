from . import binary as bin
import cv2
import numpy as np

offset = 100
FRAME_RANDOM_SIGN = "fr"
FRAME_SEQ_SIGN = "fs"
PIXEL_RANDOM_SIGN = "pr"
PIXEL_SEQ_SIGN = "ps"
delimiter = "00000011"
seeder_limit = 1000000
DIR = "avi/"

def frame_extract(video):
    temp_folder = 'temp'
    try:
        os.mkdir(temp_folder)
    except OSError:
        remove(temp_folder)
        os.mkdir(temp_folder)

    vidcap = cv2.VideoCapture("data/"+str(video))
    count = 0

    while True:
        success, image = vidcap.read()
        if not success:
            break
        cv2.imwrite(os.path.join(temp_folder, "{:d}.png".format(count)), image)
        count += 1

def remove(path):
    """ param <path> could either be relative or absolute. """
    if os.path.isfile(path):
        os.remove(path)  # remove the file
    elif os.path.isdir(path):
        shutil.rmtree(path)  # remove dir and all contains
    else:
        raise ValueError("file {} is not a file or dir.".format(path))

def split2len(s, n):
    def _f(s, n):
        while s:
            yield s[:n]
            s = s[n:]
    return list(_f(s, n))

def embed(infile, outfile, frame_mode, pixel_mode, message):

    ltr = ""
    ltr = ltr + message
    bin_ltr = ""
    seq = None

    # Pass "wb" to write a new file, or "ab" to append
    with open(directory+outfile, "wb") as output_file:

        # Pass "wb" to write a new file, or "ab" to append
        with open(directory+infile, "rb") as input_file:
            # Write text or bytes to the file
            data = bytearray(avi_file.read())


            if (frame_mode == FRAME_SEQ_SIGN):
                if (pixel_mode == PIXEL_SEQ_SIGN):
                
                
                else:
            else:
                if(pixel_mode == PIXEL_SEQ_SIGN):
                
                
                
                else:


            if (sign==acak_sign):
                seeder = 0
                for c in message:
                    seeder = (seeder + ord(c))%seeder_limit

                starting_point = offset+(len(acak_sign)+len(str(seeder)))*8+2*len(delimiter)
                seq = generateIndexRandom(message, seeder, starting_point, len(data))

            if (sign==acak_sign):
                bin_ltr = bin.text_to_bits(acak_sign) + delimiter
                bin_ltr = bin_ltr + bin.text_to_bits(str(seeder)) + delimiter
            else:
                bin_ltr = bin.text_to_bits(seq_sign) + delimiter
            bin_ltr = bin_ltr + bin.text_to_bits(ltr) + delimiter

            if (sign==acak_sign):
                for i in range(offset, starting_point):
                    data[i] = bin.setLSB(data[i], int(bin_ltr[i-offset]))
                
                for i in range(0,len(seq)):
                    data[seq[i]] = bin.setLSB(data[seq[i]], int(bin_ltr[starting_point-offset+i]))
                
            else:
                for i in range(0,len(bin_ltr)):
                    idx = offset+i
                    data[idx] = bin.setLSB(data[idx], int(bin_ltr[i])) 

            binary_file.write(data)
