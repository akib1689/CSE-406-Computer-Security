# import the socket
import socket

from router import Router

# create a socket object
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# port number
port = 5086

# bind to the port
serversocket.bind(('localhost', port))

# queue up to 5 requests
serversocket.listen(5)

while True:
    # establish a connection
    clientsocket, addr = serversocket.accept()

    print("Got a connection from %s" % str(addr))

    # extract the path
    path = clientsocket.recv(1024).decode()
    print("path: ", path)

    # print the path
    # print("path: ", path)

    # create the router
    router = Router(clientsocket, path)

    # send a default dummy response
    router.route()
