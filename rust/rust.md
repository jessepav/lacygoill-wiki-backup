# Installation
## Make sure you don't have a conflicting installation of Rust.

    $ apt purge cargo rustc

---

If you have an existing rust installation, in the next step, you'll get this warning:

   > it looks like you have an existing installation of Rust at:
   > /usr/bin
   > rustup should not be installed alongside Rust. Please uninstall your existing Rust first.
   > Otherwise you may have confusion unless you are careful with your PATH
   > If you are sure that you want both rustup and your already installed Rust
   > then please reply `y` or `yes` or set RUSTUP_INIT_SKIP_PATH_CHECK to yes
   > or pass `-y` to ignore all ignorable checks.

## Make sure a C compiler is installed.

    $ apt install gcc

Indeed, the rust compiler needs a C linker, which `gcc(1)` can provide.
Also, some common Rust packages depend on C code and will need a C compiler.

##
## Download the installer and execute it.

    $ curl --proto '=https' --tlsv1.3 --fail --show-error --silent https://sh.rustup.rs | \sh

---

`--proto` tells curl it is only allowed to use some protocol(s) in the transfer.
Here, we only want to allow the https protocol.

`=` is a modifier:

    --proto '=https'
             ^

`+` and `-` are other possible modifiers:

   - `+`: add the next named protocol to the list of allowed protocols
   - `-`: remove the next named protocol from the list of allowed protocols
   - `=`: only allow the next named protocol

By default, `+` is assumed.
For maximum security, you want `=`.

---

`--tlsv1.3` forces  curl to use  TLS version 1.3 or  later when connecting  to a
remote TLS server.

---

If the remote server  can't give us the desired installer  script, it might give
us an HTML document explaining why.  We don't want an HTML document; we want the
installer.
If we can't have  the installer, then we just want curl to  fail with a non-zero
exit code.  That's the purpose of `--fail`.

`--silent` prevents curl from printing a progress meter, or error messages.

`--show-error`  makes  curl print  an  error  message  if  it fails;  useful  in
combination with `--silent`.

The 3 options can be shortened into `-sSf`.

### The installer will install various files, whose locations can be configured.

Rustup metadata and toolchains will be installed into the Rustup home directory, located at:

    $HOME/.rustup

This can be modified with the `RUSTUP_HOME` environment variable.

---

The Cargo home directory located at:

    $HOME/.cargo

This can be modified with the `CARGO_HOME` environment variable.

---

The  cargo, rustc,  rustup  and other  commands  will be  added  to Cargo's  bin
directory, located at:

    $HOME/.cargo/bin

This path  will then be added  to your `PATH` environment  variable by modifying
the profile files located at:

    $HOME/.profile
    $HOME/.bash_profile
    $HOME/.bashrc
    $HOME/.zshenv

In each of them, a `source` command will be added to source this file:

    $HOME/.cargo/env

If  you  use zsh,  I  think  you can  undo  all  those editions;  provided  that
you  manually  include the  `${HOME}/.cargo/bin`  directory  in your  `PATH`  in
`~/.zshenv`:

    export PATH=...:${HOME}/.cargo/bin:...
                    ^----------------^

##
## To get the current version of the rust compiler:

    $ rustc --version

## To update the rustup tool:

    $ rustup udate

## To uninstall rust entirely:

    $ rustup self uninstall

##
# Resources
## Offline documentation

To read the main book which teaches you the language itself:

    $ rustup docs --book

---

This gives access to  a series of books, each dedicated to  some tool or concept
about rust:

    $ rustup doc

Notice the  input field  in the middle  of the page,  right below  "The Standard
Library  section"; it  lets you  search  for the  documentation on  any type  or
function provided by the standard library.  Useful  to learn what they do or how
to use them.

## Online documentation

- <https://doc.rust-lang.org/>
- <https://tourofrust.com/index.html>
- <https://rust-unofficial.github.io/patterns/intro.html>

## Support

Forum where you can ask questions: <https://users.rust-lang.org/>

Also, on IRC, you can visit the `##rust` channel on the libera network.
