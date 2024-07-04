import ntpath
import socket
import http.server
import re


def parse_request(request):
    method, source, *_ = request.split('\r\n')
    method = method.split()[0]
    host_line = re.search(r'Host: ([\d.]+):(\d+)', request)
    ip = "'"+host_line.group(1)+"'"
    port = int(host_line.group(2))
    return method, ip, port


def get_response_status(request, status_code):
    if 'status=' in request:
        status_param = request.split('status=')[1].split()[0]
        if status_param.isdigit():
            try:
                status_code = int(status_param)
                status_msg = http.server.BaseHTTPRequestHandler.responses[status_code][0]
            except (ValueError, KeyError):
                status_code = 200
                status_msg = 'OK'
        else:
            status_code = 200
            status_msg = 'OK'
    else:
        status_msg = http.HTTPStatus(status_code).phrase

    return status_code, status_msg


def build_response(method, ip, port, s_code, s_msg, headers):
    response_headers = []
    response_headers.append(f"Request Method: {method}")
    response_headers.append(f"Request Source: ({ip}, {port})")
    response_headers.append(f"Request Status: {s_code}, {s_msg}")
    for header, value in headers.items():
        response_headers.append(f"{header}: {value}")
    response = '\n'.join(response_headers)
    return response


def echo_server(host='192.168.0.104', port=15000):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen(1)

        print(f"Server started at {host}:{port}")

        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Connection from {client_address} established.")
            with client_socket:
                request = client_socket.recv(1024).decode()

                method, ip, port = parse_request(request)
                s_code, s_msg = get_response_status(request, 200)

                headers = dict(re.findall(r'(.*): (.*)\n', request))
                response = build_response(method, ip, port, s_code, s_msg, headers)
                client_socket.send(
                    bytes('HTTP/1.1 {} {}\r\n'.format(s_code, s_msg),
                          'utf-8'))
                client_socket.send(b'Content-Type: text/plain\r\n')
                client_socket.send(b'\r\n')
                client_socket.send(bytes(response, 'utf-8'))
                client_socket.close()


if __name__ == '__main__':
    echo_server()
