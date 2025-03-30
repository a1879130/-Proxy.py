import socket
import os
import sys
import urllib.parse

# Cache directory
CACHE_DIR = 'cache'

# Ensure the cache directory exists
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

def handle_request(client_socket):
    """Handle the request from the client."""
    request = client_socket.recv(1024).decode()

    if not request:
        return

    # Parse the request line (GET <url> HTTP/1.1)
    lines = request.splitlines()
    first_line = lines[0]
    parts = first_line.split()

    if len(parts) < 2 or parts[0] != "GET":
        client_socket.sendall(b"HTTP/1.1 400 Bad Request\r\n")
        client_socket.close()
        return

    url = parts[1]
    
    # Extract hostname and path from the URL
    parsed_url = urllib.parse.urlparse(url)
    hostname = parsed_url.hostname
    path = parsed_url.path if parsed_url.path else '/'
    port = 80

    # Check cache
    cache_file = os.path.join(CACHE_DIR, hostname + path.replace('/', '_') + ".cache")
    if os.path.exists(cache_file):
        print(f"Cache hit: {cache_file}")
        with open(cache_file, 'rb') as cached_file:
            client_socket.sendall(cached_file.read())
    else:
        print(f"Cache miss: Fetching {url} from origin server.")
        # Connect to the origin server
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.connect((hostname, port))

        # Forward the request to the origin server
        server_socket.sendall(request.encode())

        # Receive the response from the origin server
        response = b""
        while True:
            chunk = server_socket.recv(1024)
            if not chunk:
                break
            response += chunk
        
        # Cache the response
        with open(cache_file, 'wb') as cache:
            cache.write(response)

        # Send the response back to the client
        client_socket.sendall(response)

        server_socket.close()

    # Close the client connection
    client_socket.close()


def start_proxy_server(host, port):
    """Start the proxy server."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Proxy server listening on {host}:{port}...")

    while True:
        # Accept incoming client connections
        client_socket, client_addr = server_socket.accept()
        print(f"Received connection from {client_addr}")

        # Handle the client's request
        handle_request(client_socket)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python Proxy.py <host> <port>")
        sys.exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])

    start_proxy_server(host, port)
import socket
import os
import sys
import urllib.parse
import time

# Cache directory
CACHE_DIR = 'cache'

# Ensure the cache directory exists
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

def handle_request(client_socket):
    """Handle the request from the client."""
    request = client_socket.recv(1024).decode()

    if not request:
        return

    # Parse the request line (GET <url> HTTP/1.1)
    lines = request.splitlines()
    first_line = lines[0]
    parts = first_line.split()

    if len(parts) < 2 or parts[0] != "GET":
        client_socket.sendall(b"HTTP/1.1 400 Bad Request\r\n")
        client_socket.close()
        return

    url = parts[1]
    
    # Extract hostname and path from the URL
    parsed_url = urllib.parse.urlparse(url)
    hostname = parsed_url.hostname
    path = parsed_url.path if parsed_url.path else '/'
    port = 80

    # Check cache
    cache_file = os.path.join(CACHE_DIR, hostname + path.replace('/', '_') + ".cache")
    if os.path.exists(cache_file):
        # Check Cache-Control header for max-age
        with open(cache_file, 'rb') as cached_file:
            cached_data = cached_file.read()

            # Check if the cache is still valid
            # If we had a Cache-Control header with max-age, we'd compare the time
            # This example assumes we're not handling that yet, but you can add that logic here.
            if is_cache_valid(cached_file):
                print(f"Cache hit: {cache_file}")
                client_socket.sendall(cached_data)
                client_socket.close()
                return
            else:
                print(f"Cache expired: {cache_file}, fetching from origin server.")
    
    # Cache miss or expired cache, fetch from origin server
    print(f"Cache miss: Fetching {url} from origin server.")
    # Connect to the origin server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect((hostname, port))

    # Forward the request to the origin server
    server_socket.sendall(request.encode())

    # Receive the response from the origin server
    response = b""
    while True:
        chunk = server_socket.recv(1024)
        if not chunk:
            break
        response += chunk

    # Cache the response
    with open(cache_file, 'wb') as cache:
        cache.write(response)

    # Send the response back to the client
    client_socket.sendall(response)

    server_socket.close()
    client_socket.close()


def is_cache_valid(cached_file):
    """Determine if the cached file is still valid based on cache-control headers."""
    # For now, we assume that all cached files expire after 3600 seconds (1 hour).
    # You can parse headers from the cached response and add more logic here.
    file_mod_time = os.path.getmtime(cached_file.name)
    current_time = time.time()
    max_age = 3600  # This is just an example, in real-world you'd extract max-age from headers
    if current_time - file_mod_time <= max_age:
        return True
    return False


def start_proxy_server(host, port):
    """Start the proxy server."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Proxy server listening on {host}:{port}...")

    while True:
        # Accept incoming client connections
        client_socket, client_addr = server_socket.accept()
        print(f"Received connection from {client_addr}")

        # Handle the client's request
        handle_request(client_socket)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python Proxy.py <host> <port>")
        sys.exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])

    start_proxy_server(host, port)
