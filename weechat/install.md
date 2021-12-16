# install the dependencies
## find where they are

Check from what section of the repositories can the `weechat` package be installed:

    $ apt show weechat

You'll probably find this line:

    Section: universe/net

## download their source code

    $ sudoedit /etc/apt/sources.list

    # Uncomment the lines prefixed by `deb-src` and ending with `universe`.

            deb-src http://fr.archive.ubuntu.com/ubuntu/ xenial universe
            deb-src http://fr.archive.ubuntu.com/ubuntu/ xenial-updates universe

    $ sudo apt update

## install them

    $ sudo apt build-dep weechat

## install optional ones

Install some optional dependencies:

    $ sudo apt install asciidoctor libcpputest-dev

There may be more.  See:
<https://weechat.org/files/doc/devel/weechat_user.en.html#dependencies>

##
# clone the project

    $ git clone https://github.com/weechat/weechat

    # Optional: checkout the latest stable release
    $ git checkout v2.1-rc1

# prepare a build tree

    $ mkdir build
    $ cd build

# check what are the settings available to configure the compilation

    $ cmake -LAH
             │││
             ││└ display help for each variable
             ││
             │└ display also advanced variables
             │
             └ Run CMake  and list all the variables from  the CMake cache
               that are not marked as INTERNAL or ADVANCED.
               This will effectively display current CMake settings.

# generate a build system

            ┌ `cmake` must be passed the parent directory as argument,
            │ because the latter contains the file `CMakeLists.txt`,
            │ and `cmake` needs it
            │
            │   ┌ change a CMake setting ...
            │   │
            │   │┌ ... whose name is `CMAKE_BUILD_TYPE`
            │   ││
    $ cmake .. -DCMAKE_BUILD_TYPE:STRING=RelWithDebInfo \
               -DWEECHAT_HOME:STRING=~/.config/weechat  \
               -DENABLE_MAN:BOOL=ON                     \
               -DENABLE_DOC:BOOL=ON                     \
               -DENABLE_TESTS:BOOL=ON

Read the messages to check whether a (optional) dependency is missing.
If that's the case, try to find it here:
<https://weechat.org/files/doc/devel/weechat_user.en.html#dependencies>

---

Consider using the build type `Debug` to get more accurate info when you use `gdb(1)`:

    $ cmake .. -DCMAKE_BUILD_TYPE:STRING=RelWithDebInfo \
            ...

For more info about the difference between `RelWithDebInfo` and `Debug`, see:
<https://cmake.org/pipermail/cmake/2001-October/002479.html>

# compile

    $ make

---

If you can't re-compile, try to remove the following files/dirs:

    $ rm -rf CMakeCache.txt \
             CMakeFiles \
             CPackConfig.cmake \
             CPackSourceConfig.cmake \
             CTestTestfile.cmake \
             Makefile \
             build \
             cmake_install.cmake \
             cmake_uninstall.cmake \
             config.h \
             tags \
             weechat-2.2-dev-1.cygport \
             weechat.pc

# launch test(s)

    $ ctest -V

Launch the compiled binary:

    $ ./src/gui/curses/normal/weechat

If the executable is not there, here's how you can find where it's located:

    $ tree -aF | vipe
    /\<weechat\*

# install the binary

    $ sudo make install

