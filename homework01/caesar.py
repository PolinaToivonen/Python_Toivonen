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
    for i in range(len(plaintext)):
        n = ord(plaintext[i])
        if ((n > 64) and (n < 91)) or ((n > 96) and (n < 123)):
            if ((n > 87) and (n < 91)) or ((n > 119) and (n < 123)):
                ciphertext += chr((ord(plaintext[i])) % 88 + 65)
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
    for i in range(len(cipehrtext)):
        n = ord(cipehrtext[i])
        if ((n > 64) and (n < 91)) or ((n > 96) and (n < 123)):
            if ((n > 64) and (n < 68)) or ((n > 97) and (n < 100)):
                plaintext += chr((ord(cipehrtext[i])) % 65 + 88)
            else:
                plaintext += chr(ord(cipehrtext[i]) - 3)
        else:
            plaintext += cipehrtext[i]
    return plaintext
