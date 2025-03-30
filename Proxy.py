import socket
import threading
import hashlib
import os
import time

# Cache directory
CACHE_DIR = "./cache"
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

def generate_cache_key(url):
    """Generate a cache file path based on the URL"""
    return os.path.join(CACHE_DIR, hashlib.md5(url.encode()).hexdigest())

def get_cached_response(cache_key):
    """Retrieve cached data if it exists and is not expired"""
    if os.path.exists(cache_key):
        with open(cache_key, "rb") as f:
            timestamp = float(f.readline().strip())  # Read timestamp
            if time.time() - timestamp < 60:  # Cache expiry time (60 seconds)
                return f.read()  # Return cached response
    return None

def cache_response(cache_key, data):
    """Store response data in cache"""
    with open(cache_key, "wb") as f:
        f.write(f"{time.time()}\n".encode())  # Save timestamp
        f.write(data)  # Write response data

def handle_client(client_socket):
    """Handle client requests"""
    request = client_socket.recv(4096)
    if not request:
        client_socket.close()
        return
    
    # Parse the first line of the HTTP request
    request_line = request.decode().split("\n")[0]
    print(f"Request: {request_line}")

    try:
        method, url, http_version = request_line.split()
    except ValueError:
        client_socket.close()
        return

    if method != "GET":
        client_socket.send(b"HTTP/1.1 405 Method Not Allowed\r\n\r\n")
        client_socket.close()
        return

    # Extract hostname and path from URL
    url = url.strip()
    if "://" in url:
        url = url.split("://")[1]
    host = url.split("/")[0]
    path = "/" + "/".join(url.split("/")[1:])

    # Check for cached response
    cache_key = generate_cache_key(url)
    cached_response = get_cached_response(cache_key)
    if cached_response:
        print(f"Loaded from cache: {url}")
        client_socket.sendall(cached_response)
        client_socket.close()
        return

    # Forward request to the target server
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as remote_socket:
            remote_socket.connect((host, 80))
            request_headers = f"GET {path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
            remote_socket.sendall(request_headers.encode())

            # Read response from the remote server
            response = b""
            while True:
                chunk = remote_socket.recv(4096)
                if not chunk:
                    break
                response += chunk

            # Cache the response
            cache_response(cache_key, response)

            # Send response to the client
            client_socket.sendall(response)
    except Exception as e:
        print(f"Failed to fetch {url}: {e}")
        client_socket.send(b"HTTP/1.1 502 Bad Gateway\r\n\r\n")
    
    client_socket.close()

def start_proxy():
    """Start the proxy server"""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("0.0.0.0", 8888))
    server_socket.listen(5)
    print("Proxy server running on port 8888...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Received connection from: {addr}")
        threading.Thread(target=handle_client, args=(client_socket,)).start()

if __name__ == "__main__":
    start_proxy()
