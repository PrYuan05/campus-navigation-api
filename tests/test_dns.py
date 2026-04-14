import socket
try:
    host = 'oauth2.googleapis.com'
    print(f"Resolving {host}...")
    print(f"IP Address: {socket.gethostbyname(host)}")
    print("DNS Resolution: SUCCESS")
except Exception as e:
    print(f"DNS Resolution: FAILED. Error: {e}")