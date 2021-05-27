# Todo

We've installed tig from the sources:

    $ git clone https://github.com/jonas/tig

    $ make prefix=/usr/local
    $ sudo make install prefix=/usr/local

    $ make install-doc
       [...]
       INSTALL  doc/tig.1 -> /home/user/share/man/man1
       INSTALL  doc/tigrc.5 -> /home/user/share/man/man5
       INSTALL  doc/tigmanual.7 -> /home/user/share/man/man7
       [...]
       INSTALL  doc/tig.1.html -> /home/user/share/doc/tig
       INSTALL  doc/tigrc.5.html -> /home/user/share/doc/tig
       INSTALL  doc/manual.html -> /home/user/share/doc/tig
       INSTALL  README.html -> /home/user/share/doc/tig
       INSTALL  INSTALL.html -> /home/user/share/doc/tig
       INSTALL  NEWS.html -> /home/user/share/doc/tig

Read this: <https://github.com/jonas/tig/blob/master/INSTALL.adoc>

---

Read this glossary: <https://gitirc.eu/gitglossary.html>
This comes from a site associated to the `#git` irc channel on libera.
Check out the site for other possible interesting links.

Also, atm, the channel has a public logfile for each day:
<https://colabti.org/irclogger/irclogger_logs/git>
So, if you get disconnected, and want to check what you missed when you come back, visit:
<https://gitirc.eu/log>

---

Learn how to use `git-jump`.
Read `~/bin/README.md`, and read this to populate a qfl with the output:
- <https://vi.stackexchange.com/q/13433/17449>
- <https://gist.github.com/romainl/a3ddb1d08764b93183260f8cdf0f524f>

---

- <https://github.com/so-fancy/diff-so-fancy>
- <https://www.reddit.com/r/vim/comments/bkz81t/vimdiff_nor_nvim_d_are_working_as_an_external/emlntpu/>
- <https://www.reddit.com/r/vim/comments/bkz81t/vimdiff_nor_nvim_d_are_working_as_an_external/emkges3/>

---

Read: <https://chris.beams.io/posts/git-commit/>

---

Read:

    $ git help <guide>

Where `<guide>` is any guide given in the output of:

    $ git help -g

---

How to create automatically a repository-local `.gitignore` file when starting a
new project?

Maybe we  should use vim-projectionist  to automatically create them,  using the
relevant file from here as a template: <https://github.com/github/gitignore>

In particular, it would be interesting to copy the LaTeX and python files.

---

Learn to use the buffer-local commands/mappings installed by:

    $VIMRUNTIME/ftplugin/gitcommit.vim
    $VIMRUNTIME/ftplugin/gitrebase.vim

See also `:h ft-gitcommit-plugin`.

---

Document the option `rerere.autoUpdate` (see `man git-config`).
We've found it on page 28 (statusline) in the Pro Git book.
Do  it once  you've studied  the “rerere”  feature (REuse  REcorded REsolution),
which the book talks about.

---

- <https://try.gitea.io/>
- <https://www.reddit.com/r/linux/comments/8oziba/gitea_is_a_very_lightweight_github_clone_but_i/e07r34f/>
- <https://docs.gitea.io/en-us/config-cheat-sheet/>

---

Read:

- <https://gist.github.com/CristinaSolana/1885435>
- <https://github.com/edx/edx-platform/wiki/How-to-Rebase-a-Pull-Request>
- <https://help.github.com/articles/checking-out-pull-requests-locally/>
- <https://vimways.org/2018/vim-and-git/>

---

<https://github.com/github/hub/releases>

hub est un wrapper en cli autour de git qui ajoute à ce dernier des commandes et
des fonctionnalités, pour faciliter le travail avec GitHub.

On peut l'installer en téléchargeant  la dernière release, puis en décompressant
l'archive et en exécutant le script d'installation:

    $ sudo ./install

Ça devrait aussi installer les pages man du pgm.  Les lire:

    man hub

---

- <https://stackoverflow.com/a/9784089>
- <https://stackoverflow.com/a/8498197>

Merging without whitespace conflicts
Commit without whitespace changes on github

---

Read: <http://michaelwales.com/articles/make-gitconfig-work-for-you/>

---

Read: <https://github.blog/2020-02-12-supercharge-your-command-line-experience-github-cli-is-now-in-beta/>
