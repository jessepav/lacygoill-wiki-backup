# How to see all packages which can be reconfigured?

    $ debconf-show --listowners

##
# How to see how a package is currently configured?

    $ debconf-show <package>

## How to see the questions which were asked to configure it?

    $ debconf-get-selections

This will  dump the whole  debconf database,  and the questions/answers  are not
grouped by package,  so you'll need to  grep for the name of  the package you're
interested in.

Besides it requires the package `debconf-utils` to be installed.

## How to reconfigure the package?

    $ sudo dpkg-reconfigure <package>

### How to interact with readline instead of ncurses?

    $ sudo DEBIAN_FRONTEND=readline dpkg-reconfigure <package>
           ^----------------------^

##
# How to install a package and make APT ask us all possible questions to configure it?

    $ sudo DEBIAN_PRIORITY=low apt install <package>
           ^-----------------^

