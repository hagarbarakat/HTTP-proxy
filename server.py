# Don't forget to change this file's name before submission.
import sys
import os
import enum
import socket


class HttpRequestInfo(object):
    """
    Represents a HTTP request information
    Since you'll need to standardize all requests you get
    as specified by the document, after you parse the
    request from the TCP packet put the information you
    get in this object.
    To send the request to the remote server, call to_http_string
    on this object, convert that string to bytes then send it in
    the socket.
    client_address_info: address of the client;
    the client of the proxy, which sent the HTTP request.
    requested_host: the requested website, the remote website
    we want to visit.
    requested_port: port of the webserver we want to visit.
    requested_path: path of the requested resource, without
    including the website name.
    NOTE: you need to implement to_http_string() for this class.
    """

    def _init_(self, client_info, method: str, requested_host: str,
               requested_port: int,
               requested_path: str,
               headers: list):
        self.method = method
        self.client_address_info = client_info
        self.requested_host = requested_host
        self.requested_port = requested_port
        self.requested_path = requested_path
        # Headers will be represented as a list of lists
        # for example ["Host", "www.google.com"]
        # if you get a header as:
        # "Host: www.google.com:80"
        # convert it to ["Host", "www.google.com"] note that the
        # port is removed (because it goes into the request_port variable)
        self.headers = headers

    def to_http_string(self):
        """
        Convert the HTTP request/response
        to a valid HTTP string.
        As the protocol specifies:
        [request_line]\r\n
        [header]\r\n
        [headers..]\r\n
        \r\n
        (just join the already existing fields by \r\n)
        You still need to convert this string
        to byte array before sending it to the socket,
        keeping it as a string in this stage is to ease
        debugging and testing.
        """

        print("*" * 50)
        print("[to_http_string] Implement me!")
        print("*" * 50)
        return None

    def to_byte_array(self, http_string):
        """
        Converts an HTTP string to a byte array.
        """
        return bytes(http_string, "UTF-8")

    def display(self):
        print(f"Client:", self.client_address_info)
        print(f"Method:", self.method)
        print(f"Host:", self.requested_host)
        print(f"Port:", self.requested_port)
        stringified = [": ".join([k, v]) for (k, v) in self.headers]
        print("Headers:\n", "\n".join(stringified))


class HttpErrorResponse(object):
    """
    Represents a proxy-error-response.
    """

    def _init_(self, code, message):
        self.code = code
        self.message = message

    def to_http_string(self):
        """ Same as above """
        pass

    def to_byte_array(self, http_string):
        """
        Converts an HTTP string to a byte array.
        """
        return bytes(http_string, "UTF-8")

    def display(self):
        print(self.to_http_string())


class HttpRequestState(enum.Enum):
    """
    The values here have nothing to do with
    response values i.e. 400, 502, ..etc.
    Leave this as is, feel free to add yours.
    """
    INVALID_INPUT = 0
    NOT_SUPPORTED = 1
    GOOD = 2


def entry_point(proxy_port_number):
    """
    Entry point, start your code here.
    Please don't delete this function,
    but feel free to modify the code
    inside it.
    """

    print("*" * 50)
    print("[entry_point] Setup socket")
    print("*" * 50)
    proxy_socket = setup_sockets(proxy_port_number)
    print("*" * 50)
    print("[entry_point] Socket logic")
    print("*" * 50)
    do_socket_logic(proxy_socket)
    return None


def setup_sockets(proxy_port_number):
    """
    Socket logic MUST NOT be written in the any
    class. Classes know nothing about the sockets.
    But feel free to add your own classes/functions.
    Feel free to delete this function.
    """
    print("*" * 50)
    print("[setup_sockets] Starting HTTP proxy on port:", proxy_port_number)

    # Create TCP socket
    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_address = ('127.0.0.1', int(proxy_port_number))
    # Listen on the specified port
    proxy_socket.bind(proxy_address)
    proxy_socket.listen(1024)
    # when calling socket.listen() pass a number
    # that's larger than 10 to avoid rejecting
    # connections automatically.
    print("[setup_sockets] TCP socket is ready !")
    print("*" * 50)
    return proxy_socket


def do_socket_logic(proxy_socket):
    """
    This function should wait and recieve HTTP Requests
    """
    # while True:
    print('[Socket logic] Waiting for connection...')
    client_socket, addres = proxy_socket.accept()
    print(f"[Socket logic] TCP connection has been established with {addres}")
    data = client_socket.recv(1024)
    print(f"[Socket logic] Recieved request from {addres}")
    http_request_pipeline(addres, data)
    client_socket.close()
    proxy_socket.close()
    pass


def http_request_pipeline(source_addr, http_raw_data):
    """
    HTTP request processing pipeline.
    - Validates the given HTTP request and returns
      an error if an invalid request was given.
    - Parses it
    - Returns a sanitized HttpRequestInfo
    returns:
     HttpRequestInfo if the request was parsed correctly.
     HttpErrorResponse if the request was invalid.
    Please don't remove this function, but feel
    free to change its content
    """
    print("*" * 50)
    print("[http_request_pipeline] Enter pipeline...")
    print("*" * 50)
    # Check validity
    validity = check_http_request_validity(http_raw_data)
    if validity == HttpRequestState.GOOD:
        # Parse the whole request
        pass
    else:
        # Return Error response
        pass
    # Return error if needed, then:
    # parse_http_request()
    # sanitize_http_request()
    # Validate, sanitize, return Http object.

    return None


