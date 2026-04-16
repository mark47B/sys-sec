import zipfile
import itertools
import string
import sys
import time
import zlib

CHARSET = string.ascii_lowercase  # 'a'-'z'
MAX_LEN = 4


def bruteforce(zip_path: str) -> str | None:
    with zipfile.ZipFile(zip_path) as zf:
        for length in range(1, MAX_LEN + 1):
            for combo in itertools.product(CHARSET, repeat=length):
                password = "".join(combo)
                try:
                    zf.extractall(pwd=password.encode())
                    return password
                except (RuntimeError, zipfile.BadZipFile, zlib.error):
                    pass
    return None


if __name__ == "__main__":
    zip_path = sys.argv[1] if len(sys.argv) > 1 else "secret.zip"
    print(f"Brute-forcing '{zip_path}'...")
    t0 = time.time()
    password = bruteforce(zip_path)
    elapsed = time.time() - t0
    if password:
        print(f"pswd: {password}  (in {elapsed:.2f}s)")
    else:
        print(f"pswd not found (elapsed {elapsed:.2f}s)")
