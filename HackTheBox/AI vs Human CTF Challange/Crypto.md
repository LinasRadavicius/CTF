**CTF: Based0x - Easy**

Download the files and view the .py script to see how output.txt was formated

from here we see variable m(original flag string) gets converted to a hex using hex(), after which using encode() it prepares for b64 encoding by turning it into bytes 

![image](https://github.com/user-attachments/assets/6cef7372-7629-45f3-84c0-936e36de9675)

next command encodes our variable m using B64 x three times

the script calls for encode(FLAG) which encodes the flag, and it writes encoded_flag.hex() to output.txt 

Breakdown of the encoding
Convert to hex >  convert to bytes > b64 encode x3 > convert to HEX 

to encode our flag we need to:
Convert to Bytes "FROM HEX" > B64 decode x3 > This returns the flag but in its HEX value apply one more "From HEX" 

I used CyberChef for this following modules in order
From Hex > From Base64 x3 > From Hex

![image](https://github.com/user-attachments/assets/ed1a0ce7-4fa5-4cec-b5e9-a7b6e402ad5b)

 
 
 
 
 
**Neighbour Primes**

as description say get RsaCtfTool
get private key
python3 RsaCtfTool.py --publickey pubkey.pem --private
use python script to decrypt it

from Crypto.PublicKey import RSA
from Crypto.Util.number import long_to_bytes
import base64

with open("private.pem", "r") as f:
    key = RSA.import_key(f.read())

ciphertext_hex = "YOUR_CIPHERTEXT_HEX"
ciphertext = int(ciphertext_hex, 16)  # Convert hex to int

plaintext = pow(ciphertext, key.d, key.n)

flag = long_to_bytes(plaintext)
print(flag.decode()

