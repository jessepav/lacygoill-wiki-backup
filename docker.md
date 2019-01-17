# Installation

Source:

        https://docs.docker.com/install/linux/docker-ce/ubuntu/#install-docker-ce-1


        $ sudo aptitude remove docker docker-engine docker.io
        $ sudo aptitude update

        $ sudo apt-get install \
            apt-transport-https \
            ca-certificates \
            curl \
            software-properties-common

        $ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

        $ sudo apt-key fingerprint 0EBFCD88 # compare displayed fingerprint with the one on the webpage

        $ sudo add-apt-repository \
           "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
           $(lsb_release -cs) \
           stable"

        $ sudo aptitude update

        $ sudo aptitude install docker-ce

        $ sudo docker run hello-world # to check the installation worked


