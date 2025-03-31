# Include the libraries for socket and system calls
import socket
import sys
import os
import argparse
import re

# 1MB buffer size
BUFFER_SIZE = 1000000

# Get the IP address and Port number to use for this web proxy server
parser = argparse.ArgumentParser()
parser.add_argument('hostname', help='the IP Address Of Proxy Server')
parser.add_argument('port', help='the port number of the proxy server')
args = parser.parse_args()
proxyHost = args.hostname
proxyPort = int(args.port)

# Create a server socket, bind it to a port and start listening
try:
  # Create a server socket
  # ~~~~ INSERT CODE ~~~~
  # ~~~~ END CODE INSERT ~~~~
  print ('Created socket')
except:
  print ('Failed to create socket')
  sys.exit()

try:
  # Bind the the server socket to a host and port
  # ~~~~ INSERT CODE ~~~~
  # ~~~~ END CODE INSERT ~~~~
  print ('Port is bound')
except:
  print('Port is already in use')
  sys.exit()

try:
  # Listen on the server socket
  # ~~~~ INSERT CODE ~~~~
  # ~~~~ END CODE INSERT ~~~~
  print ('Listening to socket')
except:
  print ('Failed to listen')
  sys.exit()

# continuously accept connections
while True:
  print ('Waiting for connection...')
  clientSocket = None

  # Accept connection from client and store in the clientSocket
  try:
    # ~~~~ INSERT CODE ~~~~
    # ~~~~ END CODE INSERT ~~~~
    print ('Received a connection')
  except:
    print ('Failed to accept connection')
    sys.exit()

  # Get HTTP request from client
  # and store it in the variable: message_bytes
  # ~~~~ INSERT CODE ~~~~
  # ~~~~ END CODE INSERT ~~~~
  message = message_bytes.decode('utf-8')
  print ('Received request:')
  print ('< ' + message)

  # Extract the method, URI and version of the HTTP client request 
  requestParts = message.split()
  method = requestParts[0]
  URI = requestParts[1]
  version = requestParts[2]

  print ('Method:\t\t' + method)
  print ('URI:\t\t' + URI)
  print ('Version:\t' + version)
  print ('')

  # Get the requested resource from URI
  # Remove http protocol from the URI
  URI = re.sub('^(/?)http(s?)://', '', URI, count=1)

  # Remove parent directory changes - security
  URI = URI.replace('/..', '')

  # Split hostname from resource name
  resourceParts = URI.split('/', 1)
  hostname = resourceParts[0]
  resource = '/'

  if len(resourceParts) == 2:
    # Resource is absolute URI with hostname and resource
    resource = resource + resourceParts[1]

  print ('Requested Resource:\t' + resource)

  # Check if resource is in cache
  try:
    cacheLocation = './' + hostname + resource
    if cacheLocation.endswith('/'):
        cacheLocation = cacheLocation + 'default'

    print ('Cache location:\t\t' + cacheLocation)

    fileExists = os.path.isfile(cacheLocation)
    
    # Check wether the file is currently in the cache
    cacheFile = open(cacheLocation, "r")
    cacheData = cacheFile.readlines()

    print ('Cache hit! Loading from cache file: ' + cacheLocation)
    # ProxyServer finds a cache hit
    # Send back response to client 
    # ~~~~ INSERT CODE ~~~~
    # ~~~~ END CODE INSERT ~~~~
    cacheFile.close()
    print ('Sent to the client:')
    print ('> ' + cacheData)
  except:
    # cache miss.  Get resource from origin server
    originServerSocket = None
    # Create a socket to connect to origin server
    # and store in originServerSocket
    # ~~~~ INSERT CODE ~~~~
    # ~~~~ END CODE INSERT ~~~~

    print ('Connecting to:\t\t' + hostname + '\n')
    try:
      # Get the IP address for a hostname
      address = socket.gethostbyname(hostname)
      # Connect to the origin server
      # ~~~~ INSERT CODE ~~~~
      # ~~~~ END CODE INSERT ~~~~
      print ('Connected to origin Server')

      originServerRequest = ''
      originServerRequestHeader = ''
      # Create origin server request line and headers to send
      # and store in originServerRequestHeader and originServerRequest
      # originServerRequest is the first line in the request and
      # originServerRequestHeader is the second line in the request
      # ~~~~ INSERT CODE ~~~~
      # ~~~~ END CODE INSERT ~~~~

      # Construct the request to send to the origin server
      request = originServerRequest + '\r\n' + originServerRequestHeader + '\r\n\r\n'

      # Request the web resource from origin server
      print ('Forwarding request to origin server:')
      for line in request.split('\r\n'):
        print ('> ' + line)

      try:
        originServerSocket.sendall(request.encode())
      except socket.error:
        print ('Forward request to origin failed')
        sys.exit()

      print('Request sent to origin server\n')

      # Get the response from the origin server
      # ~~~~ INSERT CODE ~~~~
      # ~~~~ END CODE INSERT ~~~~

      # Send the response to the client
      # ~~~~ INSERT CODE ~~~~
      # ~~~~ END CODE INSERT ~~~~

      # Create a new file in the cache for the requested file.
      cacheDir, file = os.path.split(cacheLocation)
      print ('cached directory ' + cacheDir)
      if not os.path.exists(cacheDir):
        os.makedirs(cacheDir)
      cacheFile = open(cacheLocation, 'wb')

      # Save origin server response in the cache file
      # ~~~~ INSERT CODE ~~~~
      # ~~~~ END CODE INSERT ~~~~
      cacheFile.close()
      print ('cache file closed')

      # finished communicating with origin server - shutdown socket writes
      print ('origin response received. Closing sockets')
      originServerSocket.close()
       
      clientSocket.shutdown(socket.SHUT_WR)
      print ('client socket shutdown for writing')
    except OSError as err:
      print ('origin server request failed. ' + err.strerror)

  try:
    clientSocket.close()
  except:
    print ('Failed to close client socket')




