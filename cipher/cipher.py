# MATRIX GENERATOR FOR FULL VIGENERE
def FullMatrix():
    alpha = "abcdefghijklmnopqrstuvwxyz"
    random_num = [11, 23, 5, 14, 26, 22, 15, 2, 4, 13, 10, 7, 1, 19, 18, 12, 20, 8, 6, 21, 9, 16, 17, 24, 25, 3]
    fullmatrix = []

    for i in random_num:
        temp = alpha[i : ] + alpha[0 : i] 
        fullmatrix.append(list(temp))

    return fullmatrix

# VIGENERE CIPHER STANDARD
def VigenereCipherEncrypt(k, p):
    c = list(p)

    for i in range(0, len(p)):
        if p[i].isalpha():
            c[i] = chr((ord(p[i]) - 97 + ord(k[i % len(k)]) - 97) % 26 + 97)
    return "".join(c)

def VigenereCipherDecrypt(k, c):
    p = list(c)

    for i in range(0, len(c)):
        if p[i].isalpha():
            p[i] = chr((ord(c[i]) - ord(k[i % len(k)])) % 26 + 97)

    return "".join(p)

# VIGENERE CIPHER AUTO KEY
def AutoKeyVigenereCipherEncrypt(k, p):
    k = (k + p)[0:len(p)]
    c = list(p)

    for i in range(0, len(p)):
        if p[i].isalpha():
            c[i] = chr((ord(p[i]) - 97 + ord(k[i % len(k)]) - 97) % 26 + 97)

    return "".join(c)

def AutoKeyVigenereCipherDecrypt(k, c):
    p = list(c)

    for i in range(0, len(c)):
        if p[i].isalpha():
            p[i] = chr((ord(c[i]) - ord(k[i % len(k)])) % 26 + 97)
            k += p[i]
        else:
            k += ' '

    return "".join(p)

'''
# VIGENERE CIPHER RUNNING KEY
runningtext = ""

with open('running-key.txt') as inputs:
    for line in inputs:
        runningtext += line.replace(" ","").replace(".","").strip()
'''

def RunningKeyCipherEncrypt(k, p):
    k = (k + runningtext)[0:len(p)]
    c = list(p)

    for i in range(0, len(p)):
        if p[i].isalpha():
            c[i] = chr((ord(p[i]) - 97 + ord(k[i % len(k)]) - 97) % 26 + 97)

    return "".join(c)

def RunningKeyCipherDecrypt(k, c):
    k = (k + runningtext)[0:len(c)]
    
    p = list(c)

    for i in range(0, len(c)):
        if p[i].isalpha():
            p[i] = chr((ord(c[i]) - ord(k[i % len(k)])) % 26 + 97)

    return "".join(p)

# VIGENERE CIPHER FULL KEY
def FullKeyVigenereCipherEncrypt(k, p):
    m = FullMatrix()
    c = list(p)

    for i in range(0, len(p)):
        if p[i].isalpha():
            idx_i = ord(k[i % len(k)]) - 97
            idx_j = ord(p[i]) - 97
            c[i] = m[idx_i][idx_j]

    return "".join(c)
    
def FullKeyVigenereCipherDecrypt(k, c):
    m = FullMatrix()
    p = list(c)

    for i in range(0, len(c)):
        if p[i].isalpha():
            idx_key = ord(k[i % len(k)]) - 97
            idx_plain = m[idx_key].index(c[i])
            p[i] = chr(idx_plain + 97)

    return "".join(p)

# VIGENERE CIPHER EXTENDED
def VigenereCipherExtendedEncrypt(k, p):
    c = list(p)

    for i in range(0, len(p)):
        c[i] = chr((ord(p[i]) + ord(k[i % len(k)])) % 256)

    return "".join(c)

def VigenereCipherExtendedDecrypt(k, c):
    p = list(c)

    for i in range(0, len(c)):
        p[i] = chr((ord(c[i]) - ord(k[i % len(k)])) % 256)

    return "".join(p)

