import socket
import threading
import time

def server(host='0.0.0.0', port=5000):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Server listening on {host}:{port}")
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            start_time = time.time()
            total_bytes = 0
            while True:
                data = conn.recv(4096)
                if not data:
                    break
                total_bytes += len(data)
            end_time = time.time()
            elapsed_time = end_time - start_time
            speed_mbps = (total_bytes * 8) / (elapsed_time * 1_000_000)
            print(f"Transfer completed: {total_bytes} bytes in {elapsed_time:.2f} seconds")
            print(f"Speed: {speed_mbps:.2f} Mbps")


def client(server_ip, port=5000, data_size=100 * 1024 * 1024):
    data = b'0' * 4096
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((server_ip, port))
        print(f"Connected to server at {server_ip}:{port}")
        start_time = time.time()
        bytes_sent = 0
        while bytes_sent < data_size:
            s.sendall(data)
            bytes_sent += len(data)
        end_time = time.time()
        elapsed_time = end_time - start_time
        speed_mbps = (bytes_sent * 8) / (elapsed_time * 1_000_000)
        print(f"Sent {bytes_sent} bytes in {elapsed_time:.2f} seconds")
        print(f"Speed: {speed_mbps:.2f} Mbps")


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="Internal Network Speed Test Tool")
    parser.add_argument('mode', choices=['server', 'client'], help="Mode to run: server or client")
    parser.add_argument('--host', default='0.0.0.0', help="Server host (default: 0.0.0.0)")
    parser.add_argument('--port', type=int, default=5000, help="Port to use (default: 5000)")
    parser.add_argument('--server-ip', help="Server IP address (required for client mode)")
    parser.add_argument('--size', type=int, default=100 * 1024 * 1024, help="Data size to send in bytes (default: 100MB)")

    args = parser.parse_args()

    if args.mode == 'server':
        server(args.host, args.port)
    elif args.mode == 'client':
        if not args.server_ip:
            print("Error: --server-ip is required in client mode")
        else:
            client(args.server_ip, args.port, args.size)
