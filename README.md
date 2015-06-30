#Chat Application#

---

###A simple python chat application which support multiple client.

##Implementation

---

####Server class:
        It is server class of chat application which accept connections from multiple
        clients. It asynchronously receives the message from all client and broadcast 
        it to all the other clients

####Client class:
        Client class of chat application. It connects to the server and it asynchronously
        listen from server and standard input and pass the message to the server.


##Usage

---

`usage client.py Clinet-Name Handle Server-Password Server-IP Server-PORT`

`usage server.py Server-Password`


##Includes

---

1. server.py : server class to

2. file.lz77 : Compressed file. size: 9,033 bytes