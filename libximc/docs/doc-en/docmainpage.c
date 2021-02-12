/*!
 * \mainpage libximc library
 *
 * Documentation for libximc library.
 *
 * \image html 8SMC4.png
 * \image html 8SMC5.png
 *
 * Libximc is cross-platform library for working with 8SMC4-USB and 8SMC5-USB controllers.
 *
 * Full documentation about controllers is <a href="https://doc.xisupport.com">there</a>
 *
 * Full documentation about libximc API is available on the page <a href="https://libximc.xisupport.com/doc-en/ximc_8h.html">ximc.h.</a>
 *
 * \section what_the_controller_does What the controller does.
 *
 * - Supports input and output synchronization signals to ensure the joint operation of multiple devices within a complex system ;.
 * - Works with all compact stepper motors with a winding current of up to 3 A, without feedback, as well as with stepper motors equipped with an encoder in the feedback circuit, including a linear encoder on the positioner.
 * - Manages hardware using ready-made software or using libraries for programming languages: C / C ++, C #, JAVA, Visual Basic, Python 2/3, .NET, Delphi, integration with MS Visual Studio programming environments, gcc, Xcode.
 * - Works with scientific development environments by integrating LabVIEW and MATLAB;
 *
 * \section what_can_do_library What can do libximc library
 *
 * - Libximc manages hardware using interfaces: USB 2.0., RS232 and Ethernet, also uses a common and proven virtual serial port interface, so you can work with motor control modules through this library under almost all operating systems, including Windows, Linux and Mac OS X
 * - Libximc library supports plug/unplug on the fly. Each device can be controlled only by one program at once. Multiple processes (programs) that control one device simultaneously are not allowed.
 *
 * \warning
 * Libximc library opens the controller in exclusive access mode. Any controller opened with libximc (XiLab also uses this library) needs to be closed before it may be used by another process. So at first check that you have closed XiLab or other software dealing with the controller before trying to reopen the controller.
 *
 * Please read the <a href="https://libximc.xisupport.com/doc-en/intro_sec.html">Introduction</a> to start work with library.
 *
 * To use libximc in your project please consult with <a href="https://libximc.xisupport.com/doc-en/howtouse_sec.html"> How to use with...</a>
 *
 * \section assistance Assistance.
 *
 * Many thanks to everyone who sends suggestions, errors and ideas. We appreciate your suggestions and try to make our product better. Please post your questions <a href="https://en.xisupport.com">here</a>. Your ideas and comments send a e-mail: 8smc4@standa.lt
 *
 * \page intro_sec Introduction
 *
 * \section about_sec About library
 *
 * This document contains all information about libximc library.
 * It utilizes well known virtual COM-port interface, so you can use it on Windows 7, Windows, Vista, Windows XP, Windows Server 2003, Windows 2000, Linux, Mac OS X.
 * Multi-platform programing library supports plug/unplug on the fly.
 * Each device can be controlled only by one program at once. Multiple processes (programs) that control one device simultaneously are not allowed.
 *
 * \section sysreq_sec System requirements
 *
 * \subsection sysreq_build For rebuilding library
 *
 * On Windows:
 * - Windows 2000 or later, 64-bit system (if compiling both arhitectures) or 32-bit system. 
 * - Microsoft Visual C++ 2013 or later
 * - cygwin with tar, bison, flex, curl installed
 * - 7z
 *
 * On Linux:
 * - 64-bit or/and 32-bit system system
 * - gcc 4 or later
 * - common autotools: autoconf, autoheader, aclocal, automake, autoreconf, libtool
 * - gmake
 * - doxygen - for building docs
 * - LaTeX distribution (teTeX or texlive) - for building docs
 * - flex 2.5.30+
 * - bison
 * - mercurial (for building developer version from hg)
 *
 * On Mac OS X:
 * - XCode 4
 * - doxygen
 * - mactex
 * - autotools
 * - mercurial (for building developer version from hg)
 *
 * If mercurial is used, please enable 'purge' extension by adding to ~/.hgrc following lines:
 * \verbatim
   [extensions]
     hgext.purge=
   \endverbatim
 * 
 * \subsection sysreq_usage For using library
 *
 * Supported operating systems (32 or 64 bit) and environment requirements:
 * - Mac OS X 10.6
 * - Windows 2000 or later
 * - Autotools-compatible unix. Package is installed from sources.
 * - Linux debian-based 32 and 64 bit. DEB package is built against Debian Squeeze 7
 * - Linux debian-based ARM. DEB package is built on Ubuntu 14.04
 * - Linux rpm-based. RPM is built against OpenSUSE 12
 * - Java 7 64-bit or 32-bit
 * - .NET 2.0 (32-bit only)
 * - Delphi (32-bit only)
 
 *
 * Build requirements:
 * - Windows: Microsoft Visual C++ 2013 or mingw (currently not supported)
 * - UNIX: gcc 4, gmake
 * - Mac OS X: XCode 4
 * - JDK 7
 *
 *

 * \page building_sec How to rebuild library
 *

 * \section building_unix Building on generic UNIX
 *
 * Generic version could be built with standard autotools.
 * \code
 *   ./build.sh lib
 * \endcode
 * Built files (library, headers, documentation) are installed to ./dist/local directory.
 * It is a generic developer build. Sometimes you need to specify additional parameters to
 * command line for your machine. Please look to following OS sections.
 *
 * \section building_unix_deb Building on debian-based linux systems
 * Requirement: 64-bit and 32-bit debian system, ubuntu
 * Typical set of packages: gcc, autotools, autoconf, libtool, dpkg-dev, flex, bison, doxygen, texlive, mercurial
 * Full set of packages: apt-get install ruby1.9.1 debhelper vim sudo g++ mercurial git curl make cmake autotools-dev automake autoconf libtool default-jre-headless default-jdk openjdk-6-jdk dpkg-dev lintian texlive texlive-latex-extra texlive-lang-cyrillic dh-autoreconf hardening-wrapper bison flex doxygen lsb-release pkg-config check
 * For ARM cross-compiling install gcc-arm-linux-gnueabihf from your ARM toolchain.
 *
 * It's required to match library and host architecture: 64-bit library can be built only at 64-bit host,
 * 32-bit library - only at 32-bit host. ARM library is built with armhf cross-compiler gcc-arm-linux-gnueabihf.
 *
 * To build library and package invoke a script:
 * \code
 * $ ./build.sh libdeb
 * \endcode
 * 
 * For ARM library replace 'libdeb' with 'libdebarm'.
 *
 * Grab packages from ./ximc/deb and locally installed binaries from ./dist/local.
 *
 * \section building_unix_rpm Building on redhat-based linux systems
 * Requirement: 64-bit redhat-based system (Fedora, Red Hat, SUSE)
 * Typical set of packages: gcc, autotools, autoconf, libtool, flex, bison, doxygen, texlive, mercurial
 * Full set of packages: autoconf automake bison doxygen flex gcc gcc-32bit gcc-c++ gcc-c++-32bit java-1_7_0-openjdk java-1_7_0-openjdk-devel libtool lsb-release make mercurial rpm-build rpm-devel rpmlint texlive texlive-fonts-extra texlive-latex 
 *
 * It's possible to build both 32- and 64-bit libraries on 64-bit host system.
 * 64-bit library can't be built on 32-bit system.
 *
 * To build library and package invoke a script:
 * \code
 * $ ./build.sh librpm
 * \endcode
 * 
 * Grab packages from ./ximc/rpm and locally installed binaries from ./dist/local.
 *
 *
 * \section building_osx_generic Buliding on Mac OS X
 *
 * To build and package a script invoke a script:
 * \code
 * $ ./build.sh libosx
 * \endcode
 *
 * Built library (classical and framework), examples (classical and .app), documentation
 * are located at ./ximc/macosx, locally installed binaries from ./dist/local.
 *
 * \section building_win Buliding on Windows
 *
 * Requirements: 64-bit windows (build script builds both architectures), cygwin (must be installed to a default path), mercurial.
 *
 * Invoke a script:
 * \code
 * $ ./build.bat
 * \endcode
 *
 * Grab packages from ./deb/win32 and ./deb/win64 
 *
 * To build debug version of the library set environment variable "DEBUG" to "true" before running the build script.
 *
 * \section building_src Source code access
 * XIMC source codes are given under special request.
 *
 * \page howtouse_sec How to use with...
 *
 * Library usage can be examinated from test application testapp.
 * Non-C languages are supported because library supports stdcall calling convention and so can be used with a variety of languages.
 *
 * C test project is located at 'examples/testapp' directory, C# test project - at 'examples/testcs', VB.NET - 'examples/testvbnet', 
 * Delphi 6 - 'examples/testdelphi', sample bindings for MATLAB - 'examples/testmatlab', for Java - 'examples/testjava',
 * for Python - 'examples/testpython'.
 * Development kit also contains precompiled examples: testapp and testappeasy as 32 and 64-bit applications for Windows and 64-bit application for osx,
 * testcs, testvbnet, testdelphi - 32-bit only, testjava is architecture-independent, testmatlab and testpython are runtime-interpreted.
 *
 * NOTE: SDK requires Microsoft Visual C++ Redistributable Package (provided with SDK - vcredist_x86 or vcredist_x64)
 *
 * NOTE: On Linux both the libximc7_x.x.x and libximc7-dev_x.x need to be installed. For install packages, you can use the .deb command: dpkg -i filename.deb, where filename.deb is the name of the package (packages in Debian have the extension .deb). You must run dpkg with superuser privileges (root).
 *
 * \section howtouse_c_sec Usage with C
 *
 * \subsection howtouse_c_vcpp_sec Visual C++
 *
 * Testapp can be built using testapp.sln. 
 * Library must be compiled with MS Visual C++ too, mingw-library isn't supported.
 * Make sure that Microsoft Visual C++ Redistributable Package is installed. 
 *
 * Open solution examples/testapp/testapp.sln, build and run from the IDE.
 * 
 * In case of the 8SMC4-USB-Eth1 Ethernet adapter usage it is necessary to set correct IP address of the Ethernet adapter in testapp.c file before build (see enumerate_hints variable).
 *
 * \subsection howtouse_c_codeblocks CodeBlocks
 *
 * Testapp can be built using testcodeblocks.cbp. 
 * Library must be compiled with MS Visual C++ too, mingw-library isn't supported.
 * Make sure that Microsoft Visual C++ Redistributable Package is installed.  *
 *
 * Open solution examples/testcodeblocks/testcodeblocks.cbp, build and run from the IDE.
 *
 * \subsection howtouse_c_mingw_sec MinGW
 *
 * MinGW is a port of GCC to win32 platform.
 * It's required to install MinGW package.
 * Currently not supported
 *
 * MinGW-compiled testapp can be built with MS Visual C++ or mingw library.
 * \code
 * $ mingw32-make -f Makefile.mingw all
 * \endcode
 *
 * Then copy library libximc.dll to current directory and launch testapp.exe.
 *
 * In case of the 8SMC4-USB-Eth1 Ethernet adapter usage it is necessary to set correct IP address of the Ethernet adapter in testapp.c file before build (see enumerate_hints variable).
 * 
 * \subsection howtouse_c_bcb_sec C++ Builder
 *
 * First of all you should create C++ Builder-style import library. Visual C++ library is not compatible with BCB.
 * Invoke:
 * \code
 * $ implib libximc.lib libximc.def
 * \endcode
 *
 * Then compile test application:
 * \code
 * $ bcc32 -I..\..\ximc\win32 -L..\..\ximc\win32 -DWIN32 -DNDEBUG -D_WINDOWS testapp.c libximc.lib
 * \endcode
 *
 * In case of the 8SMC4-USB-Eth1 Ethernet adapter usage it is necessary to set correct IP address of the Ethernet adapter in testapp.c file before build (see enumerate_hints variable).
 * 
 * \subsection howtouse_c_xcode_sec XCode
 *
 * Test app should be built with XCode project testapp.xcodeproj. 
 * Library is a Mac OS X framework, and at example application it's bundled inside testapp.app
 *
 * Then launch application testapp.app and check activity output in Console.app.
 * 
 * In case of the 8SMC4-USB-Eth1 Ethernet adapter usage it is necessary to set correct IP address of the Ethernet adapter in testapp.c file before build (see enumerate_hints variable).
 *
 * \subsection howtouse_c_gcc_sec GCC
 *
 * Make sure that libximc (rpm, deb, freebsd package or tarball) is installed at your system.
 * Installation of package should be performed with a package manager of operating system.
 * On OS X a framework is provided.
 *
 * Note that user should belong to system group which allows access to a serial port (dip or serial, for example).
 *
 * Copy file /usr/share/libximc/keyfile.sqlite project directory:
 * \code
 * $ cp /usr/share/libximc/keyfile.sqlite .
 * \endcode
 *
 * Test application can be built with the installed library with the following script:
 * \code
 * $ make
 * \endcode
 *
 * In case of cross-compilation (target architecture differs from the current system architecture)
 * feed -m64 or -m32 flag to compiler. On OS X it's needed to use -arch flag instead to build an universal binary.
 * Please consult a compiler documentation.
 *
 * Then launch the application as:
 * \code
 * $ make run
 * \endcode
 *
 * Note: make run on OS X copies a library to the current directory.
 * If you want to use library from
 * the custom directory please be sure to specify LD_LIBRARY_PATH or DYLD_LIBRARY_PATH to
 * the directory with the library. 
 *
 * In case of the 8SMC4-USB-Eth1 Ethernet adapter usage it is necessary to set correct IP address of the Ethernet adapter in testapp.c file before build (see enumerate_hints variable).
 * 
 * \section howtouse_dotnet_sec .NET
 * 
 * Wrapper assembly for libximc.dll is wrappers/csharp/ximcnet.dll.
 * It is provided with two different architectures. Supports the platform .NET from 2.0. to 4.0.
 *
 * Test .NET applications for Visual Studio 2013 is located at testcs (for C#) and testvbnet (for VB.NET) respectively.
 * Open solutions and build.
 * 
 * In case of the 8SMC4-USB-Eth1 Ethernet adapter usage it is necessary to set correct IP address of the Ethernet adapter in testapp.cs or testapp.vb file (depending on programming language) before build (see enumerate_hints variable for C# or enum_hints variable for VB).
 *
 * \section howtouse_delphi_sec Delphi
 *
 * Wrapper for libximc.dll is a unit wrappers/delphi/ximc.pas
 *
 * Console test application for is located at testdelphi. Tested with Delphi 6 and only 32-bit version.
 *
 * Just compile, place DLL near the executable and run program.
 * 
 * In case of the 8SMC4-USB-Eth1 Ethernet adapter usage it is necessary to set correct IP address of the Ethernet adapter in testdelphi.dpr file before build (see enum_hints variable).
 *
 * \section howtouse_java_sec Java
 *
 * How to run example on Linux. Navigate to ximc-2.x.x./examples/testjava/compiled/ and run:
 * \code
 * $ cp /usr/share/libximc/keyfile.sqlite .
 * $ java -cp /usr/share/java/libjximc.jar:testjava.jar ru.ximc.TestJava
 * \endcode
 *
 * How to run example on Windows or Mac. Navigate to ximc-2.x.x./examples/testjava/compiled/.
 * Copy contents of ximc-2.x.x/ximc/win64 or ximc-2.x.x/ximc/macosx accordingly to the current directory.
 * Then run:
 * \code
 * $ java -classpath libjximc.jar -classpath testjava.jar ru.ximc.TestJava
 * \endcode
 
 * How to modify and recompile an example.
 * Navigate to examples/testjava/compiled. Sources are embedded in a testjava.jar.
 * Extract them:
 * \code
 * $ jar xvf testjava.jar ru META-INF
 * \endcode
 * Then rebuild sources:
 * \code
 * $ javac -classpath /usr/share/java/libjximc.jar -Xlint ru/ximc/TestJava.java
 * \endcode
 * or for windows or mac
 * \code
 * $ javac -classpath libjximc.jar -Xlint ru/ximc/TestJava.java
 * \endcode
 * Then build a jar:
 * \code
 * $ jar cmf META-INF/MANIFEST.MF testjava.jar ru
 * \endcode
 * 
 * In case of the 8SMC4-USB-Eth1 Ethernet adapter usage it is necessary to set correct IP address of the Ethernet adapter in TestJava.java file before build (see ENUM_HINTS variable).
 *
 * \section howtouse_python_sec Python
 *
 * Change current directory to the examples/testpython.
 * For correct usage of the library libximc, the example uses the file wrapper, crossplatform\wrappers\python\pyximc.py with a description of the structures of the library.
 *
 * Before launch:
 *
 * On OS X: copy library ximc/macosx/libximc.framework to the current directory.
 *
 * On Linux: you may need to set LD_LIBRARY_PATH 
 * so Python can locate libraries with RPATH. For example, you may need:
 * \code
 * export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:`pwd`
 * \endcode
 *
 * On Windows before the start nothing needs to be done. All necessary communication and dependencies are registered in the example code.
 * Libraries used: bindy.dll libximc.dll xiwrapper.dll. Located in the folder for the respective versions of Windows.
 *
 * Launch Python 2 or Python 3:
 * \code
 * python testpython.py
 * \endcode
 * 
 * In case of the 8SMC4-USB-Eth1 Ethernet adapter usage it is necessary to set correct IP address of the Ethernet adapter in testpython.py file before launch (see enum_hints variable).
 *
 * \section howtouse_matlab_sec MATLAB
 *
 * Sample MATLAB program testximc.m is provided at the directory examples/testmatlab.
 * On windows copy ximc.h, libximc.dll, bindy.dll, xiwrapper.dll and contents of ximc/(win32,win64)/wrappers/matlab/ directory to the current directory.
 *
 * Before launch:
 *
 * On OS X: copy ximc/macosx/libximc.framework, ximc/macosx/wrappers/ximcm.h,
 * ximc/ximc.h * to the directory examples/matlab. Install XCode compatible with Matlab.
 *
 * On Linux: install libximc*deb and libximc-dev*dev of target architecture.
 * Then copy ximc/macosx/wrappers/ximcm.h to the directory examples/matlab. Install gcc compatible with Matlab.
 *
 * For XCode and gcc version compability check document 
 * https://www.mathworks.com/content/dam/mathworks/mathworks-dot-com/support/sysreq/files/SystemRequirements-Release2014a_SupportedCompilers.pdf or similar.
 *
 * On Windows before the start nothing needs to be done
 *
 * Change current directory in the MATLAB to the examples/matlab.
 * Then launch in MATLAB prompt:
 * \code
 * testximc
 * \endcode
 *
 * In case of the 8SMC4-USB-Eth1 Ethernet adapter usage it is necessary to set correct IP address of the Ethernet adapter in testximc.m file before launch (see enum_hints variable).
 * 
 * \section howtouse_log Generic logging facility
 *
 * If you want to turn on file logging, you should run the program that uses libximc library with the "XILOG" environment variable set to desired file name.
 * This file will be opened for writing on the first log event and will be closed when the program which uses libximc terminates.
 * Data which is sent to/received from the controller is logged along with port open and close events.
 *
 * \section howtouse_perm Required permissions
 *
 * libximc generally does not require special permissions to work, it only needs read/write access to USB-serial ports on the system.
 * An exception to this rule is a Windows-only "fix_usbser_sys()" function - it needs elevation and will produce null result if run as a regular user.
 *
 * \section howtouse_cprofiles C-profiles
 * 
 * C-profiles are header files distributed with the libximc library. They enable one to set all controller settings for any of the supported stages with a single function call in a C/C++ program.
 * You may see how to use C-profiles in "testcprofile" example directory.
 *
 * \page userunit_sec Working with custom units
 *
 * In addition to working in basic units(steps, encoder value), the library allows you to work with custom units.
 * For this purpose are used: 
 * - The structure of the conversion units calibration_t
 * - The functions of which have doubles for working with custom units, data structures for these functions
 * - Coordinate correction table for more accurate positioning
 * 
 * \section userunit_calb1 The structure of the conversion units calibration_t
 *
 * To specify conversion of the basic units in the user and back, calibration_t structure is used.
 * With the help of coefficients A and MicrostepMode, specified in this structure, steps and microsteps which are integers are converted into the user value of the real type and back.
 *
 * Conversion formulas:
 * - The conversion to user units.
 * \verbatim
	user_value = A*(step + mstep/pow(2,MicrostepMode-1))
	\endverbatim
 * - Conversion from custom units.
 * \verbatim
	step = (int)(user_value/A)
	mstep = (user_value/A - step)*pow(2,MicrostepMode-1)
	\endverbatim
 *
 * \section userunit_calb2 Alternative functions for working with custom units and data structures for them
 * Structures and functions for working with custom units have the _calb postfix.
 * The user using these functions can perform all actions in their own units without worrying about the computations of the controller.
 * The data format of _calb structures is described in detail. For _calb functions particular descriptions are not used. They perform the same actions as the basic functions do.
 * The difference between them and the basic functions is in the position, velocity, and acceleration of the data types defined as user-defined. If clarification for _calb functions is necessary, they are provided as notes in the description of the basic functions.
 *
 * \section userunit_corr Coordinate correction table for more accurate positioning
 *
 * Some functions for working with custom units support coordinate transformation using a correction table.
 * To load a table from a file, the load_correction_table() function is used. Its description contains the functions and their data supporting correction.
 *
 * \note
 * For data fields which are corrected in case of loading of the table in the description of the field is written - corrected by the table.
 *
 * File format: 
 * - two columns separated by tabs; 
 * - column headers are string; 
 * - real type data, point is a separator; 
 * - the first column is the coordinate, the second is the deviation caused by a mechanical error; 
 * - the deviation between coordinates is calculated linearly; 
 * - constant is equal to the deviation at the boundary beyond the range; 
 * - maximum length of the table is 100 lines.
 *
 * Sample file:
 * \verbatim
	X	dX
	0	0
	5.0	0.005
	10.0	-0.01
    \endverbatim
 *
 * 
 */
