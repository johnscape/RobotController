#ifndef UDPCLIENT_H
#define UDPCLIENT_H

#define _WIN32_WINNT 0x0501

#include <string>
#include <winsock2.h>
#include <ws2tcpip.h>
#include <stdexcept>

class udp_client_server_runtime_error : public std::runtime_error
{
public:
    udp_client_server_runtime_error(const char *w) : std::runtime_error(w) {}
};

class UdpClient
{
    public:
        UdpClient(const std::string& addr, int port);
        virtual ~UdpClient();

        int send(const char* msg, size_t size);
        std::string receive();
        int close();

    private:
        int client;
        struct sockaddr_in address;
        WSADATA wsaData;
        char data;
        int f_port;
        std::string f_address;
};

#endif // UDPCLIENT_H
