import zipfile
import itertools
import string
import sys
import time
import multiprocessing
import zlib

CHARSET = string.ascii_lowercase  # 'a'-'z'
MAX_LEN = 4


def generate_passwords() -> list[str]:
    passwords = []
    for length in range(1, MAX_LEN + 1):
        for combo in itertools.product(CHARSET, repeat=length):
            passwords.append("".join(combo))
    return passwords


def try_chunk(zip_path: str, chunk: list[str], found: multiprocessing.Value) -> None:
    """Перебирает список паролей chunk; при нахождении записывает результат в found."""
    with zipfile.ZipFile(zip_path) as zf:
        for password in chunk:
            if found.value:          # другой процесс уже нашёл
                return
            try:
                zf.extractall(pwd=password.encode())
                found.value = password.encode()
                return
            except (RuntimeError, zipfile.BadZipFile, zlib.error):
                pass


def bruteforce_parallel(zip_path: str, num_workers: int) -> str | None:
    passwords = generate_passwords()
    total = len(passwords)
    chunk_size = (total + num_workers - 1) // num_workers
    chunks = [passwords[i : i + chunk_size] for i in range(0, total, chunk_size)]

    manager = multiprocessing.Manager()
    found = manager.Value("s", b"")

    with multiprocessing.Pool(num_workers) as pool:
        pool.starmap(try_chunk, [(zip_path, chunk, found) for chunk in chunks])

    return found.value.decode() if found.value else None


if __name__ == "__main__":
    zip_path   = sys.argv[1] if len(sys.argv) > 1 else "secret.zip"
    num_workers = int(sys.argv[2]) if len(sys.argv) > 2 else multiprocessing.cpu_count()

    print(f"Brute-forcing '{zip_path}' with {num_workers} workers...")
    t0 = time.time()
    password = bruteforce_parallel(zip_path, num_workers)
    elapsed = time.time() - t0

    if password:
        print(f"pswd found: {password}  (in {elapsed:.2f}s, {num_workers} workers)")
    else:
        print(f"pswd not found (elapsed {elapsed:.2f}s)")