#Handle cache hits
try:
    cacheLocation = './' + hostname + resource
    if cacheLocation.endswith('/'):
        cacheLocation = cacheLocation + 'default'

    print('Cache location:\t\t' + cacheLocation)

    fileExists = os.path.isfile(cacheLocation)
    
    # If the file exists in the cache, the cached data is returned
    if fileExists:
        with open(cacheLocation, 'rb') as cacheFile:
            cacheData = cacheFile.read()
        print('Cache hit! Loading from cache file: ' + cacheLocation)
        clientSocket.sendall(cacheData)  # Sends cached data back to the client
        print('Sent to the client:')        print('> ' + cacheData.decode('utf-8'))
    else:
        print('Cache miss. Fetching from origin server.')
        # If the cache misses, proceed with subsequent logic (fetch resources from the source server)
try:
    originServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    address = socket.gethostbyname(hostname)
    originServerSocket.connect((address, 80))  # Connect to the origin server

    # Create the origin server request header
    originServerRequest = f"GET {resource} HTTP/1.1\r\nHost: {hostname}\r\nConnection: close\r\n\r\n"
    originServerSocket.sendall(originServerRequest.encode())  # Send Request 

    response = b""
    while True:
        data = originServerSocket.recv(BUFFER_SIZE)
        if not data:
            break
        response += data

    # The response is processed and returned to the client
    clientSocket.sendall(response)
    
    # caching response
    cacheDir, file = os.path.split(cacheLocation)
    if not os.path.exists(cacheDir):
        os.makedirs(cacheDir)

    with open(cacheLocation, 'wb') as cacheFile:
        cacheFile.write(response)  # 将响应存入缓存
    print(f'Cached the response in: {cacheLocation}')

    originServerSocket.close()
except Exception as e:
    print(f"Failed to connect to the origin server: {e}")
