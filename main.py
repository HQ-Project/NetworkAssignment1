import socket
import base64
import re

SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8000

ACC_NAME = 'bilkentstu'
ACC_PASS = 'cs421s2021'


class Response:
    def __init__(self, headers, body, statusCode):
        self.headers = headers
        self.body = body
        self.statusCode = int(statusCode)


def listToString(lines):
    ret = ''

    for item in lines:
        ret += item + '\n'

    return ret


def writeToFile(fileName, dataToWrite):
    with open(fileName, 'w') as f:
        f.write(dataToWrite)


def parseResponse(response):
    lines = response.split('\r\n')
    headers = []
    body = []

    split = lines.index('')
    headers = lines[: split]
    body = lines[split + 1:]

    keywords = headers[0].split(' ')
    return Response(headers, body, keywords[1])


def sendAndReceiveResponse(socket, request):
    socket.sendall(bytes(request, 'utf-8'))
    data = socket.recv(1024)
    data = data.decode('utf-8')
    return parseResponse(data)


def executePartA(socket):
    req = 'GET / HTTP/1.1\r\n'
    req += 'Host: localhost:8000\r\n\r\n'

    response = sendAndReceiveResponse(socket, req)

    data = listToString(response.body)
    writeToFile('index2.html', data)

    link = re.findall('\".*html\"', data)[0][1:-1]
    return '/' + link


def executePartB(socket, link, authorization=False):
    req = 'GET {} HTTP/1.1\r\n'.format(link)
    req += 'Host: localhost:8000\r\n'
    if authorization:
        encoded = base64.b64encode('{}:{}'.format(
            ACC_NAME, ACC_PASS).encode('ascii')).decode('ascii')
        req += 'Authorization: Basic {}\r\n\r\n'.format(encoded)

    response = sendAndReceiveResponse(socket, req)

    if response.statusCode == 401:
        print('Authentication failed')
    elif response.statusCode == 200:
        writeToFile('protected2.html', listToString(response.body))

    return None


def executePArtC():
    return


def exitProgram(socket):
    req = 'EXIT HTTP/1.1\r\n'
    req += 'Host: localhost:8000 \r\n\r\n'
    socket.sendall(bytes(req, 'utf-8'))


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((SERVER_HOST, SERVER_PORT))

    hiddenLink = executePartA(s)
    print(hiddenLink)

    executePartB(s, hiddenLink, False)
    executePartB(s, hiddenLink, True)

    # req = 'GET /protected.html HTTP/1.1\r\n'
    # req += 'Host: localhost:8000 \r\n\r\n'

    # s.sendall(bytes(req, 'utf-8'))
    # data = s.recv(1024)

    # data = data.decode('utf-8')
    # print(data)

    # lines = data.split('\n')
    # lines = lines[2:]

    # data = listToString(lines)
    # print(data)

    exitProgram(s)
