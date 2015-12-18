# An implementation of the simple Caesar Cipher
# based on https://github.com/jmalk/dailypython.git
# and modified for beaconinside test with minor improvements

import argparse
import sys

class CaesarCipher(object):

    alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']


    def encrypt(self, plaintext, shift_by):
        return self.__doCrypto(plaintext, shift_by)

    def decrypt(self, ciphertext, shift_by):
        return self.__doCrypto(ciphertext, -shift_by)

    def __doCrypto(self, text, shift):
        plaintext = text.upper()
        ciphertext = ""
        for character in plaintext:
            if character == ' ':
                ciphertext += ' '
            else:
                position_in_alphabet = self.alphabet.index(character)
                ciphertext += self.alphabet[position_in_alphabet + shift]
        return ciphertext

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="de- and encrypt Caesar Cipher")
    parser.add_argument("--message", "-m", type=str, help="message to be encrypted or decrypted.", required=True, dest='message')
    parser.add_argument("--decrypt", "-d", help="decrypt the message", action='store_true', default=False, dest='decrypt')
    parser.add_argument("--encrypt", "-e", help="encrypt the message", action='store_true', default=False, dest='encrypt')
    parser.add_argument("--shift", "-s", type=int, help="shift delta settings", default=3, dest='shift')

    args = parser.parse_args()

    # lazy check for plausibilty
    if args.decrypt and args.encrypt:
        print "Either you encrypt or decrypt the message... chose wisely"
        sys.exit(1)

    # do Caesar
    caesar = CaesarCipher()
    if args.encrypt:
        print caesar.encrypt(args.message, args.shift)
    elif args.decrypt:
        print caesar.decrypt(args.message, args.shift)