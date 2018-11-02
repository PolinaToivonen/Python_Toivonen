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
    if len(keyword) < len(plaintext):
        for j in range(len(plaintext) - len(keyword)):
            keyword += keyword[j]
    for i in range(len(plaintext)):
        n = ord(plaintext[i])
        m = ord(keyword[i])
        if (n >= ord('A')) and (n <= ord('Z')):
            if (m - ord('A') + n) <= ord('Z'):
                ciphertext += chr(m - ord('А') + n)
            else:
                ciphertext += chr((m + n) % (1 + ord('Z')))
        else:
            if (m - ord('a') + n) <= ord('z'):
                ciphertext += chr(m - ord('a') + n)
            else:
                ciphertext += chr((m + n) % ord('a'))
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
    if len(keyword) < len(cipehrtext):
        for j in range(len(cipehrtext) - len(keyword)):
            keyword += keyword[j]
    for i in range(len(cipehrtext)):
        n = ord(cipehrtext[i])
        m = ord(keyword[i])
        if (n >= ord('A')) and (n <= ord('Z')):
            if n >= m:
                plaintext += chr(n - m + ord('A'))
            else:
                plaintext += chr(ord('Z') + 1 - (m - n))
        else:
            if n >= m:
                plaintext += chr(n - m + ord('a'))
            else:
                plaintext += chr(ord('Z') + 1 - (m - n))
    return plaintext
