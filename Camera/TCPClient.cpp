#include "TCPClient.h"
#include <iostream>
#include <sstream>
#include <glad/glad.h>
#include <GLFW/glfw3.h>

#define BUFFER_SIZE 1024

TCPClient::TCPClient(std::string ip, unsigned int targetPort, bool verbose, unsigned int width, unsigned int height) :
	result(nullptr), ptr(nullptr), ipAddress(ip), port(targetPort), verbose(verbose), ReadThread(nullptr), WinWidth(width), WinHeight(height)
{
	colorBuffer = new unsigned char[3 * width * height];
	depthBuffer = new unsigned char[width * height];
	Init();
}

TCPClient::~TCPClient()
{
	Close();
	delete[] colorBuffer;
	delete[] depthBuffer;
}

void TCPClient::Init()
{
	initFinished = false;

	connection = INVALID_SOCKET;
	struct addrinfo hints;

	if (WSAStartup(MAKEWORD(2, 2), &wsadata) != 0)
	{
		std::cout << "WSAStartup failed!" << std::endl;
		return;
	}

	ZeroMemory(&hints, sizeof(hints));
	hints.ai_family = AF_UNSPEC;
	hints.ai_socktype = SOCK_STREAM;
	hints.ai_protocol = IPPROTO_TCP;

	std::stringstream ss;
	ss << port;

	if (getaddrinfo(ipAddress.c_str(), ss.str().c_str(), &hints, &result) != 0)
	{
		std::cout << "getaddrinfo failed" << std::endl;
		WSACleanup();
		return;
	}

	initFinished = true;
}

void TCPClient::Connect()
{
	if (verbose)
		std::cout << "Connecting to " << ipAddress << ":" << port << std::endl;
	if (!initFinished)
	{
		std::cout << "Initialization is not finished, cannot connect." << std::endl;
		return;
	}
	connection = socket(result->ai_family, result->ai_socktype, result->ai_protocol);
	if (connection == SOCKET_ERROR)
	{
		std::cout << "The socket is invalid. Closing." << std::endl;
		closesocket(connection);
		connection = INVALID_SOCKET;
		return;
	}

	if (connect(connection, result->ai_addr, (int)result->ai_addrlen) == SOCKET_ERROR)
	{
		std::cout << "Socket error: " << WSAGetLastError() << std::endl;
		closesocket(connection);
		connection = INVALID_SOCKET;
		return;
	}

	if (verbose)
		std::cout << "Connected to " << ipAddress << ":" << port << std::endl;

	//std::thread readc([this] {this->ListenCycle(true); });
	if (!ReadThread)
		ReadThread = new std::thread([this] {this->ListenCycle(true); });
}

void TCPClient::Send(std::string message)
{
	char msg[BUFFER_SIZE];
	unsigned int pos = 0;
	bool error = false;
	while (pos < message.size())
	{
		for (size_t i = 0; i < BUFFER_SIZE; i++)
		{
			if (i + pos >= message.size())
				msg[i] = 0;
			else
				msg[i] = message[i + pos];
		}

		pos += BUFFER_SIZE;

		if (send(connection, msg, BUFFER_SIZE, 0) == SOCKET_ERROR)
		{
			std::cout << "Message part sending was a failure." << std::endl;
			error = true;
		}
		else if (verbose)
			std::cout << "Message part sent successfully." << std::endl;
	}

	if (error)
		std::cout << "Error while sending message." << std::endl;
	else if (verbose)
		std::cout << "Message sent successfully." << std::endl;
}

std::string TCPClient::ReceiveLastMessage()
{
	std::string msg = "";
	messageLock.lock();
	if (messages.size() > 0)
	{
		msg = messages.front();
		messages.pop();
	}
	messageLock.unlock();
	return std::string();
}

void TCPClient::Close()
{
	Send("close");
	if (ReadThread)
		ReadThread->join();
	std::cout << "joined" << std::endl;
	closesocket(connection);
	WSACleanup();
}

void TCPClient::ListenCycle(bool v)
{
	int res = 1;
	char buffer[BUFFER_SIZE];
	while (res > 0)
	{
		if (v)
			std::cout << "Waiting for message..." << std::endl;
		res = recv(connection, buffer, BUFFER_SIZE, 0);
		if (res > 0)
		{
			if (v)
				std::cout << "Message reveived!" << std::endl;
			std::string msg;
			for (size_t i = 0; i < BUFFER_SIZE; i++)
			{
				if (buffer[i] != 0)
					msg += buffer[i];
			}
			messageLock.lock();
			messages.push(msg);
			messageLock.unlock();
		}
		else if (res == 0)
			std::cout << "Connection closed." << std::endl;
		else
			std::cout << "Error while receiving: " << WSAGetLastError() << std::endl;
	}
}

void TCPClient::SendImage(bool depth)
{
	if (depth)
	{
		//TODO: implement LZW
		glReadPixels(0, 0, WinWidth, WinHeight, GL_DEPTH_COMPONENT, GL_UNSIGNED_BYTE, depthBuffer);
		std::string s;
		for (size_t i = 0; i < WinWidth * WinHeight; i++)
			s += depthBuffer[i];
		Send(s);
	}
	else
	{
		glReadPixels(0, 0, WinWidth, WinHeight, GL_RGB, GL_UNSIGNED_BYTE, colorBuffer);
		std::string s;
		for (size_t i = 0; i < WinWidth * WinHeight * 3; i++)
			s += depthBuffer[i];
		Send(s);
	}
}
