from typing import List
import ctypes
from ctypes import *
import base64
from tqdm import tqdm
import os

libname: str = os.path.abspath(os.getcwd() + '/base64_encoder.so')
testfile: str = os.path.abspath(os.getcwd() + '/word-list.txt')

BASE64_ENCODE_OUT_SIZE = lambda x: int(((x + 2) // 3) * 4 + 1)
BASE64_DECODE_OUT_SIZE = lambda x: int((x // 4) * 3)

def test(strings: List[str]) -> None:
        lib = ctypes.CDLL(libname)
        lib.base64_encode.argtypes = [c_char_p, c_int, c_char_p]
        lib.base64_decode.argtypes = [c_char_p, c_int, c_char_p]

        for string in tqdm([bytes(s, 'utf-8') for s in strings], desc="Testing"):
            # Encoding
            output_size = BASE64_ENCODE_OUT_SIZE(len(string))
            out = create_string_buffer(output_size)
            
            lib.base64_encode(string, len(string), out)
            encoded_result = out.value.rstrip(b'\x00')
            
            assert base64.b64encode(string) == encoded_result, f"Mismatch for encoding input {string}"

            # Decoding
            decode_output_size = BASE64_DECODE_OUT_SIZE(len(encoded_result))
            s_in = create_string_buffer(decode_output_size)

            lib.base64_decode(encoded_result, len(encoded_result), s_in)
            decoded_result = s_in.value.rstrip(b'\x00')
            
            assert base64.b64decode(base64.b64encode(string)) == decoded_result, f"Mismatch for decoding input {string}"


if __name__ == '__main__':
        list: List[str] = open(testfile, 'r').read().strip().split('\n')
        test(list)
