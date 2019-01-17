https://www.reddit.com/r/vim/comments/6awwk5/configuring_fzf_preview/

Essaye ça:

        fzf --preview 'cat {}'

Ça lance fzf en affichant pour chaque entrée sélectionnée une prévisualisation via `cat`.
