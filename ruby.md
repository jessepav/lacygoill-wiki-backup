# How to install a ruby gem locally, in my home?

Pass `--user-install` to `$ gem install`.

Example:

    $ gem install --user-install heytmux

For more help about `$ gem install`, run `$ gem help install`.

##
# Issues
## I can't install any ruby gem!

So, you have this kind of error message.

    ERROR:  Could not find a valid gem 'heytmux' (>= 0), here is why:
              Unable to download data from https://rubygems.org/ - Errno::ECONNRESET: Connection reset by peer - SSL_connect (https://api.rubygems.org/specs.4.8.gz)

Use a proxy:

    $ https_proxy=<IP Address>:<Port> ruby gem install --user-install <gem>

See here for a list of proxies: <https://www.us-proxy.org/>
Make sure to choose a proxy supporting http*s*.

You  may need  to  try several  proxies  before finding  one  which succeeds  in
installing a gem.

## When I install a ruby gem, I'm being warned that it's not in my path!

    WARNING:  You don't have /home/user/.gem/ruby/2.3.0/bin in your PATH,
    gem executables will not run.

Remove `${HOME}/.ruby_user_dir_cache`.

---

You can get the path to the ruby gems installed in your home via:

    $ ruby -e 'puts Gem.user_dir'

You need to add the output of this command to your `PATH`.
We do it in in our `~/.zshenv`.

However, since a shell command takes time to be executed, we cache the output in
a file, to avoid slowing down the shell startup time.
You may have updated ruby, and the output of the command may have changed, while
your cache is still the same; IOW, your cache may be stale.

