from . import binary as bin
from cipher import cipher as cp

import binascii
import random

offset = 100
acak_sign = "ak"
seq_sign = "sk"
acak_enc = "ae"
seq_enc = "se"
delimiter = "00000011"
seeder_limit = 1000000
directory = "wav/"

def generateIndexRandom(message, seeder, start, limit):
    
    index_list = []
    random.seed(seeder)
    for c in bin.text_to_bits(message):
        #for k in range(0, 8):
        index_list.append(random.randint(start, limit))

    for k in range(0, 8):
        index_list.append(random.randint(start, limit))
    
    return index_list

def embed(infile, outfile, sign, message):

    ltr = ""
    ltr = ltr + message
    bin_ltr = ""
    seq = None

    # Pass "wb" to write a new file, or "ab" to append
    with open(directory+outfile, "wb") as binary_file:

        # Pass "wb" to write a new file, or "ab" to append
        with open(directory+infile, "rb") as wav_file:
            # Write text or bytes to the file
            data = bytearray(wav_file.read())
            if (sign==acak_sign or sign==acak_enc):
                seeder = 0
                for c in message:
                    seeder = (seeder + ord(c))%seeder_limit

                starting_point = offset+(len(acak_sign)+len(str(seeder)))*8+2*len(delimiter)
                seq = generateIndexRandom(message, seeder, starting_point, len(data))
                
            if (sign==acak_sign or sign==acak_enc):
                if (acak_enc):
                    bin_ltr = bin.text_to_bits(acak_enc) + delimiter
                else:
                    bin_ltr = bin.text_to_bits(acak_sign) + delimiter
                bin_ltr = bin_ltr + bin.text_to_bits(str(seeder)) + delimiter
            else:
                if (sign==seq_sign):
                    bin_ltr = bin.text_to_bits(seq_sign) + delimiter
                else:
                    bin_ltr = bin.text_to_bits(seq_enc) + delimiter
            #print(ltr)
            bin_ltr = bin_ltr + bin.text_to_bits(ltr) + delimiter

            if (sign==acak_sign or sign==acak_enc):
                for i in range(offset, starting_point):
                    data[i] = bin.setLSB(data[i], int(bin_ltr[i-offset]))
                
                for i in range(0,len(seq)):
                    data[seq[i]] = bin.setLSB(data[seq[i]], int(bin_ltr[starting_point-offset+i]))
                
            else:
                for i in range(0,len(bin_ltr)):
                    idx = offset+i
                    data[idx] = bin.setLSB(data[idx], int(bin_ltr[i])) 

            binary_file.write(data)

def extract(filename, key):

    found = False
    ltr = ""
    i = 0
    sign = ""
    # Pass "wb" to write a new file, or "ab" to append
    with open(directory+filename, "rb") as wav_file:
        # Write text or bytes to the file
        data = bytearray(wav_file.read())
        for k in range(16,24):    
            sign = sign + str(data[offset+k] & 1)

        if (sign == delimiter):
            sign = ""
            for k in range(0,16):    
                sign = sign + str(data[offset+k] & 1)
            sign = bin.text_from_bits(sign)
        
        if (sign == seq_sign or sign == seq_enc):
            start = (len(seq_sign)+1)*8
            i = start
            while not found:
                take = data[offset+i] & 1
                ltr = ltr + str(take)
                if ((i-7)%8==0 and i!=start):
                    idx_start = i-7-start 
                    idx_end = i+1-start
                    if (ltr[idx_start:idx_end]==delimiter):
                        found = True
                i = i + 1
            hasil = bin.text_from_bits(ltr[0:len(ltr)-8])
            if (sign==seq_enc):
                hasil = cp.VigenereCipherExtendedDecrypt(key, hasil)
            return hasil
        else:
            idx = len(acak_sign)*8+len(delimiter)+offset
            count = 1
            timer = 0
            take = ""
            turn = 0
            while not found:
                take = take + str(data[idx] & 1)
                if (count == 8):
                    if (take[8*turn:8*turn+8]==delimiter):
                        found = True
                        idx = 8*(turn-1)+7
                    count = 0
                    turn = turn + 1
                idx = idx + 1
                timer = timer + 1
                count = count + 1
                if (timer==50):
                    break
    
            seeder = int(bin.text_from_bits(take[0:idx]))
            random.seed(seeder)
            found = False
            count = 1
            turn = 0
            message = ""
            while not found:
                index = random.randint(offset+(len(acak_sign)+len(str(seeder)))*8+2*len(delimiter), len(data))
                message = message + str(data[index] & 1)
                if (count == 8):
                    count = 0
                    if (message[8*turn:8*turn+8]==delimiter):
                        found = True
                    turn = turn + 1
                count = count + 1
            #
            hasil = bin.text_from_bits(message[0:8*(turn-1)])
            #print(sign)
            if (sign == acak_enc):
                #print(sign)
                hasil = cp.VigenereCipherExtendedDecrypt(key, hasil) 
            return hasil

            