network_tools
=============

#Codefellows network tools

##Modules included:
  - An echo server/client
  - A simple HTTP server

##Echo Server
  - The server takes no arguments, and must be started manually in its own terminal. 
  - It will receive a message from a client. 
  - It has a 32-byte buffer.
  - It reassembles the message, and returns the string to the client.
  - It returns the complete message. 

##Echo Client
  - The client takes one argument: `message`. 
  - The client must be started in a separate terminal from the server. 
  - The client checks the type of `message`.
  - If `message` is unicode, the client encodes it to UTF-8.
  - It sends the encoded message to the server and waits for a response. 
  - It receives the response with a 32-byte buffer. 
  - It reassembles the response and returns it. 

##HTTP Server
  - The server takes no arguments, and must be started manually in its own terminal. 
  - It will listen for a connection request. 
  - It will parse the request to ensure that it's valid. 
  - It will return the appropriate HTTP response. 

*Note: Both servers and the client listen/send to 127.0.0.1:50000. They are all opened with:*
    `socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)`

