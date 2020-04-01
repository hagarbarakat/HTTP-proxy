import socket
from skeleton import check_http_request_validity, parse_http_request, HttpRequestState, HttpRequestInfo

i = 20
while i > 0:
    client_addr = ("127.0.0.1", 18888)

    # This argument is optional, defaults to 18888
    # proxy_port_number = get_arg(1, 18888)
    # skt = entry_point(proxy_port_number)

    req_str = "GET / HTTP/1.0\r\nHost: www.google.com\r\n\r\n"
    # p = http_request_pipeline(client_addr, req_str)
    print(req_str)
    s = socket.socket(socket.AF_INET,
                      socket.SOCK_STREAM)

    host = socket.gethostname()  # or just use (host = '')
    port = 18888

    s.connect((host, port))
    s.send(req_str.encode("ascii"))

    tm = s.recv(1024)  # msg can only be 1024 bytes long
    print(tm)
    s.close()
    print("response: ", tm.decode("ascii"))
    i -= 1