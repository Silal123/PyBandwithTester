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

                elapsed_time = time.time() - start_time
                if elapsed_time > 0:
                    speed_mbps = (total_bytes * 8) / (elapsed_time * 1_000_000)
                    print(f"Current speed: {speed_mbps:.2f} Mbps", end='\r')

            elapsed_time = time.time() - start_time
            speed_mbps =  (total_bytes * 8) / (elapsed_time * 1_000_000) if elapsed_time > 0 else 0
            print(f"\nTransfer completed: {total_bytes} bytes in {elapsed_time:.2f} seconds")
            print(f"Speed: {speed_mbps:.2f} Mbps")

def client(server_ip, port=5000, duration=-1):
    data = b'0' * 4096
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((server_ip, port))
        print(f"Connected to server at {server_ip}:{port}")
        start_time = time.time()
        bytes_sent = 0
        
        while duration == -1 or (time.time() - start_time) < duration:
            s.sendall(data)
            bytes_sent += len(data)
            
            elapsed_time = time.time() - start_time
            speed_mbps = (bytes_sent * 8) / (elapsed_time * 1_000_000) if elapsed_time > 0 else 0
            print(f"Current speed: {speed_mbps:.2f} Mbps", end='\r')
        
        print(f"\nSent {bytes_sent} bytes in {elapsed_time:.2f} seconds")
        print(f"Speed: {speed_mbps:.2f} Mbps")

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="Internal Network Speed Test Tool")
    parser.add_argument('mode', choices=['server', 'client'], help="Mode to run: server or client")
    parser.add_argument('--host', default='0.0.0.0', help="Server host (default: 0.0.0.0)")
    parser.add_argument('--port', type=int, default=5000, help="Port to use (default: 5000)")
    parser.add_argument('--server-ip', help="Server IP address (required for client mode)")
    parser.add_argument('--duration', type=int, default=-1, help="Duration in seconds (-1 for unlimited)")

    args = parser.parse_args()

    if args.mode == 'server':
        while True:
            server(args.host, args.port)
            print("Restarting server...")
    elif args.mode == 'client':
        if not args.server_ip:
            print("Error: --server-ip is required in client mode")
        else:
            client(args.server_ip, args.port, args.duration)
