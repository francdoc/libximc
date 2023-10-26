# fw-scl-standa

In a RPi4 with 64 bit OS, run the following commands:
    
    mkdir folder
    cd repos
    mkdir folder
    cd folder

    wget "https://files.xisupport.com/libximc/libximc-2.14.17-all.tar.gz" -O "libximc-2.14.17-all.tar.gz"
    
    OUTPUT_FILE="libximc-2.14.17-all.tar.gz" && tar -xvf "$OUTPUT_FILE"

    # Change to the extracted directory
    cd ximc-2.14.17/ximc/deb

    # Install libximc7 package
    sudo apt install ./libximc7_2.14.17-1_armhf.deb

    # Install libximc7-dev package
    sudo apt install ./libximc7-dev_2.14.17-1_armhf.deb

    # Set LD_LIBRARY_PATH environment variable
    export LD_LIBRARY_PATH=\$LD_LIBRARY_PATH:/usr/lib