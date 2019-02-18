from . import binary as bin
import cv2
import numpy as np

# constants
CARRIER_DIR = "avi/"
FRAMES_DIR = "temp/"
FRAME_RANDOM_SIGN = "fr"
FRAME_SEQ_SIGN = "fs"
PIXEL_RANDOM_SIGN = "pr"
PIXEL_SEQ_SIGN = "ps"

def audio_extract(file_name):
    # audio is extracted using system call
    # ffmpeg -i data/chef.mp4 -q:a 0 -map a temp/audio.mp3 -y
    # 2>/dev/null for supressing the output from ffmpeg
    call(["ffmpeg", "-i", "data/" + str(file_name), "-q:a", "0", "-map", "a", "temp/audio.mp3", "-y"],stdout=open(os.devnull, "w"), stderr=STDOUT)

def merge_audio_and_frames(file_name):
    # audio and video are merged using system call
    # ffmpeg -i temp/%d.png -vcodec png data/video.mov
    call(["ffmpeg", "-i", "temp/%d.png" , "-vcodec", "png", "temp/video.mov", "-y"],stdout=open(os.devnull, "w"), stderr=STDOUT)
    # ffmpeg -i temp/video.mov -i temp/audio.mp3 -codec copy data/enc-chef.avi -y
    call(["ffmpeg", "-i", "temp/video.mov", "-i", "temp/audio.mp3", "-codec", "copy","data/enc-" + str(file_name)+".avi", "-y"],stdout=open(os.devnull, "w"), stderr=STDOUT)
       

def frame_extract(file_name):
    # frame_extract is to extract file in 'CARRIER_DIR/file_name' into frames
    # frames saved in 'FRAMES_DIR'
    
    temp_folder = 'temp'
    try:
        os.mkdir(temp_folder)
    except OSError:
        remove(temp_folder)
        os.mkdir(temp_folder)

    vidcap = cv2.VideoCapture("data/"+str(file_name))
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

def is_file_fit(carrier, file_to_be_hide):
    #is_file_fit return true if carrier can carry the file_to_be_hide
    fit = True



    return fit

def sequential_image_LSB(img, file):
    #img is the image file
    #file is the file that want to be hide

def random_image_LSB(img, file):
    #img is the image file
    #file is the file that want to be hide

def encode_frame_sequential(dir, file, opt):
    #dir is the frames directory
    #file is the file that want to be hide
    #opt is option, 'seq' for sequential, 'ran' for random 
    
    file_ext = 'txt'
    file_size = 1000

    #insert file_ext to frame
    
    #insert file_size to frame 
    
    #insert file to frame

    for chopped_file in file:
        for frame in frames:
            if (opt == 'seq'):
                sequential_image_LSB(frame, chopped_file)
            else:
                random_image_LSB(frame, chopped_file)
    #frames are inserted with file
    
def encode_frame_random(dir, file, opt):
    #dir is the frames directory
    #file is the file that want to be hide
    #opt is option, 'seq' for sequential, 'ran' for random 

    for chopped_file in file:
        for frame in frames:
            if (opt == 'seq'):
                sequential_image_LSB(frame, chopped_file)
            else:
                random_image_LSB(frame, chopped_file)
    #frames are inserted with file
    
def encode(infile, outfile, frame_mode, pixel_mode, file_to_be_hide):
    # infile is name of the input video file
    # outfile is name of the output video file
    # frame_mode is mode that how the frame gonna be steg; sequential or random
    # pixel_mode is mode that how the pixel gonna be steg; sequential or random
    # file_to_be_hide is name of the file that wanna be hide

    frame_extract(infile)
    audio_extract(infile)
    frames_dir = FRAMES_DIR

    if (frame_mode == FRAME_SEQ_SIGN):
        if (pixel_mode == PIXEL_SEQ_SIGN):
            encode_frame_sequential(frames_dir, file_to_be_hide, 'seq')
        
        else:
            encode_frame_sequential(frames_dir, file_to_be_hide, 'ran')
    else:
        if (pixel_mode == PIXEL_SEQ_SIGN):
            encode_frame_random(frames_dir, file_to_be_hide, 'seq')

        else:
            encode_frame_random(frames_dir, file_to_be_hide, 'ran')

    merge_audio_and_frames(infile)        

def decode(infile):
