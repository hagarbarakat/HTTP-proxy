# Don't forget to change this file's name before submission.
import sys
import os
import enum
import re
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

    def __init__(self, client_info, method: str, requested_host: str,
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
        """GET / HTTP/1.0
        Host: eng.alexu.edu.eg
        """
        #self.display()
        string = self.method + " / HTTP/1.0\r\n"
        for i in range(len(self.headers)):
            for j in range(len(self.headers[i])):
                if j == 0:
                    string += self.headers[i][j] + ": "
                else:
                    string += self.headers[i][j]
            string += "\r\n"
        string += "\r\n"
        print(string)
        print("*" * 50)
        print("[to_http_string] Implement me!")
        print("*" * 50)
        return string

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

    def __init__(self, code, message):
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
    PLACEHOLDER = -1


def entry_point(proxy_port_number):
    """
    Entry point, start your code here.
    Please don't delete this function,
    but feel free to modify the code
    inside it.
    """

    setup_sockets(proxy_port_number)
    print("*" * 50)
    print("[entry_point] Implement me!")
    print("*" * 50)
    return None


def setup_sockets(proxy_port_number):
    """
    Socket logic MUST NOT be written in the any
    class. Classes know nothing about the sockets.
    But feel free to add your own classes/functions.
    Feel free to delete this function.
    """
    print("Starting HTTP proxy on port:", proxy_port_number)

    # when calling socket.listen() pass a number
    # that's larger than 10 to avoid rejecting
    # connections automatically.
    print("*" * 50)
    print("[setup_sockets] Implement me!")
    print("*" * 50)
    return None


def do_socket_logic():
    """
    Example function for some helper logic, in case you
    want to be tidy and avoid stuffing the main function.
    Feel free to delete this function.
    """
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
    # Parse HTTP request
    validity = check_http_request_validity(http_raw_data)
    # Return error if needed, then:
    # parse_http_request()
    # sanitize_http_request()
    # Validate, sanitize, return Http object.
    print("*" * 50)
    print("[http_request_pipeline] Implement me!")
    print("*" * 50)
    return None


def parse_http_request(source_addr, http_raw_data):
    """
    This function parses a "valid" HTTP request into an HttpRequestInfo
    object.
    """
    splitt = re.split("[\s\n]",http_raw_data)
    if splitt[1] == '/':
        header = []
        method = splitt[0]
        path = splitt[1]
        version = splitt[2]
        host = splitt[5]
        list = ["Host", splitt[5]]
        header.append(list)
        if "Accept:" in splitt:
            list = ["Accept", splitt[splitt.index("Accept:") + 1]]
            header.append(list)
        if ":" in splitt[splitt.index(host)+1]:
            port = re.split(":",splitt[splitt.index(host)+1])
            port = port[1]
        else:
            port = "80"

    else:
        header = []
        method = splitt[0]
        path = splitt[1]
        version = splitt[2]
        host = splitt[1]
        if ":" in splitt[splitt.index(path)]:
            port = re.split(":", splitt[splitt.index(path)])
            port = port[1]
        else:
            port = "80"
        list = ["Host", splitt[1]]
        header.append(list)
        if "Accept:" in splitt:
            list = ["Accept", splitt[splitt.index("Accept:") + 1]]
            header.append(list)
    print(splitt)
    print("*" * 50)
    print("[parse_http_request] Implement me!")
    print("*" * 50)
    # Replace this line with the correct values.
    ret = HttpRequestInfo(http_raw_data, method, host, int(port), path, header)
    return ret


def check_http_request_validity(http_raw_data) -> HttpRequestState:
    """
    Checks if an HTTP request is valid
    returns:
    One of values in HttpRequestState
    """
    splitt = re.split("[\s\n]", http_raw_data)
    if splitt[1] == "/":
        print("type 1")
        return check(splitt, 1)
    else:
        return check(splitt, 2)
    print("*" * 50)
    print("[check_http_request_validity] Implement me!")
    print("*" * 50)
    return HttpRequestState.GOOD #(for example)
    #return HttpRequestState.PLACEHOLDER

def check(splitt, type):
    list = ["GET","HEAD","PUT","DELETE"]
    if splitt[0] not in list:
        return HttpRequestState.INVALID_INPUT
    if "HTTP/1.0" not in splitt:
        return HttpRequestState.INVALID_INPUT
    if "Host:" not in splitt and type == 1:
        return HttpRequestState.INVALID_INPUT
    #TODO : no colon no value
    if "Accept" in splitt:
        return HttpRequestState.INVALID_INPUT
    if "Accept:" in splitt:
        index = splitt.index("Accept:")+1
        if splitt[index] == " ":
            return HttpRequestState.INVALID_INPUT
    if splitt[0] != "GET" and splitt[0] in list:
        return  HttpRequestState.NOT_SUPPORTED
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
            exit(-1)    # Program execution failed.


def check_file_name():
    """
    Checks if this file has a valid name for *submission*
    leave this function and as and don't use it. it's just
    to notify you if you're submitting a file with a correct
    name.
    """
    script_name = os.path.basename(__file__)
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


if __name__ == "__main__":
    main()