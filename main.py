import socket

SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8000

def listToString(lines):
  ret = ''

  for item in lines:
    ret += item + '\n'
  
  return ret

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((SERVER_HOST, SERVER_PORT))

    req = 'GET / HTTP/1.1\r\n'
    req += 'Host: localhost:8000\r\n\r\n'

    s.sendall(bytes(req, 'utf-8'))
    data = s.recv(1024)
    
    data = data.decode('utf-8')

    # print(data)

    lines = data.split('\n')
    lines = lines[2:]

    data = listToString(lines)

    # print(lines)

    with open('index2.html', 'w') as f:
      f.write(data)