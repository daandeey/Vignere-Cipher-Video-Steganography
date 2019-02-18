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

acak_sign = "ak"
seq_sign = "sk"
offset = 100
ltr = ""
len_ltr = 112
i = 0
delimiter = "00000011"
found = False
sign = ""

# Pass "wb" to write a new file, or "ab" to append
with open("wav/makan.wav", "rb") as wav_file:
    # Write text or bytes to the file
    data = bytearray(wav_file.read())
    for k in range(16,24):    
        sign = sign + str(data[offset+k] & 1)
    #print(sign)

    if (sign == delimiter):
        sign = ""
        for k in range(0,16):    
            sign = sign + str(data[offset+k] & 1)
        sign = text_from_bits(sign)
    
    if (sign == seq_sign):
        start = (len(seq_sign)+1)*8
        i = start
        while not found:
            take = data[offset+i] & 1
            ltr = ltr + str(take)
            if ((i-7)%8==0 and i!=start):
                idx_start = i-7-start 
                idx_end = i+1-start
                print(ltr[idx_start:idx_end])
                print(text_from_bits(ltr[idx_start:idx_end]))
                if (ltr[idx_start:idx_end]==delimiter):
                    found = True
            i = i + 1
            if (i == 5000):
                break
    else:
        print("steganografi acak")
        idx = len(acak_sign)*8+len(delimiter)+offset
        count = 1
        timer = 0
        take = ""
        turn = 0
        while not found:
            #print(count)
            #print(idx)
            take = take + str(data[idx] & 1)
            #print(take[0])
            if (count == 8):
                #print(8*turn)
                #print(take[8*turn:8*turn+8])
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
  
        seeder = int(text_from_bits(take[0:idx]))
        random.seed(seeder)
        found = False
        count = 1
        turn = 0
        message = ""
        #print(seeder)
        #print(offset+(len(acak_sign)+len(str(seeder)))*8+2*len(delimiter), len(data))
        #print("iterasi")
        while not found:
            index = random.randint(offset+(len(acak_sign)+len(str(seeder)))*8+2*len(delimiter), len(data))
            #print(index)
            message = message + str(data[index] & 1)
            #print(message)
            if (count == 8):
                count = 0
                #print(message[8*turn:8*turn+8])
                #print(text_from_bits(message[8*turn:8*turn+8]))
                if (message[8*turn:8*turn+8]==delimiter):
                    found = True
                turn = turn + 1
            count = count + 1
        print("hasil pesan")
        print(text_from_bits(message[0:8*(turn-1)]))

if (ltr!=""):
    print(text_from_bits(ltr[0:len(ltr)-8]))