def PlayfairCipherEncrypt(k, p):
    p = p.replace("j","i")
    matrix_k = KeyToMatrix(k)
    bigraf = PlaintextToBigraf(p)
    c = []
    for elem in bigraf:
        i1, j1 = FindPosition(matrix_k, elem[0])
        i2, j2 = FindPosition(matrix_k, elem[1])
        if i1 == i2:
            if j1 == 4:
                j1 = -1
            if j2 == 4:
                j2 = -1
            c.append(matrix_k[i1][j1 + 1])
            c.append(matrix_k[i2][j2 + 1])
        elif j1 == j2:
            if i1 == 4: 
                i1 = -1
            if i2 == 4:
                i2 = -1
            c.append(matrix_k[i1 + 1][j1])
            c.append(matrix_k[i2 + 1][j2])
        else:
            c.append(matrix_k[i1][j2])
            c.append(matrix_k[i2][j1])

    return "".join(c)
    
def PlayfairCipherDecrypt(k, c):
    matrix_k = KeyToMatrix(k)
    bigraf = CiphertextToBigraf(c)
    p = []
    for elem in bigraf:
        i1, j1 = FindPosition(matrix_k, elem[0])
        i2, j2 = FindPosition(matrix_k, elem[1])
        if i1 == i2:
            if j1 == 0:
                j1 = 5
            if j2 == 0:
                j2 = 5
            p.append(matrix_k[i1][j1 - 1])
            p.append(matrix_k[i2][j2 - 1])
        elif j1 == j2:
            if i1 == 0: 
                i1 = 5
            if i2 == 0:
                i2 = 5
            p.append(matrix_k[i1 - 1][j1])
            p.append(matrix_k[i2 - 1][j2])
        else:
            p.append(matrix_k[i1][j2])
            p.append(matrix_k[i2][j1])
    
    p = "".join(p).replace('x',"")
    return p

def PlaintextToBigraf(p):
    p = p.replace(" ","")
    p = list(p)

    i = 0
    #if both letters are same, add 'x'
    while i < len(p) - 1:
        if p[i] == p[i + 1]:
            p.insert(i + 1, 'x')
        i += 2

    #if the length is odd, add 'x' at the end
    if len(p) % 2 != 0:
        p.append('x')

    bigraf = [p[i:i+2] for i in range(0, len(p), 2)]
    
    return bigraf

def CiphertextToBigraf(c):
    c = c.replace(" ","")
    c = list(c)

    bigraf = [c[i:i+2] for i in range(0, len(c), 2)]    
    return bigraf

def FindPosition(matrix, letter):
    for i in range(5):
        for j in range(5):
            if matrix[i][j] == letter:
                return i,j

def KeyToMatrix(k):
    k = k.replace(" ","")
    k += "abcdefghijklmnopqrstuvwxyz"
    new_k = ""
    matrix_k = []

    #new_k is key contains letter from a to z, except j
    for letter in k:
        if letter not in new_k and letter != 'j' :
            new_k += letter

    #matrix_k is a 5x5 matrix containing the key
    matrix_k = [new_k[i:i+5] for i in range(0, len(new_k), 5)]

    return matrix_k
    
def ReadFile(filename):
    if (filename[-4:0] == '.txt'):
        with open(filename, "r") as f:
            return f.read()
    else:    
        with open(filename, "rb") as f:
            text = ''
            while 1:
                byte_s = f.read(1)
                if not byte_s:
                    break
                c = str(byte_s, 'ISO-8859-1')
                text += c
            return text

def WriteFile(string, filename):
    if (filename[-4:0] == '.txt'):
        with open(filename, "w") as f:
            f.write(string)
    else:
        with open(filename, "wb") as f:
            byte_arr = []
            for c in string:
                byte_arr.append(ord(c))
            binary = bytearray(byte_arr)
            f.write(binary)

def CiphertextToPentagraf(c):
    return " ".join([c[i:i+5] for i in range(0, len(c), 5)])

def CiphertextWithoutSpaces(c):
    return c.replace(" ","")


