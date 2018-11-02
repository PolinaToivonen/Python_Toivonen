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
    for i in range(len(plaintext)):
        if ('A' <= plaintext[i] <= 'Z') or ('a' <= plaintext[i] <= 'z'):
            if ('X' <= plaintext[i] <= 'Z') or ('x' <= plaintext[i] <= 'z'):
                if (plaintext[i] >= 'X') and (plaintext[i] <= 'Z'):
                    ciphertext += chr((ord(plaintext[i])) % ord('Х') + ord('А'))
                else:
                    ciphertext += chr((ord(plaintext[i])) % ord('x') + ord('а'))
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
    for i in range(len(cipehrtext)):
        if ('A' <= cipehrtext[i] <= 'Z') or ('a' <= cipehrtext[i] <= 'z'):
            if ('A' <= cipehrtext[i] <= 'C') or ('a' <= cipehrtext[i] <= 'c'):
                plaintext += chr((ord(cipehrtext[i])) % ord('А') + ord('X'))
            else:
                plaintext += chr(ord(cipehrtext[i]) - 3)
        else:
            plaintext += cipehrtext[i]
    return plaintext
