import socket

SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8000


def listToString(lines):
    ret = ''

    for item in lines:
        ret += item + '\n'

    return ret


def parseResponse(response):
    lines = response.split('\n')
    headers = []
    body = []

    isHeader = True
    for line in lines:
        if line == '\n':
            isHeader = False
            continue

        if isHeader:
            headers.append(line)
        else:
            b

    keywords = headers[0].split(' ')
    keywords[0] ==


def sendAndReceiveResponse(socket, request):
    socket.sendall(bytes(request, 'utf-8'))
    data = socket.recv(1024)
    data = data.decode('utf-8')
    return parseResponse(data)


def executePartA(socket):
    req = 'GET / HTTP/1.1\r\n'
    req += 'Host: localhost:8000\r\n\r\n'

    data = sendAndReceiveResponse(socket, req)
    lines = data.split('\n')
    lines = lines[2:]

    data = listToString(lines)
    with open('index2.html', 'w') as f:
        f.write(data)

    return


def executePartB():
    return


def executePArtC():
    return


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((SERVER_HOST, SERVER_PORT))

    executePartA(s)
    #req = 'GET / HTTP/1.1\r\n'
    #req += 'Host: localhost:8000\r\n\r\n'

    #s.sendall(bytes(req, 'utf-8'))
    #data = s.recv(1024)

    #data = data.decode('utf-8')

    # print(data)

    #lines = data.split('\n')
    #lines = lines[2:]

    #data = listToString(lines)

    # print(lines)

    # with open('index2.html', 'w') as f:
    #  f.write(data)

    req = 'GET /protected.html HTTP/1.1\r\n'
    req += 'Host: localhost:8000 \r\n\r\n'

    s.sendall(bytes(req, 'utf-8'))
    data = s.recv(1024)

    data = data.decode('utf-8')
    print(data)

    lines = data.split('\n')
    lines = lines[2:]

    data = listToString(lines)
    print(data)

    req = 'EXIT HTTP/1.1\r\n'
    req += 'Host: localhost:8000 \r\n\r\n'

    s.sendall(bytes(req, 'utf-8'))
