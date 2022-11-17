Eng.

What are the examples:
A test application showing advanced features of working with the library, including user units and working with a correction table.
 
How to work with example:
* For macOS X:
	- copy ximc/macosx/libximc.framework, ximc/ximc.h to the examples/testapp_C directory
	- install XCode
	- build an example of testapp_C.xcodeproj using xcode
	- launch the testapp_C.app application and check its operation in Console.app

* For Linux: 
	- must be installed .deb packages libximc7_x.x.x and libximc7-dev_x.x.x for the required architecture strictly in the specified order, from the folder /ximc/deb
	- copy ximc/ximc.h to the examples/testapp_C directory
	- install gcc 
	- build an example using the installed library:
		$make
	- run the example:
		$make run
	- to quickly build and run the example on Linux, you can run the script testapp_C.sh . You don't need to install a library for it to work. The script will automatically build and run the example. If the script outputs a message that the device has not been found, you need to change the device address in the script to the correct one: ./testapp_C xi-com:/dev/ttyACM0

* For Windows:
	- to build and run the example, you need to use the Visual Studio 2013 environment. Make sure that Microsoft Visual C++ Redistributable Package 2013 is installed
	- the library with dependencies is located in the ximc/winX folders. The following files are required for the example to work: libximc.dll , xibridge.dll
	- open the example /testapp_C/testapp_C.sln, compile and run it from the IDE

To work with the example in the CodeBlocks environment:
* For macOS X:
	- Copy ximc/macosx/libximc.framework, ximc/ximc.h to the examples/testapp_C directory. 
	- Install XCode compatible with CodeBlocks.

* For Linux: 
	- install .deb packages libximc7_x.x.x and libximc7-dev_x.x.x for the required architecture strictly in the specified order, from the folder /ximc/deb
	- copy ximc/ximc.h to the examples/testapp_C directory
	- install gcc compatible with CodeBlocks.
	
* For Windows:
	- to build and run the example, you need to use the Visual Studio 2013 environment. Make sure that Microsoft Visual C++ Redistributable Package 2013 is installed
	- the library with dependencies is located in the ximc/winX folders. The following files are required for the example to work: libximc.dll , xibridge.dll
	- to build and run the example, open the examples/teachapp_C/testapp_C.cbp project in CodeBlocks
	- select Win32 or Win64 configuration
	- build and run the application from the development environment


Rus.

Что представляет собой пример:
Тестовое приложение показывающее расширенные возможности работы с библиотекой, включая пользовательские единицы и работу с корректирующей таблицей.
 
Как работать с примером:
* Для macOS X: 
	- скопируйте ximc/macosx/libximc.framework, ximc/ximc.h в каталог examples/testapp_C
	- установите XCode
	- соберите пример testapp_C.xcodeproj используя XCode
	- запустите приложение testapp_C.app и проверте его работу в Console.app

* Для Linux: 
	- необходимо установить .deb пакеты libximc7_x.x.x и libximc7-dev_x.x.x для требуемой архитектуры строго в указанном порядке, из папки /ximc/deb
	- скопируйте ximc/ximc.h в каталог examples/testapp_C
	- установите gcc 
	- собирите пример с помощью установленной библиотеки:
		$ make
	- запустите пример:
		$ make run
	- для быстрой сборки и запуска примера на Linux можно запустить скрипт testapp_C.sh. Для его работы не нужно устанавливать библиотеку. Скрипт автоматически соберет и запустит пример. Если скрипт выведет сообщение, что не найдено устройство нужно поменять в скрипте адрес устройства на правильный: ./testapp_C  xi-com:/dev/ttyACM0

* Для Windows:
	- для сборки и запуска примера нужно использовать среду Visual Studio 2013. Убедитесь, что Microsoft Visual C++ Redistributable Package 2013 установлен
	- библиотека с зависимостями расположена в папках ximc/winX. Для работы примера необходимы файлы: libximc.dll, xibridge.dll
	- откройте пример /testapp_C/testapp_C.sln, скомпилируйте и запустите его из среды IDE

Для работы с примером в среде CodeBlocks:
* Для macOS X: 
	- скопируйте ximc/macosx/libximc.framework, ximc/ximc.h в каталог examples/testapp_C. 
	- установите XCode, совместимый с CodeBlocks.

* Для Linux: 
	- установить .deb пакеты libximc7_x.x.x и libximc7-dev_x.x.x для требуемой архитектуры строго в указанном порядке, из папки /ximc/deb
	- скопируйте ximc/ximc.h в каталог examples/testapp_C
	- установите gcc совместимый с CodeBlocks.
	
* Для Windows:
	- для сборки и запуска примера нужно использовать среду Visual Studio 2013. Убедитесь, что Microsoft Visual C++ Redistributable Package 2013 установлен
	- библиотека с зависимостями расположена в папках ximc/winX. Для работы примера необходимы файлы: libximc.dll, xibridge.dll
	- для сборки и запуска примера откройте проект examples/teastapp_C/testapp_C.cbp в CodeBlocks
	- выберите конфигурацию Win32 или Win64
	- выполните сборку и запустите приложение из среды разработки

