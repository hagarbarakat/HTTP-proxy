import sys
from server import check_http_request_validity, parse_http_request, HttpRequestState, HttpRequestInfo,http_request_pipeline
import socket

#######################################
# Leave the code below as is. (Tests)
# Read them to know how your classes
# are used.
#######################################


def lineno():
    return sys._getframe().f_back.f_lineno


def simple_http_parsing_test_cases():
    """
    Example test cases, do NOT modify this.
    If your code is correct, calling this function will have no effect.
    """
    client_addr = ("127.0.0.1", 9877)

    #######################################
    #######################################
    case = "Parse HTTP method."

    req_str = "GET / HTTP/1.0\r\nHost: www.google.com\r\n"
    req_str += "Accept: application/json\r\n"
    req_str += "AYhAGA: AJSJBD/KSDNCN\r\n\r\n"
    parsed = parse_http_request(client_addr, req_str)

    actual_value = parsed.method
    correct_value = "GET"
    assert correct_value == actual_value,\
        f"[Line {lineno()}] [failed] {case}"\
        " Expected ( %s ) got ( %s )" % (correct_value, actual_value)
    print(f"[success] {case}")

    #######################################
    case = "Parse headers."

    # "Host: google.com" header is added to the request.
    # note that the ":" is removed.
    actual_value = parsed.headers[0]        # note: headers is a list of lists
    correct_value = ["Host", "www.google.com"]
    assert correct_value == actual_value,\
        f"[Line {lineno()}] [failed] {case}"\
        " Expected ( %s ) got ( %s )" % (correct_value, actual_value)
    print(f"[success] {case}")

    #######################################
    case = "Parse HTTP request path."

    correct_value = "/"
    actual_value = parsed.requested_path
    assert correct_value == actual_value,\
        f"[Line {lineno()}] [failed] {case}"\
        " Expected ( %s ) got ( %s )" % (correct_value, actual_value)
    print(f"[success] {case}")

    #######################################
    case = "Add Default value of the port if it doesn't exist in the request."

    correct_value = str(80)
    actual_value = str(parsed.requested_port)
    assert correct_value == actual_value,\
        f"[Line {lineno()}] [failed] {case}"\
        " Expected ( %s ) got ( %s )" % (correct_value, actual_value)
    print(f"[success] {case}")

    #######################################
    case = "Add requested host field."

    actual_value = parsed.requested_host
    correct_value = "www.google.com"
    assert correct_value == actual_value,\
        f"[Line {lineno()}] [failed] {case}"\
        " Expected ( %s ) got ( %s )" % (correct_value, actual_value)
    print(f"[success] {case}")

    #######################################
    #######################################

    case = "Convert full URL in request to relative path."

    actual_value = parsed.requested_path
    correct_value = "/"
    assert correct_value == actual_value,\
        f"[Line {lineno()}] [failed] {case}"\
        " Expected ( %s ) got ( %s )" % (correct_value, actual_value)
    print(f"[success] {case}")

    #######################################
    case = "Add host header if a full HTTP path is used in request."

    actual_value = parsed.headers[0]
    correct_value = ["Host", "www.google.com"]
    assert correct_value == actual_value,\
        f"[Line {lineno()}] [failed] {case}"\
        " Expected ( %s ) got ( %s )" % (correct_value, actual_value)
    print(f"[success] {case}")

    #######################################
    #######################################
    case = "Parse HTTP headers"

    req_str = "GET / HTTP/1.0\r\nHost: www.google.com:8080\r\nAccept: application/json\r\n\r\n"
    parsed = parse_http_request(client_addr, req_str)

    actual_value = str(len(parsed.headers))
    correct_value = str(2)
    assert correct_value == actual_value,\
        f"[Line {lineno()}] [failed] {case}"\
        " Expected ( %s ) got ( %s )" % (correct_value, actual_value)
    print(f"[success] {case}")

    #######################################
    #######################################
    case = "convert HttpRequestInfo to a the corresponding HTTP request"
    # A request to www.google.com/ , note adding the ":" to headers
    # "Host" header comes first
    headers = [["Host", "www.google.com:8080"], ["Accept", "application/json"], ["AYhAGA","AJSJBD/KSDNCN"]]
    req = HttpRequestInfo(client_addr, "GET",
                          "www.google.com", 80, "/", headers)

    http_string = "GET / HTTP/1.0\r\nHost: www.google.com:8080\r\n"
    http_string += "Accept: application/json\r\n"
    http_string += "AYhAGA: AJSJBD/KSDNCN\r\n\r\n"
    correct_value = http_string
    actual_value = req.to_http_string()
    assert correct_value == actual_value,\
        f"[Line {lineno()}] [failed] {case}"\
        " Expected \n( %s ) got\n ( %s )" % (correct_value, actual_value)
    print(f"[success] {case}")


