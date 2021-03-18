import socket
import base64
import re
import time

SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8000

ACC_NAME = 'bilkentstu'
ACC_PASS = 'cs421s2021'


class Response:
    def __init__(self, headers, body, statusCode):
        self.headers = headers
        self.body = body
        if statusCode is not None:
            self.statusCode = int(statusCode)
        else:
            self.statusCode = None


def listToString(lines, end='\n', prev=''):
    ret = ''

    for item in lines:
        ret += item + end

    return prev + ret


def writeToFile(fileName, dataToWrite):
    with open(fileName, 'w') as f:
        f.write(dataToWrite)


def parseResponse(response):
    lines = response.split('\r\n')
    # print('\n\n')
    # print(lines)
    headers = []
    body = []

    if '' in lines:
        split = lines.index('')
        headers = lines[: split]
        body = lines[split + 1:]

        try:
            keywords = headers[0].split(' ')
            return Response(headers, body, keywords[1])
        except:
            print('\n\n')
            print(lines)
    else:
        return Response(None, lines[0], None)


def sendAndReceiveResponse(socket, request, my_bytes=1024):
    socket.sendall(bytes(request, 'utf-8'))
    data = socket.recv(my_bytes + 500)
    data = data.decode('utf-8')
    return parseResponse(data)


def executePartA(socket):
    print('Executing part A')
    req = 'GET / HTTP/1.1\r\n'
    req += 'Host: localhost:8000\r\n\r\n'

    response = sendAndReceiveResponse(socket, req)

    data = listToString(response.body)
    writeToFile('index2.html', data)

    link = re.findall('href\=\".*\">', data)[0][6:-2]
    print('Finished executing part A, hidden link is: {}'.format('/' + link))
    return '/' + link


def executePartB(socket, link, authorization=False):
    print('Executing part B')
    req = 'GET {} HTTP/1.1\r\n'.format(link)
    req += 'Host: localhost:8000\r\n'
    if authorization:
        encoded = base64.b64encode('{}:{}'.format(
            ACC_NAME, ACC_PASS).encode('ascii')).decode('ascii')
        req += 'Authorization: Basic {}\r\n\r\n'.format(encoded)
    else:
        req += '\r\n'

    response = sendAndReceiveResponse(socket, req)

    if response.statusCode == 401:
        print('Authentication failed in part B')
    elif response.statusCode == 200:
        writeToFile('protected2.html', listToString(response.body))
        link = re.findall(
            'href\=\".*\">', listToString(response.body))[0][6:-2]
        print('Finished executing part B, hidden link is: {}'.format('/' + link))
        return '/' + link

    return None


def executePartC(socket, link, current_range):
    req = 'HEAD {}\r\n'.format(link)
    req += 'Host: localhost:8000\r\n\r\n'

    response = sendAndReceiveResponse(socket, req)

    code_length = int(response.headers[2].split(' ')[1])

    prev = 0
    message = ''

    start_time = time.time()
    while prev < code_length:
        req = ''
        req = 'GET {} HTTP/1.1\r\n'.format(link)
        req += 'Host: localhost:8000\r\n'
        req += 'Range: bytes={}-{}\r\n\r\n'.format(
            prev, min(prev + current_range, code_length))

        response = sendAndReceiveResponse(socket, req, current_range)
        message = listToString(response.body, end='', prev=message)

        prev += current_range

    end_time = time.time()
    print("Total time in seconds:")
    print(end_time - start_time)

    writeToFile('test.txt', message)
    return None


def pr(response):
    print('\n\n')
    print('Header', response.headers)
    print('Body', response.body)
    print('SC', response.statusCode)


def exitProgram(socket):
    req = 'EXIT HTTP/1.1\r\n'
    req += 'Host: localhost:8000\r\n\r\n'
    socket.sendall(bytes(req, 'utf-8'))


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((SERVER_HOST, SERVER_PORT))

    hiddenLink = executePartA(s)

    executePartB(s, hiddenLink, False)
    hiddenLink = executePartB(s, hiddenLink, True)

    executePartC(s, hiddenLink, 100)

    exitProgram(s)