import socket
import os
import sys
import urllib.parse
import time

# Cache directory
CACHE_DIR = 'cache'

# Ensure the cache directory exists
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

def handle_request(client_socket):
    """Handle the request from the client."""
    request = client_socket.recv(1024).decode()

    if not request:
        return

    # Parse the request line (GET <url> HTTP/1.1)
    lines = request.splitlines()
    first_line = lines[0]
    parts = first_line.split()

    if len(parts) < 2 or parts[0] != "GET":
        client_socket.sendall(b"HTTP/1.1 400 Bad Request\r\n")
        client_socket.close()
        return

    url = parts[1]
    
    # Extract hostname and path from the URL
    parsed_url = urllib.parse.urlparse(url)
    hostname = parsed_url.hostname
    path = parsed_url.path if parsed_url.path else '/'
    port = 80

    # Check cache
    cache_file = os.path.join(CACHE_DIR, hostname + path.replace('/', '_') + ".cache")
    if os.path.exists(cache_file):
        # Check Cache-Control header for max-age
        with open(cache_file, 'rb') as cached_file:
            cached_data = cached_file.read()

            # Check if the cache is still valid
            # If we had a Cache-Control header with max-age, we'd compare the time
            # This example assumes we're not handling that yet, but you can add that logic here.
            if is_cache_valid(cached_file):
                print(f"Cache hit: {cache_file}")
                client_socket.sendall(cached_data)
                client_socket.close()
                return
            else:
                print(f"Cache expired: {cache_file}, fetching from origin server.")
    
    # Cache miss or expired cache, fetch from origin server
    print(f"Cache miss: Fetching {url} from origin server.")
    # Connect to the origin server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect((hostname, port))

    # Forward the request to the origin server
    server_socket.sendall(request.encode())

    # Receive the response from the origin server
    response = b""
    while True:
        chunk = server_socket.recv(1024)
        if not chunk:
            break
        response += chunk

    # Cache the response
    with open(cache_file, 'wb') as cache:
        cache.write(response)

    # Send the response back to the client
    client_socket.sendall(response)

    server_socket.close()
    client_socket.close()


def is_cache_valid(cached_file):
    """Determine if the cached file is still valid based on cache-control headers."""
    # For now, we assume that all cached files expire after 3600 seconds (1 hour).
    # You can parse headers from the cached response and add more logic here.
    file_mod_time = os.path.getmtime(cached_file.name)
    current_time = time.time()
    max_age = 3600  # This is just an example, in real-world you'd extract max-age from headers
    if current_time - file_mod_time <= max_age:
        return True
    return False


