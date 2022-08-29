# Cargo

Rust's build system and package manager for the Rust programming language.

It handles a lot of tasks for you, such as:

   - building your code
   - downloading the libraries your code depends on (aka dependencies)
   - building dependencies

You can check whether Cargo is installed (and under which version) with:

    $ cargo --version

# crate

The  compilation model  centers on  artifacts called  crates.  Each  compilation
processes a  single crate in source  form, and if successful,  produces a single
crate in binary form: either an executable or some sort of library.

Source: <https://doc.rust-lang.org/reference/crates-and-source-files.html#crates-and-source-files>

A crate is declared in the `[lib]` or `[[bin]]` table in the `Cargo.toml` manifest.
At most  one lib crate  may be  present, but an  arbitrary number of  bin crates
may  be  present.  You  won't  see  these  tables  added explicitly  too  often,
because they're implicitly  present if you have `src/lib.rs`  (lib crate) and/or
`src/main.rs` (bin crate).

Source: <https://www.reddit.com/r/rust/comments/lvtzri/confused_about_package_vs_crate_terminology/gpdti5j/>

# channel

Rust is released to three different "channels"; stable, beta, and nightly:

   - the stable releases are made every 6 weeks
   - beta releases are the version that will appear in the next stable release
   - nightly releases are made every night

# edition

The  Rust language  and  compiler have  a six-week  release  cycle, with  number
versions such as 1.10 or 1.31.

Every two  or three  years, the  Rust team  produces a  new Rust  edition.  Each
edition brings together the features that  have landed into a clear package with
fully updated documentation and tooling.  New editions ship as part of the usual
six-week release process.

An edition brings together incremental changes into an easy-to-understand package.

At the moment, two Rust editions are available: Rust 2015 and Rust 2018.

In a  project's `Cargo.toml` file, the  edition key indicates which  edition the
compiler should use for your code.  If  the key doesn't exist, Rust uses 2015 as
the edition value for backward compatibility reasons.

For more info, see:
<https://doc.rust-lang.org/stable/edition-guide/editions/index.html>

# manifest

A manifest  file contains metadata  for a group  of accompanying files  that are
part of a  set or coherent unit.   For example, the files of  a computer program
may  have a  manifest  describing  the name,  version  number,  license and  the
constituent files of the program.

The term  is borrowed  from a  cargo shipping procedure,  where a  ship manifest
would list the crew and/or cargo of a vessel.

Source: <https://en.wikipedia.org/wiki/Manifest_file>

# package

A package is what you're describing in the `[package]` table of the `Cargo.toml`
manifest.  It's meant to be managed by Cargo, the Rust package manager.

---

In practice, the terms package and crate are often used interchangeably.

   > Generally the  main artifact of a  package is a  library crate, and since  it is
   > identified with the package name, it is  customary to treat package and crate as
   > synonyms.

Source: <https://stackoverflow.com/a/52072169>

# rustup

rustup is a toolchain multiplexer.  It installs and manages many Rust toolchains
and presents them all through a single set of tools installed to `~/.cargo/bin`.
The rustc  and cargo  executables installed in  `~/.cargo/bin` are  proxies that
delegate to the real toolchain. rustup then provides mechanisms to easily change
the active toolchain by reconfiguring the behavior of the proxies.

In practice,  this mechanism lets  you easily  switch between stable,  beta, and
nightly compilers and keep them  updated.

So  when  rustup  is first  installed,  running  rustc  will  run the  proxy  in
`$HOME/.cargo/bin/rustc`, which  in turn will  run the stable compiler.   If you
later change the  default toolchain to nightly with `$  rustup default nightly`,
then that same proxy will run the nightly compiler instead.

# toolchain

A complete  installation of the  Rust compiler  (rustc) and related  tools (like
cargo).  A toolchain specification includes  the release channel or version, and
the host platform that the toolchain runs on.

See: <https://rust-lang.github.io/rustup/concepts/toolchains.html>

