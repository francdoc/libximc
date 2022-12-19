Eng.

How to work with example:
1. To use the libximc library correctly, the example uses a file wrapper, /ximc/crossplatform/wrappers/python/pyximc.py with a description of the library structure.
2. Configuring dependencies:
* On macOS X: 
	- copy the ximc/macosx/libximc.framework library to the directory with an example

* On Linux:
	- nothing needs to be done before example execute if you use ./Extendtestpython.sh.
	- install the packages, from the /ximc/deb folder, libximc7_x.x.x and libximc7-dev_x.x.x for the required architecture strictly in the specified order
	- set LD_LIBRARY_PATH so that Python can find libraries using PATH. For example, using: 
	export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:usr/lib. You must specify the correct path for the installed packages.
 
* On Windows: 
	- before running example, install dependencies from requirements.txt. To do this, on the command line in the directory with the example, execute:
	python -m pip install -r requirements.txt
	- the library with dependencies is located in the ximc/winX folders. The following files are required for the example to work xibridge.dll, libximc.dll.
3. To run, you need to have python 2 or 3 versions installed
4. Run the example with the command: python Extendtestpython.py

To modify the example:
The example code can be modified in any text editor.
More detailed information about the example can be found in the file Readme_Extendtestpython.html.


Rus.
Для корректного использования библиотеки libximc в примере используется файловая оболочка, /ximc/crossplatform/wrappers/python/pyximc.py с описанием структуры библиотеки.
Для запуска необходим установленный python 2 или 3 версии. Python версии 3.9 НЕ ПОДДЕРЖИВАЕТСЯ!
 
Как работать с примером:
1. Для корректного использования библиотеки libximc в примере используется файловая оболочка, /ximc/crossplatform/wrappers/python/pyximc.py с описанием структуры библиотеки.
2. Настройка зависимостей:
* Для macOS X: 
	- скопируйте библиотеку ximc/macosx/libximc.framework в дерикторию с примером

* Для Linux: 
	- можно ни чего не устанавливать, если запускать пример с помощью ./Extendtestpython.sh
	- необходимо установить пакеты, из папки /ximc/deb архива, libximc7_x.x.x и libximc7-dev_x.x.x для требуемой архитектуры строго в указанном порядке - установить LD_LIBRARY_PATH, чтобы Python мог находить библиотеки с помощью RPATH. Например, с помощью: 
	export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:usr/lib - указать правильный путь для установленных пакетов.

* Для Windows:
	- перед запуском примера установите зависимости из requirements.txt. Для этого в командой строке в директории с примером выполните команду: 
	python -m pip install -r requirements.txt
	- используемые библиотеки: xibridge.dll, libximc.dll, находятся в папках ximc/winX
3. Для запуска необходим установленный python 2 или 3 версии
4. Запустите пример командой: python Extendtestpython.py

Для модификации примера:
Код примера можно модифицировать в любом текстовом редакторе.
Более подробную информацию о примере можно посмотреть в файле Readme_Extendtestpython.html.