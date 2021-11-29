# a ceasar cipher


class Cipher:
    def encrypt(word, shift=3):
        if word != None:
            cipher = []
            for char in word:
                cipher.append(chr(ord(char) + shift))
            return ''.join(cipher)
        return ""

    def decrypt(word, shift=3):
        if word != None:
            cipher = []
            for char in word:
                cipher.append(chr(ord(char) - shift))
            return ''.join(cipher)
        return ""
