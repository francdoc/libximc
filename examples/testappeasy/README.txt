Eng.

A simple test application to show the main features of the library.

How to work with example.

For run:

 * On OS X: library is a Mac OS X framework, and at example application it’s bundled inside testappeasy.app. 
Copy ximc/macosx/libximc.framework, ximc/ximc.h to the directory examples/testappeasy. 
Install XCode. Test app should be built with XCode project testappeasy.xcodeproj. 
Then launch application testappeasy.app and check activity output in Console.app.
 * For Linux: Install libximc*deb and libximc-dev*dev of the target architecture. Then copy ximc/ximc.h to the directory
examples/testappeasy. Install gcc. Test application can be built with the installed library with the following script:
$ make
In case of cross-compilation (target architecture differs from the current system architecture) feed -m64 or -m32 flag
to compiler.
Then launch the application as:
$ make run
 * In Windows: testappeasy can be built using testappeasy.sln. Make sure that Microsoft Visual C++ Redistributable Package is installed.
Open solution examples/testappeasy/testappeasy.sln, build and run from the IDE.



Rus.

Простое тестовое приложение для показа основных возможностей библиотеки.

Как работать с примером
 
Для запуска примера:

* На OS X: библиотека для Mac OS поставляется в формате Mac OS X framework. Скопируйте ximc/macosx/libximc.framework, ximc/ximc.h в каталог
examples/testappeasy. Должен быть установлен XCode. Пример testappeasy дорлжен быть собран проектом XCode testappeasy.xcodeproj.
Запустите приложение testappeasy.app и проверте его работу в Console.app.
* Для Linux: установите libximc*deb и libximc-dev*dev целевой архитектуры. Затем скопируйте ximc/ximc.h в каталог
examples/testappeasy. Установите gcc. Тестовое приложение может быть собрано с помощью установленной библиотеки командой:
$ make
Выполнить приложение можно командой:
$ make run
* В Windows для компиляции необходимо использовать MS Visual C++. Убедитесь, что Microsoft Visual C++ Redistributable Package установлен. 
Библиотека с зависимостями находится в папках ximc/win**. Для работы примера неоходимы следующие файлы: bindy.dll, libximc.dll, xiwrapper.dll.
Откройте пример /testappeasy/testappeasy.sln, создайте и запустите их из среды IDE.

