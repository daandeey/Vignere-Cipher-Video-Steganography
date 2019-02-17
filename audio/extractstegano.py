import binascii

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

print(text_from_bits(ltr[0:len(ltr)-8]))