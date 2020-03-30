import socket
from skeleton import check_http_request_validity, parse_http_request, HttpRequestState, HttpRequestInfo

# creates socket object
s = socket.socket(socket.AF_INET,
                  socket.SOCK_STREAM)

host = socket.gethostname() # or just use (host = '')
port = 18888

s.connect((host, port))
s.sendall(b'Here I am!')

tm = s.recv(1024) # msg can only be 1024 bytes long
print(tm)
s.close()
print("the time we got from the server is %s" % tm.decode('ascii'))