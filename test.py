from typing import List
import ctypes
import base64
from tqdm import tqdm
import time
import os

libname: str = os.path.abspath(os.getcwd() + '/base64_encoder.so')
testfile: str = os.path.abspath(os.getcwd() + '/word-list.txt')

BASE64_ENCODE_OUT_SIZE = lambda x: int(((x + 2) // 3) * 4 + 1)
BASE64_DECODE_OUT_SIZE = lambda x: int((x // 4) * 3)

def test(strings: List[str]) -> None:

    lib = ctypes.CDLL(libname)
    lib.base64_encode.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p]
    lib.base64_decode.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p]
    
    start = time.monotonic()

    for num, string in enumerate(tqdm([bytes(s, 'utf-8') for s in strings], desc="Testing"), start=1):
        # Encoding
        output_size = BASE64_ENCODE_OUT_SIZE(len(string))
        out = ctypes.create_string_buffer(output_size)
        
        lib.base64_encode(string, len(string), out)
        encoded_result = out.value.rstrip(b'\x00')
        
        assert base64.b64encode(string) == encoded_result, f"Mismatch for encoding input {string}"

        # Decoding
        decode_output_size = BASE64_DECODE_OUT_SIZE(len(encoded_result))
        s_in = ctypes.create_string_buffer(decode_output_size)

        lib.base64_decode(encoded_result, len(encoded_result), s_in)
        decoded_result = s_in.value.rstrip(b'\x00')
        
        assert base64.b64decode(base64.b64encode(string)) == decoded_result, f"Mismatch for decoding input {string}"

    end = time.monotonic() - start
    print(f'\n{num} test cases passed in {end:.3f} seconds.')

if __name__ == '__main__':
    with open(testfile, 'r') as file:
        strings: List[str] = file.read().strip().split('\n')
    test(strings)
