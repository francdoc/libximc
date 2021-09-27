#include "common.h"

// do not force to use DDK with MSVC or other
#ifdef _MSC_VER
#include <winioctl.h>
#include <winsock2.h>
#include <Ws2tcpip.h>
#else
#include <ddk/ntddser.h>
#endif
#include <setupapi.h>
#include <process.h>

#include "ximc-template.h"

#include "ximc-gen-template.h"
#include "util.h"
#include "metadata.h"
#include "platform.h"

#include "protosup.h"

//#include "wrapper.h"

result_t open_udp(device_metadata_t *metadata, const char* ip4_port)
{
	// check parameter ip4_port : address:port

	char saddress[64];
	memset(saddress, 0, 64);
	strncpy(saddress, ip4_port, 64);
	char * port_start = strchr(saddress,':');
	if (port_start == NULL) return result_error;
	USHORT port;
	if (sscanf(port_start, "%ud", &port) != 1) return result_error;
	*port_start = 0;
	ULONG addr = inet_addr(saddress);
	if (addr == INADDR_NONE) return result_error;
 
	// creating a new connection resource

	metadata->handle = (handle_t)socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
	if (metadata->handle == INVALID_SOCKET) return result_error;

	metadata->type = dtUdp;

	SOCKADDR_IN * sa;

	metadata->virtual_state = (sa = (SOCKADDR_IN *)malloc(sizeof(SOCKADDR_IN)));

	sa->sin_family = AF_INET;
	sa->sin_port = htons(port);
	sa->sin_addr.s_addr = addr;
	
	return result_ok;
}

result_t close_udp(device_metadata_t *metadata)
{
	closesocket((SOCKET)metadata->handle);
	free(metadata->virtual_state);
	return result_ok;
}


int write_udp(device_metadata_t *metadata, const byte* command, size_t command_len)
{
	int iResult;
	iResult = sendto((SOCKET)metadata->handle, (const char *)command, command_len, 0, (SOCKADDR *)&metadata->virtual_state, sizeof (SOCKADDR_IN));
	return  (iResult == SOCKET_ERROR) ? 0 : iResult;
}

int read_udp(device_metadata_t *metadata, void *buf, size_t amount)
{
	int iResult;
	int size_1;
	iResult = recvfrom((SOCKET)metadata->handle, (char *)buf, amount, 0, NULL, NULL);
	return  (iResult == SOCKET_ERROR) ? 0 : iResult;
}