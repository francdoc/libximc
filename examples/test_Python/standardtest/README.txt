Eng.

How to work with example:
1. For the correct use of the libximc library, the example uses a file shell, /ximc/crossplatform/wrappers/python/pyximc.py with a description of the library structure
2. Configuring dependencies:
	* For macOS X: 
		- copy the libximc/macosx/libximc.framework to the directory with an example
	
	* For Linux:
		- nothing needs to be done before example execute if you use ./testpython.sh 
		- install the packages, from the /ximc/deb folder, libximc7_x.x.x and libximc7-dev_x.x.x for the required architecture strictly in the specified order
		- set LD_LIBRARY_PATH so Python can find libraries using PATH: 
		export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:usr/lib - specify the correct path for installed packages
	
	* For Windows:
		- nothing needs to be done before example execute
		- the library with dependencies is located in the ximc/winX folders. The following files are required for the example to work libximc.dll xibridge.dll
3. To run, you need python 2 or 3 versions installed
4. Run the example with the command: python testpython.py

To modify the example:
The example code can be modified in any text editor


Rus.
 
Как работать с примером:
1. Для правильного использования библиотеки libximc в примере используется файловая оболочка, /ximc/crossplatform/wrappers/python/pyximc.py с описанием структуры библиотеки
2. Настройка зависимостей:
	* Для macOS X: 
		- скопируйте libximc/macosx/libximc.framework в каталог с примером
	
	* Для Linux:
		- ничего не нужно делать перед запуском примера, если вы используете ./testpython.sh
		- установите пакеты из папки /ximc/deb, libximc7_x.x.x и libximc7-dev_x.x.x для требуемой архитектуры строго в указанном порядке
		- установите LD_LIBRARY_PATH, чтобы Python мог находить библиотеки, используя PATH: 
		export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:usr/lib - укажите правильный путь для установленных пакетов
	
	* Для Windows:
		- перед запуском примера ничего делать не нужно  
		- библиотека с зависимостями находится в папках ximc/winX. Для работы примера требуются следующие файлы libximc.dll xibridge.dll
3. Для запуска вам необходимо установить python 2 или 3 версии
4. Запустите пример с помощью команды: python testpython.py

Чтобы изменить пример:
Пример кода может быть изменен в любом текстовом редакторе