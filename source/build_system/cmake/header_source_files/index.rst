====================
头文件、源文件设置
====================

头文件路径设置
==================

When you have different include folders, you can make your compiler aware of them using the ``target_include_directories()`` function.
When compiling this target this will add these directories to the compiler with the -I flag e.g. ``-I/directory/path``

.. code-block:: cmake

    target_include_directories(target
        PRIVATE
            ${PROJECT_SOURCE_DIR}/include
    )

源文件设置
===========

It is typical to directly declare the sources in the add_xxx function. ``add_library`` ``add_executable``

Creating a variable which includes the source files allows you to be clearer about these files and easily add them to multiple commands,
for example, the add_executable() function.

.. code-block:: cmake

    # Create a sources variable with a link to all cpp files to compile
    set(SOURCES
        src/Hello.cpp
        src/main.cpp
    )

    add_executable(${PROJECT_NAME} ${SOURCES})

CMAKE 文件路径
==================

CMake syntax specifies a number of variables which can be used to help find useful directories in your project or source tree. Some of these include:

 - CMAKE_SOURCE_DIR: The root source directory
 - CMAKE_CURRENT_SOURCE_DIR: The current source directory if using sub-projects and directories.
 - PROJECT_SOURCE_DIR: The source directory of the current cmake project.
 - CMAKE_BINARY_DIR: The root binary / build directory. This is the directory where you ran the cmake command.
 - CMAKE_CURRENT_BINARY_DIR: The build directory you are currently in.
 - PROJECT_BINARY_DIR: The build directory for the current project.