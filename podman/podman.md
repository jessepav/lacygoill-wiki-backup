# How to install Podman?

On a Fedora-based systems:

    $ sudo dnf install podman-docker

On Debian-based systems:

    $ sudo apt install podman

For more info: <https://podman.io/getting-started/installation>

---

On Ubuntu, the `podman` package is not available before 20.10.
But you can install it on Ubuntu 20.04 via a PPA:

    $ echo 'deb https://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable/xUbuntu_20.04/ /' \
        | sudo tee /etc/apt/sources.list.d/devel:kubic:libcontainers:stable.list
    $ curl --fail --location --show-error --silent 'https://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable/xUbuntu_20.04/Release.key' \
        | sudo apt-key add -
    $ sudo apt-get update
    $ sudo apt-get -y install podman

See: <https://podman.io/getting-started/installation#linuxmint-20x>

# Where can I download the (updated) example code files for the book “Podman for DevOps”?

<https://github.com/PacktPublishing/Podman-for-DevOps>
