Eng.


For run:
1. Type in command line for win32 or win64:
 java -classpath libjximc.jar -classpath testjava.jar ru.ximc.TestJava
2. For other platforms, use the compiled folder. You may need to copy some dependencies to it.
 
For modify:
1. Unpack jar:
 jar xvf testjava.jar ru META-INF
2. Modyfy sources
3. Build example:
 javac -classpath libjximc.jar -Xlint ru/ximc/TestJava.java
 jar cmf META-INF\MANIFEST.MF testjava.jar ru

Rus.

 
Для запуска примера:
1. Для запуска примера для win32 или win64 наберите в командной строке: 
 java -classpath libjximc.jar -classpath testjava.jar ru.ximc.TestJava
2. Для других платформ используйте папку compiled. Возможно в нее понадобится скопировть некоторые зависимости.
 
Для модификации примера:
1. Распакуйте jar командой:
 jar xvf testjava.jar ru META-INF
2. Модифицируйте исходные коды
3. Соберите пример:
 javac -classpath libjximc.jar -Xlint ru/ximc/TestJava.java
 jar cmf MANIFEST.MF testjava.jar ru