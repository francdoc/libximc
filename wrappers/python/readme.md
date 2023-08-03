# libximc

This is python binding for libximc - cross-platform library for [Standa  8SMC5-USB](https://www.standa.lt/products/catalog/motorised_positioners?item=525) motor controllers. 

![8SMC5-based devices](https://raw.githubusercontent.com/EPC-MSU/libximc/dev-2.14/libximc/docs/8SMC5_based_devices.png)

Libximc manages hardware using interfaces: USB 2.0, RS232 and Ethernet, also uses a common and proven virtual serial port interface, so you can work with motor control modules through this library under almost all operating systems, including Windows, Linux and Mac OS X.

This library also supports virtual devices. So you can make some tests without real hardware.

## Installation

```shell
pip install libximc
```

### Minimal example

```python
import time
from ctypes import c_int, byref
import libximc as ximc

# Virtual device will be used by default.
# In case you have real hardware set correct device URI here

device_uri = "xi-emu:///virtual_motor_controller.bin"  # Virtual device
# device_uri = "xi-com:\\\\.\\COM111"                  # Serial port
# device_uri = "xi-tcp://172.16.130.155:1820"          # Raw TCP connection
# device_uri = "xi-net://192.168.1.120/abcd"           # XiNet connection

device_id = ximc.lib.open_device(device_uri.encode())
if device_id > 0:
    print("Device with URI {} successfully opened".format(device_uri))
else:
    raise RuntimeError("Failed to open device with URI", device_uri)

print("Launch movement...")
ximc.lib.command_right(device_id)

time.sleep(3)

print("Stop movement")
ximc.lib.command_stop(device_id)

print("Disconnect device")
ximc.lib.close_device(byref(c_int(device_id)))

print("Done")
```

## More information

* Libximc library documentation: https://libximc.xisupport.com/doc-en/index.html

* Standa 8SMC5 motor controller user manual: https://doc.xisupport.com/en/8smc5-usb/

* Standa website: https://www.standa.lt/

If you have faced any issues while using the library and you have no idea how to solve them contact **technical support** via:

* Website: [en.xisupport.com](https://en.xisupport.com/account/register)
* E-mail: [8smc4@standa.lt](mailto:8smc4@standa.lt)
* Telegram: [@SMC5TechSupport](https://t.me/SMC5TechSupport)
* WhatsApp: [+1 (585) 282-6387](https://wa.me/15852826387)
