Eng.

A simple test application to show the main features of the library.


For run:

 * On OS X: library is a Mac OS X framework, and at example application it’s bundled inside testappeasy_C.app.
Copy ximc/macosx/libximc.framework, ximc/ximc.h to the directory examples/test_C/testappeasy_C.
Install XCode. Test app should be built with XCode project testappeasy_C.xcodeproj.
Then launch application testappeasy_C.app and check activity output in Console.app.
 * For Linux: install libximc*.deb and libximc-dev*.deb of the target architecture in the specified order. 
! IT is IMPORTANT to install the library only of the appropriate Linux bit depth and only in the specified order.
Then copy ximc/ximc.h to the directory
examples/test_C/testappeasy_C. Install gcc. Test application can be built with the installed library with the following script:
$ make
In case of cross-compilation (target architecture differs from the current system architecture) feed -m64 or -m32 flag
to compiler.
Then launch the application as:
$ make run

To quickly build and run the example on Linux, you can run the script testappeasy_C.sh . You don't need to install libraries for it to work.
It will automatically build and run the example. If the script displays a message that the device has not been found, you can change the device address to the correct one:
./testappeasy_C  xi-com:/dev/ttyACM0

 * In Windows: testappeasy_C can be built using testappeasy_C.sln. Make sure that Microsoft Visual C++ Redistributable Package 2013 is installed.
Open solution examples/test_C/testappeasy_C/testappeasy_C.sln, build and run from the IDE.

For run in CodeBlocks:

1. Before starting:
* On OS X: copy ximc/macosx/libximc.framework, ximc/ximc.h to the directory
examples/test_C/testappeasy_C. Install XCode compatible with CodeBlocks.
* For Linux: Install libximc*deb and libximc-dev*dev of the target architecture. Then copy ximc/ximc.h to the directory
examples/test_C/testappeasy_C. Install gcc compatible with CodeBlocks.
* In Windows, you must use MS Visual C++ to compile. Make sure that the Microsoft Visual C++ Redistributable Package is installed.
The library with dependencies is located in the ximc/win** folders. The following files are required for the example to work: bindy.dll, libximc.dll, xiwrapper.dll.

2. To build and run, open the examples/test_C/testappeasy_C/testappeasy_C.cbp project in CodeBlocks. For Windows select Configuration named Win32 or Win64.
Build and run the application from the development environment.




Rus.

Простое тестовое приложение для показа основных возможностей библиотеки.

 
Для запуска примера:

* На OS X: библиотека для Mac OS поставляется в формате Mac OS X framework. Скопируйте ximc/macosx/libximc.framework, ximc/ximc.h в каталог
examples/test_C/testappeasy_C. Должен быть установлен XCode. Пример testappeasy_C дорлжен быть собран проектом XCode testappeasy_C.xcodeproj.
Запустите приложение testappeasy_C.app и проверте его работу в Console.app.
* Для Linux: установите libximc*.deb и libximc-dev*.deb целевой архитектуры в указанном порядке. 
! ВАЖНО устанавливать библиотеку только соответствующей разрядности Linux и только в указанном порядке.
Затем скопируйте ximc/ximc.h в каталог
examples/test_C/testappeasy_C. Установите gcc. Тестовое приложение может быть собрано с помощью установленной библиотеки командой:
$ make
Выполнить приложение можно командой:
$ make run

Для быстрой сборки и запуска примера на Linux можно запустить скрипт testappeasy_C.sh. Для его работы не нужно устанавливать библиотеки. 
Он автоматически соберет и запустит пример. Если скрипт выведет сообщение, что не найдено устройство можно поменять адрес устройства на правильный: 
./testappeasy_C  xi-com:/dev/ttyACM0


* В Windows для компиляции необходимо использовать MS Visual C++. Убедитесь, что Microsoft Visual C++ Redistributable Package 2013 установлен. 
Библиотека с зависимостями находится в папках ximc/win**. Для работы примера неоходимы следующие файлы: bindy.dll, libximc.dll, xiwrapper.dll.
Откройте пример /testappeasy_C/testappeasy_C.sln, создайте и запустите их из среды IDE.

Для работы с примером в среде CodeBlocks:

1. Перед запуском:
* На OS X: скопируйте ximc/macosx/libximc.framework, ximc/ximc.h в каталог
examples/test_C/testappeasy_C. Установите XCode, совместимый с CodeBlocks.
* Для Linux: установите libximc*deb и libximc-dev*dev целевой архитектуры. Затем скопируйте ximc/ximc.h в каталог
examples/test_C/testappeasy_C. Установите gcc, совместимый с CodeBlocks.
* В Windows для компиляции необходимо использовать MS Visual C++. Убедитесь, что Microsoft Visual C++ Redistributable Package установлен. 
Библиотека с зависимостями находится в папках ximc/win**. Для работы примера неоходимы следующие файлы: bindy.dll, libximc.dll, xiwrapper.dll.
2. Для сборки и запуска откройте проект examples/test_C/testappeasy_C/testappeasy_C.cbp в CodeBlocks. Для ОС Windows выберите  конфигурацию Win32 или Win64.
Выполните сборку и запустите приложение из среды разработки.