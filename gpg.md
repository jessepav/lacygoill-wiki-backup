# How to get rid of the warning which I sometimes encounter when checking the signature of an archive?

    $ gpg --edit-key <8 hex digits public key ID>
    gpg> trust
        1 = I don't know or won't say˜
        2 = I do NOT trust˜
        3 = I trust marginally˜
        4 = I trust fully˜
        5 = I trust ultimately˜
        m = back to the main menu˜
    Your decision? 5

See:
- <https://serverfault.com/a/569923>
- <https://security.stackexchange.com/a/69089>
