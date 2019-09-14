import requests
import socket


def download_file(url):
    with requests.get(url, stream=True) as request:
        local_file = url.split('/')[-1]
        request.raise_for_status()
        with open(local_file, 'wb') as file:
            for chunk in request.iter_content(chunk_size=512):
                if chunk:
                    file.write(chunk)
    print(request.status_code)
    print(request.headers)


def download_file_socket(host, path, port=80):
    file_name = path.split('/')[-1]
    headers_limit = '\r\n\r\n'.encode('ascii')
    has_headers_ended = False
    request = 'GET {0} HTTP/1.0\r\nHost:{1}\r\n\r\n'.format(path, host)
    socket_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_connection.connect((host, port))
    socket_connection.send(request.encode('ascii'))
    file = open(file_name, 'wb')
    while True:
        data = socket_connection.recv(1024)
        if not data:
            break
        else:
            response = data.split(headers_limit)
            if len(response) > 1:
                has_headers_ended = True
            if has_headers_ended:
                file.write(response[-1])
    file.close()
    socket_connection.close()


if __name__ == '__main__':
    content = "/media/testRequest/testRequest.bin"
    download_file_socket('192.168.100.98', content, 8000)
