Eng.

A test application that shows the advanced features of working with the library, including user units and working with the correction table.


For run:

 * On OS X: library is a Mac OS X framework, and at example application it’s bundled inside testapp.app. 
Copy ximc/macosx/libximc.framework, ximc/ximc.h to the directory examples/testapp. 
Install XCode. Test app should be built with XCode project testapp.xcodeproj. 
Then launch application testapp.app and check activity output in Console.app.
 * For Linux: Install libximc*deb and libximc-dev*dev of the target architecture. Then copy ximc/ximc.h to the directory
examples/testapp. Install gcc. Test application can be built with the installed library with the following script:
$ make
In case of cross-compilation (target architecture differs from the current system architecture) feed -m64 or -m32 flag
to compiler.
Then launch the application as:
$ make run
 * In Windows: testapp can be built using testapp.sln. Make sure that Microsoft Visual C++ Redistributable Package 2013 is installed.
Open solution examples/testapp/testapp.sln, build and run from the IDE.



Rus.

Тестовое приложение показывающее расширенные возможности работы с библиотекой, включая пользовательские единицы и работу с корректирующей таблицей.

 
Для запуска примера:

* На OS X: библиотека для Mac OS поставляется в формате Mac OS X framework. Скопируйте ximc/macosx/libximc.framework, ximc/ximc.h в каталог
examples/testapp. Должен быть установлен XCode. Пример testapp дорлжен быть собран проектом XCode testapp.xcodeproj.
Запустите приложение testapp.app и проверте его работу в Console.app.
* Для Linux: установите libximc*deb и libximc-dev*dev целевой архитектуры. Затем скопируйте ximc/ximc.h в каталог
examples/testapp. Установите gcc. Тестовое приложение может быть собрано с помощью установленной библиотеки командой:
$ make
Выполнить приложение можно командой:
$ make run
* В Windows для компиляции необходимо использовать MS Visual C++. Убедитесь, что Microsoft Visual C++ Redistributable Package 2013 установлен. 
Библиотека с зависимостями находится в папках ximc/win**. Для работы примера неоходимы следующие файлы: bindy.dll, libximc.dll, xiwrapper.dll.
Откройте пример /testapp/testapp.sln, создайте и запустите их из среды IDE.

