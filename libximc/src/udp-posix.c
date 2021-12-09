#include "common.h"

#include <stdio.h>

#include<stdio.h>	
#include<string.h>    
#include<stdlib.h>    
#include<unistd.h>

#include<arpa/inet.h>
#include<sys/socket.h>

#ifdef HAVE_LOCKS
#include <semaphore.h>
#endif

#include "ximc.h"
#include "util.h"
#include "metadata.h"
#include "platform.h"

#include "protosup.h"
#include "wrapper.h"

#ifdef STRERROR_R_CHAR_P
#error GNU variant of strerror_r is not supported
#endif

#ifdef __APPLE__
/* We need IOKit */
#include <CoreFoundation/CoreFoundation.h>
#include <IOKit/IOKitLib.h>
#include <IOKit/usb/IOUSBLib.h>
#include <sys/sysctl.h>
/* and time too */
#include <mach/clock.h>
#include <mach/mach.h>
#endif


/*
 * Udp support
 */

result_t open_udp(device_metadata_t *metadata, const char* ip4_port)
{

	// check parameter ip4_port : address:port
	char saddress[64];
	memset(saddress, 0, 64);
	strncpy(saddress, ip4_port, strlen(ip4_port));
	char * port_start = strchr(saddress, ':');
	if (port_start == NULL) return result_error;
	unsigned int port;
	if (sscanf(port_start + 1, "%ud", &port) != 1) return result_error;
	*port_start = 0;
	in_addr_t addr = inet_addr(saddress);
	if (addr == INADDR_NONE) return result_error;

	// creating a new connection resource

	metadata->handle = (uint32_t)socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
	if ((int)metadata->handle == -1) return result_error;

	// setting  socket option
	int OptVal = 1;
	int OptLen = sizeof(int);

	int rez = setsockopt((int)metadata->handle, SOL_SOCKET, SO_REUSEADDR, (const char*)&OptVal, OptLen);
	if (rez == -1)
	{
		return result_error;
	}

	metadata->type = dtUdp;

	sockaddr_in * sa;

	metadata->virtual_state = (sa = (sockaddr_in*)malloc(sizeof(sockaddr_in)));

	sa->sin_family = AF_INET;
	sa->sin_port = htons((port));
	sa->sin_addr.s_addr = addr;

	return result_ok;

}

result_t close_udp(device_metadata_t *metadata)
{
	close((int)metadata->handle);
	free(metadata->virtual_state);
	return result_ok;
}


int write_udp(device_metadata_t *metadata, const byte* command, size_t command_len)
{
	int iResult;
	iResult = (int)sendto((int)metadata->handle, (const char *)command, (int)command_len, 0, (sockaddr *)metadata->virtual_state, (socklen_t) sizeof (sockaddr_in));
	return  (iResult == -1) ? 0 : iResult;
}

int read_udp(device_metadata_t *metadata, void *buf, size_t amount)
{
	int iResult;
	iResult = (int)recvfrom((int)metadata->handle, (char *)buf, (int)amount, 0, NULL, NULL);
	return  (iResult == -1) ? 0 : iResult;
}

