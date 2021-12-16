# How to test the Alpine Linux OS in a docker container?

    # install docker
    $ sudo apt install docker.io

    # start Alpine in a docker container
    $ sudo docker run --interactive=true --tty=true --rm=true alpine

Can be shortened into:

    $ sudo docker run -it --rm alpine

---

`--interactive` keeps STDIN open even if not attached.

`--tty` allocates  a pseudo-TTY letting Docker  attach to the standard  input of
any container.  Here, it's necessary to run an interactive shell in which we can
run commands to interact with Alpine.

`--rm` automatically removes the container when it exits.

For more info, `man docker-run`.

## How to remove the docker container?

    $ sudo docker system prune --all
    WARNING! This will remove:
      - all stopped containers
      - all networks not used by at least one container
      - all images without at least one container associated to them
      - all build cache

    Are you sure you want to continue? [y/N] y
    ...

    Total reclaimed space: ...

`$ docker system prune` removes unused data.
`--all` removes *all* unused images, not just dangling ones.

For more info, `man docker-system-prune`.

##
# How to get a more recent version of Docker?

    # uninstall old versions
    $ sudo apt remove docker docker-engine docker.io containerd runc

    # update the apt package index,
    # and install packages to allow apt to use a repository over HTTPS
    $ sudo apt update &&
      sudo apt install &&
               ca-certificates \
               curl \
               gnupg \
               lsb-release

    # add Docker's official GPG key
    $ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
        sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

     # set up the stable repository
     $ echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
      $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

    # update the apt package index,
    # and install the latest version of Docker Engine and containerd
    $ sudo apt update && sudo apt install docker-ce docker-ce-cli containerd.io

    # verify that Docker Engine is installed correctly by running the hello-world image
    $ sudo docker run hello-world

For more info: <https://docs.docker.com/engine/install/ubuntu/>

