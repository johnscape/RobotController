#include "UdpClient.h"
#include <unistd.h>

#include <stdio.h>
#include <WinSock2.h>
#include <Ws2tcpip.h>

#define BUFFER_SIZE 1024

//linker: -lws2_32

UdpClient::UdpClient(const std::string& addr, int port) : f_port(port), f_address(addr)
{
    WSAStartup(MAKEWORD(2, 0), &wsaData);
    memset(&address, 0, sizeof(address));
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = inet_addr(f_address.c_str());
    address.sin_port = htons(f_port);
    this->client = socket(PF_INET, SOCK_DGRAM, IPPROTO_UDP);
}

UdpClient::~UdpClient()
{
    if (client)
        close();
}

int UdpClient::send(const char* msg, size_t s)
{
    if (!client)
        return 1;
    return sendto(client, msg, s, 0, (struct sockaddr *)&address, sizeof(address));
}

std::string UdpClient::receive()
{
    char buffer[BUFFER_SIZE];
    int siz = sizeof(address);
    int n = recvfrom(client, (char*)buffer, BUFFER_SIZE, 0, (struct sockaddr *)&address, &siz);
    buffer[n] = '\0';
    std::string text = "";
    int i = 0;
    while (buffer[i] != '\0')
    {
        text += buffer[i];
        i++;
    }
    text += '\0';
    return text;

}


int UdpClient::close()
{
    closesocket(this->client);
    WSACleanup();
    this->client = 0;
    return 0;
}

