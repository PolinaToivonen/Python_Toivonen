def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    n = int()
    m = int()
    if len(keyword) < len(plaintext):
        for j in range(len(plaintext)-len(keyword)):
            keyword += keyword[j]
    for i in range(len(plaintext)):
        n = ord(plaintext[i])
        m = ord(keyword[i])
        if (n > 64) and (n < 91):
            if (m - 65 + n) < 91:
                ciphertext += chr(m - 65 + n)
            else:
                ciphertext += chr((m - 65 + n) % 91 + 65)
        else:
            if (m - 97 + n) < 123:
                ciphertext += chr(m - 97 + n)
            else:
                ciphertext += chr((m - 97 + n) % 97 + 97)
    return ciphertext


def decrypt_vigenere(cipehrtext: str, keyword: str) -> str:
    """
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    n = int()
    m = int()
    if len(keyword) < len(cipehrtext):
        for j in range(len(cipehrtext)-len(keyword)):
            keyword += keyword[j]
    for i in range(len(cipehrtext)):
        n = ord(cipehrtext[i])
        m = ord(keyword[i])
        if (n > 64) and (n < 91):
            if n >= m:
                plaintext += chr(n - m + 65)
            else:
                plaintext += chr(91 - (m - n))
        else:
            if n >= m:
                plaintext += chr(n - m + 97)
            else:
                plaintext += chr(91 - (m-n))
    return plaintext
