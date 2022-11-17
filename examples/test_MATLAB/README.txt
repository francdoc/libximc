Eng.

How to work with example:
* For macOS X:
	- copy from the ximc/macosx folder libximc.framework, wrappers/ximcm.h, ximc.h to the directory with examples
	- install XCode compatible with Matlab
	- run the program on the command line

* For Linux:
	- must be installed .deb packages libximc7_x.x.x and libximc7-dev_x.x.x for the required architecture strictly in the specified order, from the  /ximc/deb folder
	- copy ximc/macosx/wrappers/matlab/ximcm.h to the examples/test_MATLAB directory.
	- install gcc compatible with Matlab
To check the compatibility of XCode and gcc versions, study the documents https://www.mathworks.com/content/dam/mathworks/mathworks-dot-com/support/sysreq/files/SystemRequirements-Release2014a_SupportedCompilers.pdf or similar
	- run the program on the command line

* For Windows:
	- the following files are necessary for the example to work: libximc.dll , xibridge.dll . The dependent libraries are located in the ximc/winX folders
	- there is nothing to do before starting
	- run the program on the command line

To modify the example:
The example code can be modified in the MATLAB editor.


Rus.

Как работать с примером:
* Для macOS X: 
	- из папки  ximc/macosx скопируйте libximc.framework, wrappers/ximcm.h, ximc.h в каталог с примерами 
	- установите XCode совместимый с Matlab
	- запустите программу в командной строке

* Для Linux: 
	- необходимо установить .deb пакеты libximc7_x.x.x и libximc7-dev_x.x.x для требуемой архитектуры строго в указанном порядке, из папки /ximc/deb  
	- скопируйте ximc/macosx/wrappers/matlab/ximcm.h в каталог examples/test_MATLAB. 
	- установите gcc, совместимый с Matlab
	Для проверки совместимости версий XCode и gcc изучите документы	 https://www.mathworks.com/content/dam/mathworks/mathworks-dot-com/support/sysreq/files/SystemRequirements-Release2014a_SupportedCompilers.pdf или аналогичные
	- запустите программу в командной строке

* Для Windows:
	- для работы примера неоходимы следующие файлы: libximc.dll, xibridge.dll. Зависимые библиотеки находится в папках ximc/winX
	- перед запуском ничего не нужно делать
	- запустите программу в командной строке

Для модификации примера:
	Код примера можно модифицировать в редакторе MATLAB.