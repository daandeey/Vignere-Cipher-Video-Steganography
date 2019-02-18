'''
Bit Manipulation
1) Bin | 1: Membuat LSB menjadi angka 1
2) Bin & 1: Mendapatkan nilai LSB
'''
import binascii
import random

def text_to_bits(text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int(binascii.hexlify(text.encode(encoding, errors)), 16))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

def text_from_bits(bits, encoding='utf-8', errors='surrogatepass'):
    n = int(bits, 2)
    return int2bytes(n).decode(encoding, errors)

def int2bytes(i):
    hex_string = '%x' % i
    n = len(hex_string)
    return binascii.unhexlify(hex_string.zfill(n + (n & 1)))

offset = 100

def setLSB(data, binary):
    return (data & ~1) | binary

def generateIndexRandom(message, seeder, start, limit):
    
    index_list = []
    random.seed(seeder)
    for c in message:
        for k in range(0, 8):
            index_list.append(random.randint(start, limit))

    for k in range(0, 8):
        index_list.append(random.randint(start, limit))
    
    return index_list

acak_sign = "ak"
seq_sign = "sk"
ltr = ""
sign = acak_sign
message = "poster nih;(!"
delimiter = "00000011"
ltr = ltr + message
bin_ltr = ""
seq = None
seeder_limit = 1000000
#bin_ltr = ''.join(format(ord(x), 'b') for x in st)

# Pass "wb" to write a new file, or "ab" to append
with open("wav/makan.wav", "wb") as binary_file:

    # Pass "wb" to write a new file, or "ab" to append
    with open("wav/cat-purr.wav", "rb") as wav_file:
        # Write text or bytes to the file
        data = bytearray(wav_file.read())
        if (sign==acak_sign):
            print("penyisipan acak")
            seeder = 0
            for c in message:
                seeder = (seeder + ord(c))%seeder_limit

            starting_point = offset+(len(acak_sign)+len(str(seeder)))*8+2*len(delimiter)
            seq = generateIndexRandom(message, seeder, starting_point, len(data))

            bin_ltr = text_to_bits(acak_sign) + delimiter
            bin_ltr = bin_ltr + text_to_bits(str(seeder)) + delimiter
            bin_ltr = bin_ltr + text_to_bits(ltr) + delimiter

            if (sign==acak_sign):
                for i in range(offset, starting_point):
                    data[i] = setLSB(data[i], int(bin_ltr[i-offset]))
                
                #print("hasil sisipan")
                #print(len(text_to_bits(str(seeder)))+8)
                #for i in range(0,len(text_to_bits(str(seeder)))+8):
                    #print(i+24+offset)
                    #print(data[i+24+offset] & 1)
                for i in range(0,len(seq)):
                    data[seq[i]] = setLSB(data[seq[i]], int(bin_ltr[starting_point-offset+i]))
                
            else:
                 for i in range(0,len(bin_ltr)):
                    if (sign==acak_sign):
                        idx = offset+seq[i]
                    else:
                        idx = offset+i
                    data[idx] = (data[idx] & ~1) | int(bin_ltr[i])

            #print(seeder)
            #print(text_to_bits(str(seeder)))
            #print("\n")
            #print(bin_ltr[24:24+len(text_to_bits(str(seeder)))+8])
        binary_file.write(data)
        #print(seq)
        #print(seeder)