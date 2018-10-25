def encrypt_caesar(plaintext: str) -> str:
    """
    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ""
    n = int()
    b = ord('a')
    c = ord('A')
    d = ord('X')
    e = ord('x')
    f = ord('z')
    g = ord('Z')
    for i in range(len(plaintext)):
        n = ord(plaintext[i])
        if ((n >= c) and (n <= g)) or ((n >= b) and (n <= f)):
            if ((n >= d) and (n <= g)) or ((n >= e) and (n <= f)):
                if (n >= d) and (n <= g):
                    ciphertext += chr((ord(plaintext[i])) % d + c)
                else:
                    ciphertext += chr((ord(plaintext[i])) % e + b)
            else:
                ciphertext += chr(3 + ord(plaintext[i]))
        else:
            ciphertext += plaintext[i]
    return ciphertext


def decrypt_caesar(cipehrtext: str) -> str:
    """
    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ""
    n = int()
    b = ord('a')
    c = ord('A')
    d = ord('X')
    e = ord('x')
    f = ord('z')
    g = ord('Z')
    k = ord('C')
    m = ord('c')
    for i in range(len(cipehrtext)):
        n = ord(cipehrtext[i])
        if ((n >= c) and (n <= g)) or ((n >= b) and (n <= f)):
            if ((n >= c) and (n <= k)) or ((n >= b) and (n <= m)):
                plaintext += chr((ord(cipehrtext[i])) % c + d)
            else:
                plaintext += chr(ord(cipehrtext[i]) - 3)
        else:
            plaintext += cipehrtext[i]
    return plaintext
