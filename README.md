# base64
base64 decode/encode 


## setup 

```sh
$ git clone https://github.com/salmiyounes/base64.git
$ cd base64
$ make
```

## usage

```python
from c_base64 import Base64
```
## example
```python
string: bytes = b'this is an example'
enc =  Base64.encode(string) # dGhpcyBpcyBhbiBleGFtcGxl
dec =  Base64.decode(enc)
```
