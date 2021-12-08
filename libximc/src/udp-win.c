#include "common.h"

// do not force to use DDK with MSVC or other
#ifdef _MSC_VER
#include <winioctl.h>
#include <winsock2.h>
#include <Ws2tcpip.h>

/*
#include <ddk/ntddser.h>
#include <setupapi.h>
#include <process.h>
*/
#include "ximc.h"

//#include "ximc-gen.h"
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
	strncpy_s(saddress, 64, ip4_port, strlen(ip4_port));
	char * port_start = strchr(saddress,':');
	if (port_start == NULL) return result_error;
	unsigned int port;
	if (sscanf_s(port_start+1, "%ud", &port) != 1) return result_error;
	*port_start = 0;
	ULONG addr = inet_addr(saddress);
	if (addr == INADDR_NONE) return result_error;
 
 // init actions to init some windows dll with udp from Microsoft example  
	unsigned short wVersionRequested;
	WSADATA wsaData;
	int err;

	/* Use the MAKEWORD(lowbyte, highbyte) macro declared in Windef.h */
	wVersionRequested = MAKEWORD(2, 2);

	err = WSAStartup(wVersionRequested, &wsaData);
	if (err != 0) {
		/* Tell the user that we could not find a usable */
		/* Winsock DLL.                                  */
		//printf("WSAStartup failed with error: %d\n", err);
		return result_error;
	}

	/* Confirm that the WinSock DLL supports 2.2.*/
	/* Note that if the DLL supports versions greater    */
	/* than 2.2 in addition to 2.2, it will still return */
	/* 2.2 in wVersion since that is the version we      */
	/* requested.                                        */

	if (LOBYTE(wsaData.wVersion) != 2 || HIBYTE(wsaData.wVersion) != 2) {
		/* Tell the user that we could not find a usable */
		/* WinSock DLL.                                  */
		//printf("Could not find a usable version of Winsock.dll\n");
		WSACleanup();
		return result_error;
	}
	
  
	// creating a new connection resource

	metadata->handle = (handle_t)socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
	if ((SOCKET)metadata->handle == INVALID_SOCKET) return result_error;

	// устанавлмваем опцию сокета
	int OptVal = 1;
	int OptLen = sizeof(int);

	int rez = setsockopt((SOCKET)metadata->handle, SOL_SOCKET, SO_REUSEADDR, (const char*)&OptVal, OptLen);
	if (rez == SOCKET_ERROR)
	{
		return result_error;
	}

	metadata->type = dtUdp;

	SOCKADDR_IN * sa;

	metadata->virtual_state = (sa = (SOCKADDR_IN *)malloc(sizeof(SOCKADDR_IN)));

	sa->sin_family = AF_INET;
	sa->sin_port = htons((USHORT)(port));
	sa->sin_addr.s_addr = addr;
	
	return result_ok;
}

result_t close_udp(device_metadata_t *metadata)
{
	closesocket((SOCKET)metadata->handle);
	free(metadata->virtual_state);
	// free some windows dll
	WSACleanup();
	return result_ok;
}


int write_udp(device_metadata_t *metadata, const byte* command, size_t command_len)
{
	int iResult;
	iResult = sendto((SOCKET)metadata->handle, (const char *)command, (int)command_len, 0, (SOCKADDR *)metadata->virtual_state, (int) sizeof (SOCKADDR_IN));
	return  (iResult == SOCKET_ERROR) ? 0 : iResult;
}

int read_udp(device_metadata_t *metadata, void *buf, size_t amount)
{
	int iResult;
	iResult = recvfrom((SOCKET)metadata->handle, (char *)buf, (int)amount, 0, NULL, NULL);
	return  (iResult == SOCKET_ERROR) ? 0 : iResult;
}

#endif