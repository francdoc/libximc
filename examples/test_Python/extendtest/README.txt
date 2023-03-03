Eng.
To use the libximc library correctly, the example uses a file wrapper, /ximc/crossplatform/wrappers/python/pyximc.py with a description of the library structure.
To run, you need to have python 2 or 3 versions installed. Python version 3.9 IS NOT SUPPORTED!

For run:
Configuring dependencies:
 * On OS X: 
	- copy the ximc/macosx/libximc.framework to the current directory
	- before running the example, install the dependencies from requirements.txt . To do this, opne terminal in the directory with the example and run the command: python -m pip install -r requirements.txt
	- install getch. To do this, run: python -m pip install getch
   To run the example, you can go two ways:
	- you don't have to install the libximc library and just run the example using a bash file: bash ./Extendtestpython.sh 
	- install packages from the /ximc/deb archive folder, libximc7_x.x.x and libximc7-dev_x.x.x for the required architecture strictly in the specified order. You will also need to set LD_LIBRARY_PATH so that Python can find libraries using PATH. For example, using:
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:usr/lib - specify the correct path for installed packages.
	- run the example with the command: python Extendtestpython.py

 
 * On Linux:
	- before running the example, install the dependencies from requirements.txt. To do this, open terminal in the directory with the example and run the command: python -m pip install -r requirements.txt
	- install getch. To do this, run: python -m pip install getch
   To run the example, you can go two ways:
	- you don't have to install the libximc library and just run the example using a bash file: bash ./Extendtestpython.sh
	- install packages from the /ximc/deb archive folder, libximc7_x.x.x and libximc7-dev_x.x.x for the required architecture strictly in the specified order. You will also need to set LD_LIBRARY_PATH so that Python can find libraries using PATH. For example, using:
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:usr/lib - specify the correct path for installed packages.
	- run the example with the command: python Extendtestpython.py
 
 * On Windows: 
	- before running the example, install the dependencies from requirements.txt . To do this, on the command line in the directory with the example, run the command: python -m pip install -r requirements.txt
	Libraries used: bindy.dll, libximc.dll, xiwrapper.dll, key file.sqlite, is located in the folder for the corresponding Windows versions.
	- run the example with the command: python Extendtestpython.py


For modify:
The example code can be modified in any text editor.
More detailed information about the example can be found in the file Readme_Extendtestpython.html.


Rus.
Для корректного использования библиотеки libximc в примере используется файловая оболочка, /ximc/crossplatform/wrappers/python/pyximc.py с описанием структуры библиотеки.
Для запуска необходим установленный python 2 или 3 версии. Python версии 3.9 НЕ ПОДДЕРЖИВАЕТСЯ!
 
Для запуска примера:
 * В OS X: 
	- скопируйте библиотеку ximc/macosx/libximc.framework в текущий каталог
	- перед запуском примера установите зависимости из requirements.txt. Для этого откройте терминал в директории с примером и выполните команду: python -m pip install -r requirements.txt
	- установите getch. Для этого выполните: python -m pip install getch
   Для запуска примера можно пойти двумя путями:
	- можно не устанавливать библиотеку libximc и просто запускать пример с помощью командного файла ./Extendtestpython.sh
	- установить пакеты, из папки /ximc/deb архива, libximc7_x.x.x и libximc7-dev_x.x.x для требуемой архитектуры строго в указанном порядке. Так же потребуется установить LD_LIBRARY_PATH, чтобы Python мог находить библиотеки с помощью RPATH. Например, с помощью:
 export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:usr/lib - указать правильный путь для установленных пакетов.
	- запустите пример командой: python Extendtestpython.py
 
 * В Linux: 
	- перед запуском примера установите зависимости из requirements.txt. Для этого в командой строке в директории с примером выполните команду:
python -m pip install -r requirements.txt
	- установите getch. Для этого выполните: python -m pip install getch
   Для запуска примера можно пойти двумя путями:
	- можно не устанавливать библиотеку libximc и просто запускать пример с помощью командного файла ./Extendtestpython.sh
	- установить пакеты, из папки /ximc/deb архива, libximc7_x.x.x и libximc7-dev_x.x.x для требуемой архитектуры строго в указанном порядке. Так же потребуется установить LD_LIBRARY_PATH, чтобы Python мог находить библиотеки с помощью RPATH. Например, с помощью:
 export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:usr/lib - указать правильный путь для установленных пакетов.
	- запустите пример командой: python Extendtestpython.py
 
 * В Windows:
	- перед запуском примера установите зависимости из requirements.txt. Для этого в командой строке в директории с примером выполните команду:
 python -m pip install -r requirements.txt
 Используемые библиотеки: bindy.dll, libximc.dll, xiwrapper.dll находится в папке для соответствующих версий Windows.
	- запустите пример командой: python Extendtestpython.py

 
Для модификации примера:
Код примера можно модифицировать в любом текстовом редакторе.
Более подробную информацию о примере можно посмотреть в файле Readme_Extendtestpython.html.