from typing import List
import base64
from c_base64 import Base64
from tqdm import tqdm
import time
import os

def test(strings: List[str]) -> None:
    start = time.monotonic()

    for num, string in enumerate(tqdm([bytes(s, 'utf-8') for s in strings], desc="Testing"), start=1):
        # Encoding
        encoded_result = Base64.encode(string)
        assert base64.b64encode(string) == encoded_result, f"Mismatch for encoding input {string}"

        # Decoding
        decoded_result = Base64.decode(encoded_result)
        assert string == decoded_result, f"Mismatch for decoding input {string}"

    end = time.monotonic() - start
    print(f'\n{num} test cases passed in {end:.3f} seconds.')

if __name__ == '__main__': 
    testfile: str = os.path.join(os.getcwd(), 'word-list.txt')
    with open(testfile, 'r') as file:
        strings: List[str] = file.read().strip().split('\n')
    test(strings)