def start_proxy_server(host, port):
    """Start the proxy server."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Proxy server listening on {host}:{port}...")

    while True:
        # Accept incoming client connections
        client_socket, client_addr = server_socket.accept()
        print(f"Received connection from {client_addr}")

        # Handle the client's request
        handle_request(client_socket)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python Proxy.py <host> <port>")
        sys.exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])

    start_proxy_server(host, port)
def handle_request(client_socket):
    """Handle the request from the client."""
    request = client_socket.recv(1024).decode()

    if not request:
        return

    # Parse the request line (GET <url> HTTP/1.1)
    lines = request.splitlines()
    first_line = lines[0]
    parts = first_line.split()

    if len(parts) < 2 or parts[0] != "GET":
        client_socket.sendall(b"HTTP/1.1 400 Bad Request\r\n")
        client_socket.close()
        return

    url = parts[1]
    
    # Extract hostname and path from the URL
    parsed_url = urllib.parse.urlparse(url)
    hostname = parsed_url.hostname
    path = parsed_url.path if parsed_url.path else '/'
    port = 80

    # Check cache
    cache_file = os.path.join(CACHE_DIR, hostname + path.replace('/', '_') + ".cache")
    if os.path.exists(cache_file):
        print(f"Cache hit: {cache_file}")
        with open(cache_file, 'rb') as cached_file:
            cached_data = cached_file.read()
            client_socket.sendall(cached_data)
            client_socket.close()
            return
    
    # Cache miss, fetch from origin server
    print(f"Cache miss: Fetching {url} from origin server.")
    # Connect to the origin server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect((hostname, port))

    # Forward the request to the origin server
    server_socket.sendall(request.encode())

    # Receive the response from the origin server
    response = b""
    while True:
        chunk = server_socket.recv(1024)
        if not chunk:
            break
        response += chunk

    # Check the HTTP status code in the response
    if response.startswith(b"HTTP/1.1 200"):
        # Success, send the response back to client
        client_socket.sendall(response)
    elif response.startswith(b"HTTP/1.1 301") or response.startswith(b"HTTP/1.1 302"):
        # Redirect, send back to client
        handle_redirect(response, client_socket)
    elif response.startswith(b"HTTP/1.1 404"):
        # Resource not found, send back 404 response
        client_socket.sendall(b"HTTP/1.1 404 Not Found\r\n")
        client_socket.sendall(b"Content-Type: text/plain\r\n\r\n")
        client_socket.sendall(b"404 Not Found: The requested resource could not be found.")
    elif response.startswith(b"HTTP/1.1 500"):
        # Internal server error, send back 500 response
        client_socket.sendall(b"HTTP/1.1 500 Internal Server Error\r\n")
        client_socket.sendall(b"Content-Type: text/plain\r\n\r\n")
        client_socket.sendall(b"500 Internal Server Error: Something went wrong.")
    elif response.startswith(b"HTTP/1.1 503"):
        # Service unavailable, send back 503 response
        client_socket.sendall(b"HTTP/1.1 503 Service Unavailable\r\n")
        client_socket.sendall(b"Content-Type: text/plain\r\n\r\n")
        client_socket.sendall(b"503 Service Unavailable: The server is temporarily unable to process the request.")
    else:
        # Default error handling for unknown status codes
        client_socket.sendall(b"HTTP/1.1 500 Internal Server Error\r\n")
        client_socket.sendall(b"Content-Type: text/plain\r\n\r\n")
        client_socket.sendall(b"500 Internal Server Error: Unexpected response from origin server.")

    # Cache the response if it's a valid status code (not error)
    if response.startswith(b"HTTP/1.1 200"):
        with open(cache_file, 'wb') as cache:
            cache.write(response)

    server_socket.close()
    client_socket.close()

def handle_redirect(response, client_socket):
    """Handle HTTP 301 or 302 redirects."""
    # Extract Location header from the response
    location_header = b""
    for line in response.split(b"\r\n"):
        if line.lower().startswith(b"location:"):
            location_header = line
            break

    # Forward the redirection to the client
    if location_header:
        client_socket.sendall(response)
        print(f"Redirected to {location_header.decode().split(': ')[1]}")
    else:
        client_socket.sendall(b"HTTP/1.1 500 Internal Server Error\r\n")
        client_socket.sendall(b"Content-Type: text/plain\r\n\r\n")
        client_socket.sendall(b"500 Internal Server Error: Missing Location header in redirect.")
