cd ..
python3 run.py
if [ -d "./package" ]
then
    printf "\nBuilding distribution...\n"
    cd "./package"
    python3 -m pip install --upgrade build
    python3 -m build
fi