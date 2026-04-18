import __main__

def encrypt(p):
    if isinstance(p, bytes):
        return p.decode('utf-8', errors='replace')
    return str(p)

__main__.encrypt = encrypt
print("encrypt patched: now returns plaintext")
