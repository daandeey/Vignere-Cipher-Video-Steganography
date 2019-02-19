from audio import steganography as aud
from audio import binary as bin
from cipher import cipher as cp

import pyaudio  
import wave
import sys
import vlc
import time
import os

directory = "text/"
audio_dir = "wav/"

def clear_screen():
    os.system('cls')
    os.system('clear')

def first_menu():
    print("======================")
    print("Aplikasi Steganografi")
    print("======================")
    print("1: Penyisipan pesan")
    print("2: Ekstraksi pesan")
    print("3: Keluar")
    print("Pilih (1/2/3): ", end='')

def embed_menu():
    print("==================")
    print("Penyisipan Pesan")
    print("==================")
    print("1: Audio")
    print("2: Video")
    print("3: Kembali")
    print("Pilih (1/2/3): ", end='')

def embed_audio_menu(fileaudio, filepesan):
    print("==========================================")
    print("Penyisipan Pesan ke Audio")
    print("File audio: ", fileaudio)
    print("File pesan: ", filepesan)
    print("==========================================")
    print("1: Mainkan file audio")
    print("2: Penyisipan pesan terurut")
    print("3: Penyisipan pesan secara acak")
    print("4: Ganti file audio")
    print("5: Ganti file pesan")
    print("6: Kembali")
    print("Pilih (1/2/3/4): ", end='')

def extract_audio_menu(fileaudio):
    print("==========================================")
    print("Ekstrasi Pesan dari Audio")
    print("File audio: ", fileaudio)
    print("==========================================")
    print("1: Mainkan file audio")
    print("2: Ekstraksi pesan ke file eksternal")
    print("3: Ekstraksi pesan langsung")
    print("4: Ganti file audio")
    print("5: Kembali")
    print("Pilih (1/2/3/4): ", end='')

def play_audio(fileaudio):
    player = vlc.MediaPlayer(audio_dir+fileaudio)
    player.play()

if __name__ == "__main__":

    finished = False
    
    while(not finished):
        clear_screen()
        first_menu()
        choice = input()

        if (choice=="1"):
            while(not finished):
                clear_screen()
                embed_menu()
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

                    while(not finished):
                        clear_screen()
                        embed_audio_menu(fileaudio, filepesan)
                        choice = input()

                        if (choice=="1"):
                            play_audio(fileaudio)
                        elif (choice=="3"):
                            clear_screen()
                            print("=======================================")
                            print("Penyisipan Pesan ke Audio Secara Acak")
                            print("=======================================")
                            print("Apakah perlu dienkripsi? (y/n): ", end='')
                            choice = input()
                            key = None
                            sign = aud.acak_sign
                            if (choice=='y'):
                                print("Masukkan kunci untuk enkripsi dan pengacakan: ", end='')
                                key = input()
                                pesan = cp.VigenereCipherExtendedEncrypt(key, pesan)
                                sign = aud.acak_enc
                            else:
                                print("Masukkan kunci untuk pengacakan: ", end='')
                                key = input()
                            print("Simpan hasil ke file: ", end='')
                            out = input()
                            aud.embed(fileaudio, out, sign, pesan, key)
                            print("Penyisipan pesan berhasil!!!")
                            print("Mainkan hasil steganografi? (y/n): ", end='')
                            clear_screen()
                            choice = input()
                            if (choice=="y"):
                                play_audio(out)
                                print("\nTekan apapun untuk lanjut...", end='')
                                choice = input()
                        elif (choice=="2"):
                            clear_screen()
                            print("===================================")
                            print("Penyisipan Pesan Terurut ke Audio")
                            print("===================================")
                            print("Apakah perlu dienkripsi? (y/n): ", end='')
                            choice = input()
                            sign = aud.seq_sign
                            key = None
                            if (choice=='y'):
                                sign = aud.seq_enc
                                print("Masukkan kunci untuk enkripsi: ", end='')
                                key = input()
                                pesan = cp.VigenereCipherExtendedEncrypt(key, pesan)
                            print("Simpan hasil ke file: ", end='')
                            out = input()
                            aud.embed(fileaudio, out, sign, pesan, key)
                            print("Penyisipan pesan berhasil!!!")
                            print("Mainkan hasil steganografi? (y/n): ", end='')
                            choice = input()
                    
                            if (choice=="y"):
                                clear_screen()
                                play_audio(out)
                                print("\nTekan apapun untuk lanjut...", end='')
                                choice = input()
                        elif(choice=="6"):
                            finished = True

                    finished = False
                elif(choice=="3"):
                    finished = True
            finished = False

        elif (choice=="2"):
            print("Catatan: audio diambil dari folder wav")
            print("Masukkan file audio: ", end='')
            fileaudio = input()

            while(not finished):
                clear_screen()
                extract_audio_menu(fileaudio)
                choice = input()

                if (choice=="1"):
                    clear_screen()
                    play_audio(fileaudio)
                    print("\nTekan apapun untuk lanjut...")
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
                        clear_screen()
                        print("Ekstraksi pesan berhasil!!!")
                        print("Pesan: ")
                        print(hasil)
                        print("\nTekan apapun untuk lanjut...", end='')
                        choice = input()
                    else:
                        writing = open(directory+filepesan, "w")
                        writing.write(hasil)
                        writing.close() 
                        print("Ekstraksi pesan berhasil disimpan di "+filepesan+"!!!")
                
                if (choice=="4"):
                    finished = True
            finished = False
        elif (choice=="3"):
            finished = True
        