def simple_http_validation_test_cases():
    """
    Example test cases, do NOT modify this.
    If your code is correct, calling this function will have no effect.
    """
    case = "Parse a valid HTTP request."
    req_str = "GET / HTTP/1.0\r\nHost: www.google.com\r\n\r\n"

    actual_value = check_http_request_validity(req_str)
    correct_value = HttpRequestState.GOOD
    assert correct_value == actual_value,\
        f"[Line {lineno()}] [failed] {case}"\
        " Expected ( %s ) got ( %s )" % (correct_value, actual_value)
    print(f"[success] {case}")

    #######################################
    #######################################

    case = "Parse an invalid HTTP request (invalid method)"
    req_str = "GOAT / HTTP/1.0\r\nHost: www.google.com\r\n\r\n"

    actual_value = check_http_request_validity(req_str)
    correct_value = HttpRequestState.INVALID_INPUT
    assert correct_value == actual_value,\
        f"[Line {lineno()}] [failed] {case}"\
        " Expected ( %s ) got ( %s )" % (correct_value, actual_value)
    print(f"[success] {case}")

    #######################################
    #######################################

    case = "Parse an invalid HTTP request (not-supported method)"
    req_str = "HEAD / HTTP/1.0\r\nHost: www.google.com\r\n\r\n"

    actual_value = check_http_request_validity(req_str)
    correct_value = HttpRequestState.NOT_SUPPORTED
    assert correct_value == actual_value,\
        f"[Line {lineno()}] [failed] {case}"\
        " Expected ( %s ) got ( %s )" % (correct_value, actual_value)
    print(f"[success] {case}")

    #######################################
    #######################################

    """case = "Parse an invalid HTTP request (relative path with no host header)"
    req_str = "HEAD / HTTP/1.0\r\n\r\n"

    actual_value = check_http_request_validity(req_str)
    correct_value = HttpRequestState.INVALID_INPUT
    assert correct_value == actual_value,\
        f"[Line {lineno()}] [failed] {case}"\
        " Expected ( %s ) got ( %s )" % (correct_value, actual_value)
    print(f"[success] {case}")
"""
    #######################################
    #######################################
    case = "Parse an invalid HTTP request (bad header [no colon, no value])"
    req_str = "HEAD www.google.com HTTP/1.0\r\nAccept \r\n"

    actual_value = check_http_request_validity(req_str)
    correct_value = HttpRequestState.INVALID_INPUT
    assert correct_value == actual_value,\
        f"[Line {lineno()}] [failed] {case}"\
        " Expected ( %s ) got ( %s )" % (correct_value, actual_value)
    print(f"[success] {case}")

    #######################################
    #######################################
    case = "Parse an invalid HTTP request (no HTTP version)"
    req_str = "HEAD / \r\nHost: www.google.com\r\n\r\n"

    actual_value = check_http_request_validity(req_str)
    correct_value = HttpRequestState.INVALID_INPUT
    assert correct_value == actual_value,\
        f"[Line {lineno()}] [failed] {case}"\
        " Expected ( %s ) got ( %s )" % (correct_value, actual_value)
    print(f"[success] {case}")

    #######################################
    #######################################
    case = "GET request with full URL in path returns GOOD"
    req_str = "GET http://google.com/ HTTP/1.0\r\n"

    actual_value = check_http_request_validity(req_str)
    correct_value = HttpRequestState.GOOD
    assert correct_value == actual_value,\
        f"[Line {lineno()}] [failed] {case}"\
        " Expected ( %s ) got ( %s )" % (correct_value.name, actual_value.name)
    print(f"[success] {case}")

    #######################################
    #######################################

    case = "GET request with relative path and host header returns GOOD"
    req_str = "GET / HTTP/1.0\r\nHost: google.com\r\n\r\n"

    actual_value = check_http_request_validity(req_str)
    correct_value = HttpRequestState.GOOD
    assert correct_value == actual_value,\
        f"[Line {lineno()}] [failed] {case}"\
        " Expected ( %s ) got ( %s )" % (correct_value.name, actual_value.name)
    print(f"[success] {case}")

    #######################################
    #######################################

    case = "Relative path without host header returns INVALID_INPUT"
    req_str = "GET / HTTP/1.0\r\n\r\n"

    actual_value = check_http_request_validity(req_str)
    correct_value = HttpRequestState.INVALID_INPUT
    assert correct_value == actual_value,\
        f"[Line {lineno()}] [failed] {case}"\
        " Expected ( %s ) got ( %s )" % (correct_value.name, actual_value.name)
    print(f"[success] {case}")

def pipeline():
    i = 2
    while i > 0:
        client_addr = ("127.0.0.1", 18888)

        # This argument is optional, defaults to 18888
        #proxy_port_number = get_arg(1, 18888)
        #skt = entry_point(proxy_port_number)

    #http://apache.org/

        #req_str = "GET / HTTP/1.0\r\nHost: www.apache.org\r\n"
        req_str = "GET / HTTP/1.0\r\n"
        print(req_str)
        s = socket.socket(socket.AF_INET,
                          socket.SOCK_STREAM)

        host = "127.0.0.1" # or just use (host = '')
        print(host)
        port = 18888

        s.connect((host, port))
        s.send(req_str.encode("ascii"))
        req_str = "Host: www.google.com\r\n\r\n"
        s.send(req_str.encode("ascii"))
        tm = s.recv(1024)  # msg can only be 1024 bytes long
        print(tm)
        s.close()
        print("response: ", tm.decode("ascii"))
        i -= 1

def main():
    ###################
    # Run tests
    ###################
    # Sorted by checklist order, feel free to comment/un-comment
    # any of those functions.
    try:
        simple_http_validation_test_cases()
        simple_http_parsing_test_cases()
        pipeline()
    except AssertionError as e:
        print("Test case failed:\n", str(e))
        exit(-1)


if __name__ == "__main__":
    main()