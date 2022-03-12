Program consists of two parts: server and client

Client:  
connects to server, 
signs in to server, 
provides server with login and  password for authentication, 
sends message to specific user, 
send  broadcast message.

Server: 
accepts clients connection, 
registers new users, authenticates clients, 
routes messages, 
logs clients activity.

Passwords are stored on server side in db named 
DataBase_for_task_3.db.

Clients and server operate using sockets.

To run server run messenger_server.py.
To run client run run_client.py.