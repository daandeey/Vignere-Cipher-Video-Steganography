'''
Bit Manipulation
1) Bin | 1: Membuat LSB menjadi angka 1
2) Bin & 1: Mendapatkan nilai LSB
'''
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
'''
def text_to_bits(text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int.from_bytes(text.encode(encoding, errors), 'big'))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

def text_from_bits(bits, encoding='utf-8', errors='surrogatepass'):
    n = int(bits, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(encoding, errors) or '\0'
'''

offset = 100
ltr = "makanan enak!"
#bin_ltr = ''.join(format(ord(x), 'b') for x in st)
bin_ltr = text_to_bits(ltr)

print(bin_ltr)

# Pass "wb" to write a new file, or "ab" to append
with open("makan.wav", "wb") as binary_file:

    # Pass "wb" to write a new file, or "ab" to append
    with open("cat-purr.wav", "rb") as wav_file:
        # Write text or bytes to the file
        data = bytearray(wav_file.read())
        for i in range(0,len(bin_ltr)):
            data[offset+i] = (data[offset+i] & ~1) | int(bin_ltr[i])
        binary_file.write(data)
