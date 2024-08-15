import os
import ctypes

class Base64:
    _libname: str = os.path.join(os.getcwd(), 'base64_encoder.so')
    _lib = ctypes.CDLL(_libname)
    _BASE64_ENCODE_OUT_SIZE = lambda x: int(((x + 2) // 3) * 4 + 1)
    _BASE64_DECODE_OUT_SIZE = lambda x: int((x // 4) * 3)

    @staticmethod
    def decode(encoded_string: bytes) -> bytes:

        if not isinstance(encoded_string, bytes):
            raise TypeError(f"Expected bytes-like object, got '{type(encoded_string).__name__}'")

        output_size = Base64._BASE64_DECODE_OUT_SIZE(len(encoded_string))
        decoded_buffer = ctypes.create_string_buffer(output_size)

        Base64._lib.base64_decode(encoded_string, len(encoded_string), decoded_buffer)
        
        return decoded_buffer.value.rstrip(b'\x00')

    @staticmethod
    def encode(input_bytes: bytes) -> bytes:

        if not isinstance(input_bytes, bytes):
            raise TypeError(f"Expected bytes-like object, got '{type(input_bytes).__name__}'")

        output_size = Base64._BASE64_ENCODE_OUT_SIZE(len(input_bytes))
        encoded_buffer = ctypes.create_string_buffer(output_size)

        Base64._lib.base64_encode(input_bytes, len(input_bytes), encoded_buffer)
        
        return encoded_buffer.value.rstrip(b'\x00')

class Base64Error(Exception):
    pass

class TypeError(Base64Error):
    pass
