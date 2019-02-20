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