if __name__ == "__main__":
    valid = False
    
    while(not valid):  
        print("TUGAS KECIL IF4020 KRIPTOGRAFI")
        print("By Dandy Arif Rahman")
        print("13516086")
        

        while(not valid):
            print("Pilih cara input plaintext")
            print("1. Keyboard")
            print("2. File Eksternal")
            opt = int(input("Mohon masukkan pilihan: "))
            if (opt == 1):
                p = str(input("Mohon masukkan plaintext: "))
                k = str(input("Mohon masukkan key: "))
                break
            elif (opt == 2):
                fn = str(input("Mohon masukan nama file: "))
                p = ReadFile(fn)
                k = str(input("Mohon masukkan key: "))
                break
            else:
                print("Pilihan anda salah\n")

        while(not valid):
            print("Pilih metode enkripsi")
            print("1. Vigenere (26 Character)")
            print("2. Full Vigenere (26 Character)")
            print("3. Auto Key Vigenere (26 Character)")
            print("4. Running Key Vigenere (26 Character)")
            print("5. Vigenere (ASCII)")
            print("6. Playfair (26 Character)")
            opt = int(input("Mohon masukkan pilihan: "))
            if (opt == 1):
                c = VigenereCipherEncrypt(k, p)
                p = VigenereCipherDecrypt(k, c)
                break
            elif (opt == 2):
                c = FullKeyVigenereCipherEncrypt(k, p)
                p = FullKeyVigenereCipherDecrypt(k, c)
                break
            elif (opt == 3):
                c = AutoKeyVigenereCipherEncrypt(k, p)
                p = AutoKeyVigenereCipherDecrypt(k, c)
                break
            elif (opt == 4):
                c = RunningKeyCipherEncrypt(k, p)
                p = RunningKeyCipherDecrypt(k, c)
                break
            elif (opt == 5):
                c = VigenereCipherExtendedEncrypt(k, p)
                p = VigenereCipherExtendedDecrypt(k, c)
                break
            elif (opt == 6):
                c = PlayfairCipherEncrypt(k, p)
                p = PlayfairCipherDecrypt(k, c)
                break
            else:
                print("Pilihan anda salah\n")

        while(not valid):
            print("\nPesan berhasil dienkripsi!\n")
            print("Mohon pilih metode output")
            print("1. Tampilkan pada layar dalam format original")
            print("2. Tampilkan pada layar dalam format tanpa spasi")
            print("3. Tampilkan pada layar dalam format pentagraf")
            print("4. Output ke dalam file")
            opt = int(input("Mohon masukkan pilihan: "))
            if (opt == 1):
                print('Hasil Enkripsi: ' + c)
                print('Hasil Dekripsi: ' + p)
                break
            elif (opt == 2):
                print('Hasil Enkripsi: ' + CiphertextWithoutSpaces(c))
                print('Hasil Dekripsi: ' + p)
            elif (opt == 3):
                print('Hasil Enkripsi: ' + CiphertextToPentagraf(c))
                print('Hasil Dekripsi: ' + p)
            elif (opt == 4):
                fn = str(input("Mohon masukkan nama file: "))
                WriteFile(p, fn)
                break
            else:
                print("Pilihan anda salah\n")

        opt = str(input("Apakah Anda ingin melakukan enkripsi lagi? (y/n) :"))
        if (opt == 'y'):
            pass
        else:
            break
    
    print('\nTerimakasih telah menggunakan program saya')
    print('\nDandy Arif Rahman\n13516086')
            

    # k = "nama pacarku wati"
    # p = "texmxuix ibu nanti malam"

    # c = PlayfairCipherEncrypt(k, p)
    # print(c)
    # p = PlayfairCipherDecrypt(k, c)
    # print(p)



    # s1 = ReadFile('wallpaper.jpg')
    # k = 'd'
    # s2 = VigenereCipherExtendedEncrypt(k, s1)
    # WriteFile(s2, "wallpaper2.jpg")
    # s3 = VigenereCipherExtendedDecrypt(k, s2)
    # WriteFile(s3, "wallpaper3.jpg")

    # k = 'dandy'
    # p = 'nama saya dandy arif rahman umur saya dua puluh tahun 32456789 *&^%&*^^$'
    # print('FULL')
    # c = FullKeyVigenereCipherEncrypt(k, p)
    # print(c)
    # print(FullKeyVigenereCipherDecrypt(k, c))
    
    # print('STANDARD')
    # c = VigenereCipherEncrypt(k, p)
    # print(c)
    # print(VigenereCipherDecrypt(k, c))
    
    # print('AUTO')
    # c = AutoKeyVigenereCipherEncrypt(k,p)
    # print(c)
    # print(AutoKeyVigenereCipherDecrypt(k, c))
    
    # print('RUNNING')
    # c = RunningKeyCipherEncrypt(k,p)
    # print(c)
    # print(RunningKeyCipherDecrypt(k, c))
    
    # print('EXTENDED')
    # c = VigenereCipherExtendedEncrypt(k,p)
    # print(c)
    # print(VigenereCipherExtendedDecrypt(k, c))