from audio import steganography as aud
from audio import binary as bin
from cipher import cipher as cp

directory = "text/"

print("========================================")
print("Aplikasi Steganografi")
print("1: Penyisipan pesan")
print("2: Ekstraksi pesan")
print("Pilih (1/2): ", end='') 
choice = input()

if (choice=="1"):
    print("========================================")
    print("Penyisipan Pesan")
    print("1: Audio")
    print("2: Video")
    print("3: Kembali")
    print("Pilih (1/2/3): ", end='')
    choice = input()
    if (choice=="1"):
        print("Catatan: audio diambil dari folder wav")
        print("Catatan: pesan diambil dari folder text")
        print("Masukkan file audio: ", end='')
        fileaudio = input()
        print("Masukkan file pesan: ", end='')
        filepesan = input()

        pesan = None
        with open(directory+filepesan, "rb") as wav_file:
            pesan = bytes(wav_file.read()).decode("utf-8") 

        print("========================================")
        print("File audio: ", fileaudio)
        print("File pesan: ", filepesan)
        print("1: Mainkan file audio")
        print("2: Penyisipan pesan terurut")
        print("3: Penyisipan pesan secara acak")
        print("4: Kembali")
        print("Pilih (1/2/3/4): ", end='')
        choice = input()

        if (choice=="3"):
            print("========================================")
            print("Penyisipan pesan ke audio secara acak")
            print("Apakah perlu dienkripsi? (y/n): ", end='')
            choice = input()
            key = None
            if (choice=='y'):
                print("Masukkan kunci: ", end='')
                key = input()
                pesan = cp.VigenereCipherExtendedEncrypt(key, pesan)
            print("Simpan hasil ke file: ", end='')
            out = input()
            aud.embed(fileaudio, out, aud.acak_sign, pesan)
            print("Penyisipan pesan berhasil!!!")
            print("Mainkan hasil steganografi? (y/n): ")
            print(aud.extract(out, key))
        elif (choice=="2"):
            print("========================================")
            print("Penyisipan pesan ke audio terurut")
            print("Apakah perlu dienkripsi? (y/n): ", end='')
            choice = input()
            sign = aud.seq_sign
            key = None
            if (choice=='y'):
                sign = aud.seq_enc
                print("Masukkan kunci: ", end='')
                key = input()
                pesan = cp.VigenereCipherExtendedEncrypt(key, pesan)
            print("Simpan hasil ke file: ", end='')
            out = input()
            aud.embed(fileaudio, out, sign, pesan)
            print("Penyisipan pesan berhasil!!!")
            print("Mainkan hasil steganografi? (y/n): ")
            print(aud.extract(out, key))

    elif (choice=="2"):
        print()

elif (choice=="2"):
    print("Catatan: audio diambil dari folder wav")
    print("Masukkan file audio: ", end='')
    fileaudio = input()
    print("File audio: ", fileaudio)
    print("1: Mainkan file audio")
    print("2: Ekstraksi pesan ke file eksternal")
    print("3: Ekstraksi pesan langsung")
    print("4: Kembali")
    print("Pilih (1/2/3/4): ", end='')
    choice = input()

    if (choice=="2" or choice=="3"):
        print("Apakah memerlukan kunci? (y/n): ", end='')
        confirm = input()
        key = None
        if (confirm=="y"):
            print("Masukkan kunci: ", end='')
            key = input()
    
    filepesan = ""
    if (choice=="2"):
        print("Simpan pesan pada file: ", end="")
        filepesan = input()

    if (choice=="2" or choice=="3"):
        hasil = aud.extract(fileaudio, key)
        
        if (choice=="3"):
            print("Ekstraksi pesan berhasil!!!")
            print("Pesan: ")
            print(hasil)
        else:
            writing = open(directory+filepesan, "w")
            writing.write(hasil)
            writing.close() 
            print("Ekstraksi pesan berhasil disimpan di "+filepesan+"!!!")
        