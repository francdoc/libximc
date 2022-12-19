Eng.

What are the example:
This example shows how to work with a profile for a specific positioner in a user application.

How to work with example:
* For macOS X:
	- copy ximc/macosx/libximc.framework, ximc/ximc.h in the examples/testprofile_C directory
	- install XCode
	- build an example of testprofile_C.xcodeproj using XCode
	- run the testprofile_C.app application and check its operation in Console.app

* For Linux: 
	- must be installed .deb packages libximc7_x.x.x and libximc7-dev_x.x.x for the required architecture strictly in the specified order, from the  /ximc/deb folder
	- copy ximc/ximc.h to the examples/test_C/testprofile_C directory. 
	- install gcc 
	- build an example using the installed library:
		$ make
	- run the example:
		$ make run
	- for a quick build and run the example on Linux, you can run the testprofile_C.sh script. You don't need to install a library for it to work. The script will automatically build and run the example. If the script outputs a message that the device has not been found, you need to change the device address in the script to the correct one: ./testprofile_C xi-com:/dev/ttyACM0

* For Windows:
	- to build and run the example, you need to use the Visual Studio 2013. Make sure that Microsoft Visual C++ Redistributable Package 2013 is installed
	- the library with dependencies is located in the ximc/winX folders. The following files are required for the example to work: libximc.dll, xibridge.dll
	- open the example /testprofile_C/testprofile_C.sln, compile and run it from the IDE


Rus.

Что представляет собой пример:
Данный пример показывает как работать с профилем для конкретного позиционера в пользовательском приложении.

Как работать с примером:
* Для macOS X: 
	- скопируйте ximc/macosx/libximc.framework, ximc/ximc.h в каталог examples/testprofile_C
	- установите XCode
	- соберите пример testprofile_C.xcodeproj используя XCode
	- запустите приложение testprofile_C.app и проверте его работу в Console.app

* Для Linux: 
	- необходимо установить .deb пакеты libximc7_x.x.x и libximc7-dev_x.x.x для требуемой архитектуры строго в указанном порядке, из папки /ximc/deb
	- скопируйте ximc/ximc.h в каталог examples/test_C/testprofile_C
	- установите gcc 
	- собирите пример с помощью установленной библиотеки:
		$ make
	- запустите пример:
		$ make run
	- для быстрой сборки и запуска примера на Linux можно запустить скрипт testprofile_C.sh. Для его работы не нужно устанавливать библиотеку. Скрипт автоматически соберет и запустит пример. Если скрипт выведет сообщение, что не найдено устройство нужно поменять в скрипте адрес устройства на правильный: ./testprofile_C  xi-com:/dev/ttyACM0

* Для Windows:
	- для сборки и запуска примера нужно использовать среду Visual Studio 2013. Убедитесь, что Microsoft Visual C++ Redistributable Package 2013 установлен
	- библиотека с зависимостями расположена в папках ximc/winX. Для работы примера необходимы файлы: libximc.dll, xibridge.dll
	- откройте пример /testprofile_C/testprofile_C.sln, скомпилируйте и запустите его из среды IDE

