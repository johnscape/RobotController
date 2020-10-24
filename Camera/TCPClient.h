#pragma once
#include <stdio.h> 
#ifdef __WIN32__
# include <winsock2.h>
#else
# include <sys/socket.h>
#endif
#include <arpa/inet.h> 
#include <unistd.h> 
#include <string.h> 
class TCPClient
{
public:
	TCPClient();
	~TCPClient();
	bool IsConnected();

private:
	bool Connected;

};

