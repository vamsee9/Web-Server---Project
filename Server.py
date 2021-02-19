import socket
import os

HOST, PORT = 'localhost', 9995
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
print(f'Access:http://{HOST}:{PORT}')
while True:
    connection, address = s.accept()
    request = connection.recv(1024).decode('utf-8')
    temp_string = request.split(' ')  # Split request
    method = temp_string[0]
    requesting_file = temp_string[1]
    print('Client request ', requesting_file)
    # After the "?" symbol not relevent here
    myfile = requesting_file.split('?')[0]
    myfile = myfile.lstrip('/')
    if(myfile == ''):
        myfile = 'index.html'  # Index file is default
    try:
        if(".html" not in myfile):
            header = 'HTTP/1.1 415 Unsupported Media Type\n\n'
            response = '<html><body><center><h2>Error 415: Unsupported Media Type</h2></center></body></html>'.encode('utf-8')
        if(myfile == "a.html"):
            header = 'HTTP/1.1 403 Forbidden pages\n\n'
            response = '<html><body><center><h2>Error 403: Forbidden Pages</h2></center></body></html>'.encode('utf-8')
        elif(myfile != "index.html"):
            header = 'HTTP/1.1 400 Bad Request\n\n'
            response = '<html><body><center><h2>Error 400: Bad Request </h2></center></body></html>'.encode('utf-8')
        else:
            header = 'HTTP/1.1 200 OK\n\n'
            file = open(myfile, 'rb')
            response = file.read()
            file.close()
           
    except Exception as e:
        header = 'HTTP/1.1 404 Not Found\n\n'
        response = '<html><body><center><h2>Error 404: File not found</h2><p>Python HTTP Server</p></center></body></html>'.encode('utf-8')
    endresponse = header.encode('utf-8')
    endresponse += response
    connection.send(endresponse)
    connection.close()

