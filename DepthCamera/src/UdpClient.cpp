#include "UdpClient.h"
#include <unistd.h>

#include <stdio.h>
#include <WinSock2.h>
#include <Ws2tcpip.h>

#define BUFFER_SIZE 1024

UdpClient::UdpClient(const std::string& addr, int port) : f_port(port), f_address(addr)
{
    /*char decimal_port[16];
    snprintf(decimal_port, sizeof(decimal_port), "%d", f_port);
    decimal_port[sizeof(decimal_port) / sizeof(decimal_port[0]) - 1] = '\0';
    struct addrinfo hints;
    memset(&hints, 0, sizeof(hints));
    hints.ai_family = AF_UNSPEC;
    hints.ai_socktype = SOCK_DGRAM;
    hints.ai_protocol = IPPROTO_UDP;
    int r(getaddrinfo(addr.c_str(), decimal_port, &hints, &f_addrinfo));
    if(r != 0 || f_addrinfo == NULL)
    {
        throw udp_client_server_runtime_error(("invalid address or port: \"" + addr + ":" + decimal_port + "\"").c_str());
    }
    f_socket = socket(f_addrinfo->ai_family, SOCK_DGRAM, IPPROTO_UDP);
    if(f_socket == -1)
    {
        freeaddrinfo(f_addrinfo);
        throw udp_client_server_runtime_error(("could not create socket for: \"" + addr + ":" + decimal_port + "\"").c_str());
    }*/
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
    return text;

}


int UdpClient::close()
{
    closesocket(this->client);
    WSACleanup();
    this->client = 0;
    return 0;
}

