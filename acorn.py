# Right rotate a 32-bit number n by k bits
def ROR(n, k):
    print('ROR:', ((n >> k) | (n << (32 - k))) & 0xFFFFFFFF )
    return ((n >> k) | (n << (32 - k))) & 0xFFFFFFFF

# Left rotate a 32-bit number n by k bits
def ROL(n, k):
    print('ROL:', ((n << k) | (n >> (32 - k))) & 0xFFFFFFFF)
    return ((n << k) | (n >> (32 - k))) & 0xFFFFFFFF

# Convert a 128-bit key into a list of four 32-bit integers
def key_schedule(k):
    KS = []
    
    for i in range(0, 16, 4):
        idx = i // 4
        KS.append((k[i] << 24) | (k[i+1] << 16) | (k[i+2] << 8) | k[i+3])
    print('key_schedule:', KS)
    return KS

# Convert a 128-bit nonce into a list of four 32-bit integers
def nonce_schedule(n):
    NS = []
    
    for i in range(0, 16, 4):
        idx = i // 4
        NS.append((n[i] << 24) | (n[i+1] << 16) | (n[i+2] << 8) | n[i+3])
    print('nonce_schedule', NS)
    return NS

# Generate a 32-bit subkey for round i
def subkey_generation(KS, NS, i):
    T = KS[(i-1)%4] ^ NS[(i-1)%4] ^ i
    T = ROL(T, 8)
    T = T + KS[(i+2)%4]
    T = T ^ NS[(i+1)%4]
    T = ROR(T, 3)
    print('subkey_gen:', T)
    return T

# Generate a 128-bit keystream block
def generate_keystream_block(KS, NS):
    S = []
    
    for i in range(20):
        T = subkey_generation(KS, NS, i+1)
        S.append(T & 0xFF)
        S.append((T >> 8) & 0xFF)
        S.append((T >> 16) & 0xFF)
        S.append((T >> 24) & 0xFF)
    print('generate_keystream_block', S )
    return S


## ACORN v3 encryption and decryption functions ##

# ACORN v3 encryption function
def acorn_v3_encrypt(pt, k, n):
    # Key and nonce schedule
    KS = key_schedule(k)    
    NS = nonce_schedule(n)    
    # Generate keystream
    keystream = generate_keystream_block(KS, NS)    
    # XOR plaintext with keystream to get ciphertext
    ct = [(keystream[i] ^ pt[i]) for i in range(len(pt))]
    print(pt)    
    return ct

# ACORN v3 decryption function
def acorn_v3_decrypt(ct, k, n):
    # Key and nonce schedule
    KS = key_schedule(k)
    NS = nonce_schedule(n)
    # Generate keystream
    keystream = generate_keystream_block(KS, NS)
    # XOR ciphertext with keystream to get plaintext
    pt = [(keystream[i] ^ ct[i]) for i in range(len(ct))]
    print(pt)
    return pt

 
## Example of use ##

# Example key and nonce
k = [0x01, 0x23, 0x45, 0x67, 0x89, 0xab, 0xcd, 0xef, 0xfe, 0xdc, 0xba, 0x98, 0x76, 0x54, 0x32, 0x10]
n = [0x01, 0x23, 0x45, 0x67, 0x89, 0xab, 0xcd, 0xef, 0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77, 0x88]

# Example plaintext "acorn v3"
pt = [0x41, 0x43, 0x4f, 0x52, 0x4e, 0x20, 0x76, 0x33] 

# Encrypt plaintext
ct = acorn_v3_encrypt(pt, k, n) # [65, 67, 79, 82, 78, 32, 118, 51]

# Print ciphertext
print("Ciphertext: ", end="")
for c in ct:
    print("{:02x}".format(c), end=" ")
print()

# Decrypt ciphertext
pt = acorn_v3_decrypt(ct, k, n) 

# Print plaintext
print("Plaintext: ", end="")
for p in pt:
    print("{:02x}".format(p), end=" ")
print()

keystream = [10, 192, 238, 140, 29, 166, 136, 234, 23, 221, 34, 49, 106, 51, 17, 183, 138, 192, 238, 140, 157, 167, 136, 234, 151, 221, 34, 49, 234, 
48, 17, 183, 10, 193, 238, 140, 29, 167, 136, 234, 23, 220, 34, 49, 106, 48, 17, 183, 138, 193, 238, 140, 157, 164, 136, 234, 151, 220, 34, 49, 234, 49, 17, 183, 
10, 206, 238, 140, 29, 164, 136, 234, 23, 219, 34, 49, 106, 49, 17, 183]
ct = [0x41, 0x43, 0x4f, 0x52, 0x4e, 0x20, 0x76, 0x33] 
print( [(keystream[i] ^ ct[i]) for i in range(len(ct))])

## ACORN v3 encryption and decryption functions with IV ##

# ACORN v3 encryption function with IV
def acorn_v3_encrypt_with_iv(pt, k, n, iv):
    # Key and nonce schedule
    KS = key_schedule(k)
    NS = nonce_schedule(n)
    # IV schedule
    IVS = nonce_schedule(iv)
    # Generate keystream
    keystream = generate_keystream_block(KS, NS)
    keystream_with_iv = generate_keystream_block(keystream, IVS)  # Combine keystream with IV
    # XOR plaintext with keystream to get ciphertext
    ct = [(keystream_with_iv[i] ^ pt[i]) for i in range(len(pt))]
    return ct

# ACORN v3 decryption function with IV
def acorn_v3_decrypt_with_iv(ct, k, n, iv):
    # Key and nonce schedule
    KS = key_schedule(k)
    NS = nonce_schedule(n)
    # IV schedule
    IVS = nonce_schedule(iv)
    # Generate keystream
    keystream = generate_keystream_block(KS, NS)
    keystream_with_iv = generate_keystream_block(keystream, IVS)  # Combine keystream with IV
    # XOR ciphertext with keystream to get plaintext
    pt = [(keystream_with_iv[i] ^ ct[i]) for i in range(len(ct))]
    return pt

# Example IV
iv = [0x01, 0x23, 0x45, 0x67, 0x89, 0xab, 0xcd, 0xef, 0xfe, 0xdc, 0xba, 0x98, 0x76, 0x54, 0x32, 0x10]

# Example plaintext "acorn v3"
pt = [0x41, 0x43, 0x4f, 0x52, 0x4e, 0x20, 0x76, 0x33] 

# Encrypt plaintext with IV
ct = acorn_v3_encrypt_with_iv(pt, k, n, iv)

# Print ciphertext
print("Ciphertext: ", end="")
for c in ct:
    print("{:02x}".format(c), end=" ")
print()

# Decrypt ciphertext with IV
pt = acorn_v3_decrypt_with_iv(ct, k, n, iv)

# Print plaintext
print("Plaintext: ", end="")
for p in pt:
    print("{:02x}".format(p), end=" ")
print()
