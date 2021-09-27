#ifndef UDP_WIN_H
#define UDP_WIN_H

#include "ximc-template.h"
#include "metadata.h"


/**
* Opens UDP-socket as a client
* Assumes host contains as follows: just an IP-address
* port contains port
*/
extern result_t open_udp(device_metadata_t *metadata, const char* host, USHORT port, const char* serial);

/**
Closes previuosly opened UDP socket and removes all metadata associated
*/
extern result_t close_udp(device_metadata_t *metadata);

/**
* Writes to UDP socket

*/
extern int write_udp(device_metadata_t *metadata, const byte* command, size_t command_len);

/**
* Reads from  UDP socket

*/

extern int read_udp(device_metadata_t *metadata, void *buf, size_t amount);

#endif