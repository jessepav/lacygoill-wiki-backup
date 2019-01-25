# ?

<https://www.reddit.com/r/vim/comments/6awwk5/configuring_fzf_preview/>

Essaye ça:

        fzf --preview 'cat {}'

Ça lance fzf en affichant pour chaque entrée sélectionnée une prévisualisation via `cat`.

# ?

Here's an example of integration of fzf in Vim.
We define a  custom command `:FzfSnippets` to fuzzy search  through our snippets
and their descriptions.
In practice,  it's useless if you  use `fzf.vim`, because the  latter installs a
similar command.
But I  keep this code here,  because it illustrates  how you can build  your own
commands.
It could also be useful to elminate `fzf.vim`.

Note that this code doesn't call any function from `fzf.vim`.
It relies on `fzf#run()` and `fzf#wrap()` which are installed in `~/.fzf/plugin/fzf.vim`.
The latter is installed by `fzf` itself.

    command! -bar -bang FzfSnippets call s:fzf_snippets(<bang>0)
    function! s:fzf_snippets(bang) abort
        let list = UltiSnips#SnippetsInCurrentScope()
        if empty(list)
            echohl WarningMsg | echom 'No snippets available here' | echohl None
        endif
        let aligned = sort(s:align_lists(items(list)))
        let colored = map(aligned, {i,v -> "\x1b[33m" . v[0] . "\x1b[m\t" . v[1]})
        call fzf#run(fzf#wrap('snippets', {
            \ 'source':  colored,
            \ 'options': '--ansi --tiebreak=index +m',
            \ 'sink':    function('s:inject_snippet')}, a:bang))
    endfunction
    function! s:align_lists(lists) abort
        let maxes = [0, 0]
        for list in a:lists
            call map(maxes, {i,v -> max([maxes[i], len(list[i])])})
        endfor
        for list in a:lists
            call map(list, {i,v -> printf('%-' . maxes[i] . 's', v)})
        endfor
        return a:lists
    endfunction
    function! s:inject_snippet(line) abort
        let snip = trim(split(a:line, "\t")[0])
        execute 'normal! a'.snip."\<c-r>=UltiSnips#ExpandSnippet()\<cr>"
    endfunction

