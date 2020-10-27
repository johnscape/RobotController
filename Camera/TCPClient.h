#pragma once
#include <winsock2.h>
#include <windows.h>
#include <ws2tcpip.h>
#include <stdlib.h>
#include <stdio.h>
#include <string>
#include <queue>
#include <thread>
#include <mutex>

#pragma comment (lib, "Ws2_32.lib")
#pragma comment (lib, "Mswsock.lib")
#pragma comment (lib, "AdvApi32.lib")


class TCPClient
{
public:
	TCPClient(std::string ip, unsigned int targetPort, bool verbose = false, unsigned int width = 512, unsigned int height = 512);
	~TCPClient();

	void Init();
	void Connect();

	void Send(std::string message);
	std::string ReceiveLastMessage();

	void Close();

	void ListenCycle(bool v);

	void SendImage(bool depth);

private:
	WSAData wsadata;
	SOCKET connection;
	struct addrinfo* result, * ptr;

	unsigned int port;
	std::string ipAddress;

	bool initFinished;
	bool verbose;

	std::queue<std::string> messages;
	std::mutex messageLock;

	std::thread* ReadThread;

	unsigned char* colorBuffer;
	unsigned char* depthBuffer;

	unsigned int WinWidth;
	unsigned int WinHeight;
};