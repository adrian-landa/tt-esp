import requests


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


if __name__ == '__main__':
    download_file('http://192.168.100.98:8000/media/testRequest/testRequest.gif')
