# Socket-2ndSem-20.21
### General Information
This is a project called Live-score socket using TCP protocol which is a title from Computer Networking subject.
All is run by Python 3, using socket, threading and some other basic library such as requests for getting live-score API and json to save file.

## Connect
- Implement a basic TCP connection, allowing n clients to connect through different threads to the server but not limited to n.
- Do not place clients and servers at different hosts.
## Manage connections
- 1 client loses connection, server and other clients do not crash when using multithreading (multithreading).
## Log in
In previous version, the https://github.com/HMy2912/socket_save12042021 version:
  - The client logs in normally with fixed user data in the json file, processed in the server and printed to the server's console, but not yet displayed on the client interface.
In this version, the log in have not done yet, due to the crash after connecting files.
## Registration
- There's an error. Therefore, this feature is not available.
- Idea: when registering, enter the username and password, the client sends this information to the server, the server saves it in a json file, then the client returns to the normal login interface.
## View match list
- The list of matches can be exported thanks to the API reference on livescore.com. Use the registered API link using the requests library to get a json file of data from it and output a list of information.
## View information about a match
-	Unfinished.
## Database Management
- Stored mainly in fixed json file get from the requests library to get the json and then extract it to dictionaries or lists.
## Exit
- There is a disconnect button (DISCONNECT) for each client.
- The server has not been disconnected yet.
## Display
- There is no interface for the server, only for the client using the tkinter library.

### Teacher Requirements
![image](https://user-images.githubusercontent.com/67527838/119859847-f2a9ef00-bf3f-11eb-8271-d82012e51ed3.png)
