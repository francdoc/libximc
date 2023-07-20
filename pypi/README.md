# Скрипт для выпуска релиза на PyPI

1. Положите архив с релизом **libximc** в папку **pypi**. Название архива должно удовлетворять шаблону *libximc-version-all.tar.gz*.

2. Перейдите в папку **pypi/scripts** и запустите файл:

   - **install.bat**, если Вы работаете в *Windows*;

   - **install.sh**, если Вы работаете в *Linux*:

     ```bash
     bash install.sh
     ```

3. Из той же папки **pypi/scripts** запустите файл:

   - **run.bat**, если Вы работаете в *Windows*;

   - **run.sh**, если Вы работаете в *Linux*:

     ```bash
     bash run.sh
     ```

4. 