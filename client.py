import socket

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 45000

def main():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((SERVER_HOST, SERVER_PORT))
        print(f"[Connected] to {SERVER_HOST}:{SERVER_PORT}")
        
        while True:
            command = input("TIME / QUIT: ").strip().upper()
            if command not in ["TIME", "QUIT"]:
                print("[!] Invalid command.")
                continue

            sock.sendall((command + "\r\n").encode())
            if command == "TIME":
                response = sock.recv(1024).decode()
                print(f"[Server] {response.strip()}")
            elif command == "QUIT":
                print("[Disconnected]")
                break

    except Exception as e:
        print(f"[Error] {e}")
    finally:
        sock.close()

if __name__ == "__main__":
    main()