def validate_request_line(request):
    print('[validate request line] ', request)
    tokens = request.split()
    if len(tokens) != 3:
        print('[validate request line] failed, invalid length: ', len(tokens))
        return 'none', HttpRequestState.INVALID_INPUT

    method = tokens[0].upper()
    if method != 'GET':
        if method != 'POST' and method != 'PUT' and method != 'HEAD':
            print("*" * 50)
            print("[check_http_request_validity] INVALID_INPUT")
            print("*" * 50)
            return 'none', HttpRequestState.INVALID_INPUT
        else:
            print("*" * 50)
            print("[check_http_request_validity] NOT_SUPPORTED")
            print("*" * 50)
            return 'none', HttpRequestState.NOT_SUPPORTED

    # validate the http version
    http_version = tokens[2].upper()
    if http_version != 'HTTP/1.0':
        if http_version.split('/')[0] == 'HTTP':
            print("[check_http_request_validity] NOT SUPPORTED HTTP Version")
            return 'none', HttpRequestState.NOT_SUPPORTED
        print("[check_http_request_validity] INVALID INPUT HTTP Version")
        return 'none', HttpRequestState.INVALID_INPUT

    # Validate the url or path
    target = tokens[1].upper()
    if target[0:7] != 'HTTP://' and target[0] != '/':
        print("[check_http_request_validity] INVALID INPUT url")
        return 'none', HttpRequestState.INVALID_INPUT
    else:
        url = target
        if target[0:7] == 'HTTP://':
            url = target[7: len(target)]
        if len(url.split(':')) > 1:
            if not (url.split(':')[1].isnumeric()) or len(url.split(':')) != 2:
                print("[check_http_request_validity] INVALID INPUT port")
                return 'none', HttpRequestState.INVALID_INPUT
        if target[0:7] == 'HTTP://':
            return 'first', HttpRequestState.GOOD
            pass
        if target[0] == '/':
            return 'second', HttpRequestState.GOOD
            pass


def parse_http_request(source_addr, http_raw_data):
    """
    This function parses a "valid" HTTP request into an HttpRequestInfo
    object.
    """
    print("*" * 50)
    print("[parse_http_request] Parsing...")
    print("*" * 50)
    lines = http_raw_data.split('\r\n')
    request_line = lines[0]
    # request_line should be somethin like <method> <path/url> <http version>
    # validate request line
    frmt, status = validate_request_line(request_line)

    # Replace this line with the correct values.
    ret = HttpRequestInfo(None, None, None, None, None, None)
    return ret


def check_http_request_validity(http_raw_data) -> HttpRequestState:
    """
    Checks if an HTTP request is valid
    returns:
    One of values in HttpRequestState
    """
    print("*" * 50)
    print("[check_http_request_validity] Checking validity...")
    print("*" * 50)
    lines = http_raw_data.split('\r\n')
    request_line = lines[0]
    # request_line should be somethin like <method> <path/url> <http version>
    # validate request line
    frmt, status = validate_request_line(request_line)

    if status != HttpRequestState.GOOD:
        return status
    print("*" * 50)
    print("[check_http_request_validity] Request line status : ", status)
    print("*" * 50)
    # validate headers
    # collect all headers in a dict
    headers = {}
    for i in range(1, len(lines) - 2):
        header = lines[i]
        # split on ':'
        # it should have 2 filds , headername : value
        header_elements = header.split(':')
        if len(header_elements) != 2:
            print("[check_http_request_validity] Invalid header : ", header)
            return HttpRequestState.INVALID_INPUT
        headers[header_elements[0].upper()] = header_elements[1].upper()
    print("*" * 50)
    print("[check_http_request_validity] Headers status : ", status)
    print("*" * 50)
    if frmt == 'second':
        # must have host header
        if 'HOST' in headers:
            return HttpRequestState.GOOD
        else:
            return HttpRequestState.INVALID_INPUT

    return HttpRequestState.GOOD


def sanitize_http_request(request_info: HttpRequestInfo):
    """
    Puts an HTTP request on the sanitized (standard) form
    by modifying the input request_info object.
    for example, expand a full URL to relative path + Host header.
    returns:
    nothing, but modifies the input object
    """
    print("*" * 50)
    print("[sanitize_http_request] Implement me!")
    print("*" * 50)


#######################################
# Leave the code below as is.
#######################################


def get_arg(param_index, default=None):
    """
        Gets a command line argument by index (note: index starts from 1)
        If the argument is not supplies, it tries to use a default value.
        If a default value isn't supplied, an error message is printed
        and terminates the program.
    """
    try:
        return sys.argv[param_index]
    except IndexError as e:
        if default:
            return default
        else:
            print(e)
            print(
                f"[FATAL] The comand-line argument #[{param_index}] is missing")
            exit(-1)  # Program execution failed.


def check_file_name():
    """
    Checks if this file has a valid name for submission
    leave this function and as and don't use it. it's just
    to notify you if you're submitting a file with a correct
    name.
    """
    script_name = os.path.basename(_file_)
    import re
    matches = re.findall(r"(\d{4}_){,2}lab2\.py", script_name)
    if not matches:
        print(f"[WARN] File name is invalid [{script_name}]")
    else:
        print(f"[LOG] File name is correct.")


def main():
    """
    Please leave the code in this function as is.
    To add code that uses sockets, feel free to add functions
    above main and outside the classes.
    """
    print("\n\n")
    print("*" * 50)
    print(f"[LOG] Printing command line arguments [{', '.join(sys.argv)}]")
    check_file_name()
    print("*" * 50)

    # This argument is optional, defaults to 18888
    proxy_port_number = get_arg(1, 18888)
    entry_point(proxy_port_number)


if _name_ == "_main_":
    main()