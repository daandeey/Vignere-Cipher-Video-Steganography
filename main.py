from audio import steganography as aud

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
        #print("Catatan: pesan diambil dari folder in")
        print("Masukkan file audio: ", end='')
        fileaudio = input()
        print("Masukkan pesan: ", end='')
        pesan = input()
        #filepesan = input()

        print("========================================")
        print("File audio: ", fileaudio)
        print("Pesan: ", pesan)
        print("1: Mainkan file audio")
        print("2: Penyisipan pesan terurut")
        print("3: Penyisipan pesan secara acak")
        print("4: Kembali")
        print("Pilih (1/2/3/4): ", end='')
        choice = input()

        if (choice=="3"):
            print("========================================")
            print("Penyisipan pesan ke audio terurut")
            print("Apakah perlu dienkripsi? (y/n): ")
            print("Simpan hasil ke file: ", end='')
            out = input()
            aud.embed(fileaudio, out, aud.acak_sign, pesan)
            print("Penyisipan pesan berhasil!!!")
            print("Mainkan hasil steganografi? (y/n): ")
            print(aud.extract(out))
        elif (choice=="2"):
            print("========================================")
            print("Penyisipan pesan ke audio secara terurut")
            print("Apakah perlu dienkripsi? (y/n): ")
            print("Simpan hasil ke file: ", end='')
            out = input()
            aud.embed(fileaudio, out, aud.seq_sign, pesan)
            print("Penyisipan pesan berhasil!!!")
            print("Mainkan hasil steganografi? (y/n): ")
            print(aud.extract(out))

    elif (choice=="2"):
        print()

elif (choice=="2"):
    print("hello!")
'''

print("Masukkan kunci: ")
print("Masukkan file eksternal: ")
print("Simpan file audio dengan nama:")
print("Audio hasil sisipan pesan berhasil dibuat")
print("Mainkan hasil file audio? (y/n)")

print("Ekstraksi Pesan")
print("1: Audio")
print("2: Video")
print("3: Kembali")
print("Pilih (1/2/3): ")

print("File audio: ")
print("1: Mainkan file audio")
print("2: Ekstraksi pesan ke file eksternal")
print("3: Ekstraksi pesan langsung")
print("4: Kembali")
print("Pilih (1/2/3/4): ")
'''