=============
hello cmake
=============

.. code-block:: cmake

    # Set the minimum version of CMake that can be used
    # To find the cmake version run
    # $ cmake --version
    cmake_minimum_required(VERSION 3.5)

    # Set the project name
    project (hello_cmake)

    # Add an executable
    add_executable(hello_cmake main.cpp)

    # Print CMAKE_BUILD_TYPE
    message(STATUS "Build type: ${CMAKE_BUILD_TYPE}")

-----------
Concepts
-----------

CMakeLists.txt
---------------

CMakeLists.txt is the file which should store all your CMake commands. When cmake is run in a folder it will look for this file and if it does not exist cmake will exit with an error.

Minimum CMake version
----------------------

When creating a project using CMake, you can specify the minimum version of CMake that is supported.

Creating an Executable
-----------------------

The add_executable() command specifies that an executable should be build from the specified source files, in this example main.cpp.
The first argument to the add_executable() function is the name of the executable to be built, and the second argument is the list of source files to compile.

----------------------
Building the Examples
----------------------

Below is sample output from building this example.

.. code-block:: bash

    $ mkdir build

    $ cd build

    $ cmake ..
    -- The C compiler identification is GNU 4.8.4
    -- The CXX compiler identification is GNU 4.8.4
    -- Check for working C compiler: /usr/bin/cc
    -- Check for working C compiler: /usr/bin/cc -- works
    -- Detecting C compiler ABI info
    -- Detecting C compiler ABI info - done
    -- Check for working CXX compiler: /usr/bin/c++
    -- Check for working CXX compiler: /usr/bin/c++ -- works
    -- Detecting CXX compiler ABI info
    -- Detecting CXX compiler ABI info - done
    -- Configuring done
    -- Generating done
    -- Build files have been written to: /workspace/cmake-examples/01-basic/hello_cmake/build

    $ make
    Scanning dependencies of target hello_cmake
    [100%] Building CXX object CMakeFiles/hello_cmake.dir/hello_cmake.cpp.o
    Linking CXX executable hello_cmake
    [100%] Built target hello_cmake

    $ ./hello_cmake
    Hello CMake!