import socket
import threading
import logging
from datetime import datetime

logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(message)s')

class ProcessTheClient(threading.Thread):
    def __init__(self, connection, address):
        self.connection = connection
        self.address = address
        threading.Thread.__init__(self)

    def run(self):
        logging.warning(f"[Thread-{self.name}] Handling {self.address}")
        buffer = b""
        try:
            while True:
                data = self.connection.recv(32)
                if not data:
                    break
                buffer += data

                while b'\r\n' in buffer:
                    line, buffer = buffer.split(b'\r\n', 1)
                    request = line.decode().strip()

                    if request == "TIME":
                        now = datetime.now()
                        waktu = now.strftime("%d %m %Y %H:%M:%S")
                        response = f"JAM {waktu}\r\n"
                        self.connection.sendall(response.encode())
                        logging.warning(f"[Thread-{self.name}] Sent: {response.strip()}")
                    elif request == "QUIT":
                        logging.warning(f"[Thread-{self.name}] Client {self.address} disconnected.")
                        self.connection.close()
                        return
                    else:
                        self.connection.sendall("ERROR\r\n".encode())
        except Exception as e:
            logging.warning(f"[Thread-{self.name}] Error: {str(e)}")
        finally:
            self.connection.close()

class Server(threading.Thread):
    def __init__(self, host='0.0.0.0', port=45000):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)
        self.host = host
        self.port = port
        threading.Thread.__init__(self)

    def run(self):
        logging.warning(f"[*] Server running on {self.host}:{self.port}")
        while True:
            conn, addr = self.server_socket.accept()
            logging.warning(f"[+] Connection from {addr}")
            client_thread = ProcessTheClient(conn, addr)
            client_thread.start()

def main():
    server = Server()
    server.start()

if __name__ == "__main__":
    main()