if response.startswith(b"HTTP/1.1 301") or response.startswith(b"HTTP/1.1 302"):
    location_header = None
    for line in response.split(b"\r\n"):
        if line.lower().startswith(b"location:"):
            location_header = line.decode('utf-8').split(": ")[1]
            break

    if location_header:
        clientSocket.sendall(response)  # 将重定向响应发送给客户端
        print(f"Redirecting to: {location_header}")
import socket
import os
import re
import sys
import argparse
from datetime import datetime, timedelta

BUFFER_SIZE = 1000000

# Set the IP address and port number of the proxy server
parser = argparse.ArgumentParser()
parser.add_argument('hostname', help='the IP Address of Proxy Server')
parser.add_argument('port', help='the port number of the proxy server')
args = parser.parse_args()
proxyHost = args.hostname
proxyPort = int(args.port)

try:
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind((proxyHost, proxyPort))
    serverSocket.listen(5)
    print('Proxy server started, listening...')
except:
    print('Failed to create or bind socket')
    sys.exit()

while True:
    clientSocket, addr = serverSocket.accept()
    print(f"Connection received from {addr}")

    # Get the client request
    message_bytes = clientSocket.recv(BUFFER_SIZE)
    message = message_bytes.decode('utf-8')
    print(f"Received request:\n< {message}")

    #Parse request line
    requestParts = message.split()
    method, URI, version = requestParts[0], requestParts[1], requestParts[2]
    
    # Extract host names and resources from URIs
    URI = re.sub('^(/?)http(s?)://', '', URI, count=1)
    URI = URI.replace('/..', '')
    resourceParts = URI.split('/', 1)
    hostname = resourceParts[0]
    resource = '/' + resourceParts[1] if len(resourceParts) > 1 else '/'

    print(f"Requested Resource: {resource}")

    # Cache Handler Function
    cacheLocation = f'./{hostname}{resource}'
    if cacheLocation.endswith('/'):
        cacheLocation += 'default'

    try:
        if os.path.isfile(cacheLocation):
            with open(cacheLocation, 'rb') as cacheFile:
                cacheData = cacheFile.read()
            clientSocket.sendall(cacheData)
            print(f"Cache hit: Sending cached data from {cacheLocation}")
        else:
            # Send a request to the origin server
            originServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            originServerSocket.connect((socket.gethostbyname(hostname), 80))
            
            originServerRequest = f"GET {resource} HTTP/1.1\r\nHost: {hostname}\r\nConnection: close\r\n\r\n"
            originServerSocket.sendall(originServerRequest.encode())

            response = b""
            while True:
                data = originServerSocket.recv(BUFFER_SIZE)
                if not data:
                    break
                response += data

            # The response is sent to the client and cached
            clientSocket.sendall(response)
            with open(cacheLocation, 'wb') as cacheFile:
                cacheFile.write(response)

            originServerSocket.close()
            print(f"Resource fetched from origin server and cached at {cacheLocation}")

    except Exception as e:
        print(f"Error: {e}")

    clientSocket.close()
$ curl -iS http://localhost:8080/http://http.badssl.com/
$ curl -iS http://localhost:8080/http://http.badssl.com/fakefile.html
$ curl -iS "http://localhost:8080/http://httpbin.org/redirect-to?url=http://http.badssl.com&status_code=301"
$ curl -iS "http://localhost:8080/http://httpbin.org/redirect-to?url=http://http.badssl.com&status_code=302"
$ telnet localhost 8080
GET http://http.badssl.com HTTP/1.1

import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

proxyHost = "localhost"  # Change this if needed
proxyPort = 8080

try:
    server_socket.bind((proxyHost, proxyPort))
    print(f"Proxy server is running on {proxyHost}:{proxyPort}")
except Exception as e:
    print(f"Failed to bind: {e}")
    exit(1)

server_socket.listen(5)
print(f"Listening on {proxyHost}:{proxyPort}")
