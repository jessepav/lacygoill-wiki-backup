# ?

Commandes de configuration

Chaque option fenêtre ou session existe en 2 versions, locale ou globale.
La version locale s'applique uniquement à la fenêtre / session courante.
La globale à toutes les fenêtres / sessions.

En cas de conflit, la locale a la priorité sur la globale.

Si la locale n'est pas configurée explicitement, elle est héritée de la globale.


En plus des options par défaut, un utilisateur peut créer ses propres options.
Pour ce faire, il doit préfixer leur nom avec ’@’.
Une option utilisateur accepte comme valeur une chaîne arbitraire.


La valeur d'une option peut être un booléen, un nombre, une chaîne ou une array.
Un flag peut être on, off ou omis.


    Affiche les options:

    ┌──────────────────┬─────────────────────┐
    │ show-options -s  │ serveur             │
    ├──────────────────┼─────────────────────┤
    │ show-options     │ session et locales  │
    ├──────────────────┼─────────────────────┤
    │ show-options -g  │ session et globales │
    ├──────────────────┼─────────────────────┤
    │ show-options -w  │ fenêtre et locales  │
    ├──────────────────┼─────────────────────┤
    │ show-options -gw │ fenêtre et globales │
    └──────────────────┴─────────────────────┘

            `show` est un alias de `show-options`.

            À la place de `show-options -w`, on peut aussi utiliser:

                    - showw
                    - show -w
                    - show-window-options


    Donne la valeur `val` à l'option `opt`, cette dernière étant une option:

    ┌─────────────────────────┬────────────────────┐
    │ set-option -s   opt val │ serveur            │
    ├─────────────────────────┼────────────────────┤
    │ set-option      opt val │ session et locale  │
    ├─────────────────────────┼────────────────────┤
    │ set-option -g   opt val │ session et globale │
    ├─────────────────────────┼────────────────────┤
    │ set-option -w   opt val │ fenêtre et locale  │
    ├─────────────────────────┼────────────────────┤
    │ set-option -gw  opt val │ fenêtre et globale │
    └─────────────────────────┴────────────────────┘

            `set` est un alias de `set-option`.

            À la place de `set-option -w`, on peut aussi utiliser:

                    - setw
                    - set -w
                    - set-window-option


    show-options -gv opt

            Affiche la valeur globale de l'option session `opt` sans afficher son nom (flag `-v`).

            Montre qu'on peut limiter la sortie de `show-options` de 2 façons:

                    - flag `-v`      supprime les noms des options
                    - argument `opt` supprime toutes les options différentes de `opt`


    set-option -g  status-left 'foo'
    set-option -ag status-left 'bar'

            Configure l'option session `status-left` en lui donnant la valeur `foo`.
            Puis, lui ajoute (append) la valeur `bar`.
            La valeur finale est donc `foobar`.

            Le flag `-a` permet d'ajouter (append) une chaîne/un style à une option.


    set-option -g  status-style 'bg=red'
    set-option -ag status-style 'fg=blue'

            Configure l'option session `status-style` en lui donnant la valeur `'bg=red'`.
            `'bg=red'` est un style.
            Puis, lui ajoute le 2e style `'fg=blue'`.

            Le résultat est un avant-plan bleu et un arrière-plan rouge.
            Sans le flag `-a`, le résultat serait un avant-plan bleu et un arrière-plan NOIR (valeur par défaut).


Les commandes `set-option`, `show-options`, `set-window-option` et `show-window-options`
acceptent également les arguments suivants:

    ┌───────────────┬─────────────────────────────────────────────────────┐
    │ -o            │ ne configure pas l'option si elle a déjà une valeur │
    ├───────────────┼─────────────────────────────────────────────────────┤
    │ -q            │ supprime un éventuel message d'erreur               │
    │               │ (option inconnue ou ambigüe)                        │
    ├───────────────┼─────────────────────────────────────────────────────┤
    │ -u            │ supprime la valeur locale d'une option,             │
    │               │ de sorte qu'elle hérite de la globale               │
    ├───────────────┼─────────────────────────────────────────────────────┤
    │ -gu           │ supprime la valeur globale d'une option,            │
    │               │ de sorte qu'elle récupère sa valeur par défaut      │
    ├───────────────┼─────────────────────────────────────────────────────┤
    │ -t my_window  │ configure ou affiche une option d'une fenêtre       │
    │ -t my_session │ ou session arbitraire                               │
    └───────────────┴─────────────────────────────────────────────────────┘

##
# Getting info
## Why doesn't `$ tmux show-options mouse` show anything?

Because you're asking for the value local to the current session, and there's none.

OTOH, if you ask for the *global* value, you will have an output:

    $ tmux show-options -g mouse
    mouse on~

##
# Setting an option
## What happens if I
### omit `-g` when I set a session or window option in `~/.tmux.conf`?

Tmux will complain with one of these error messages:

    no current session
    no current window

### don't provide a value to `$ tmux set-option <boolean option>`?

The option is toggled between on and off.

    $ tmux set-option -g mouse && tmux show-options -g mouse
    mouse off~

    $ tmux set-option -g mouse && tmux show-options -g mouse
    mouse on~

##
# Array options
## What is an array option?

An option whose final value is an array of items.

##
## Currently, there are 6 of them.  What are their names?

   - 'command-alias'
   - 'status-format'
   - 'terminal-overrides'
   - 'update-environment'
   - 'user-keys'

Hooks are also stored as array options.

### How can I find them quickly in the manpage?

Search for the pattern `[]`.

##
## How to add an item to an array option?  (2)

With the `-a` flag:

    $ tmux show user-keys
    user-keys~

    $ tmux set -a user-keys "\e[123"
    $ tmux show user-keys
    user-keys[0] \\e[123~

    $ tmux set user-keys ''

---

Or with an `[123]` index:

    $ tmux show user-keys
    user-keys~

               necessary for zsh, where `[` and `]` have a special meaning
               v            v
    $ tmux set 'user-keys[0]' "\e[123"
    $ tmux show user-keys
    user-keys[0] \\e[123~

    $ tmux set user-keys ''

### What's the benefit of the first method?

It can't overwrite an existing item.

When you use the second method, there *is* such a risk.
To avoid it, you need to know the size of the array.

    $ tmux set 'user-keys[<size>]' "\e[123"
                          ├────┘
                          └ if the size of the array is 3,
                            then the array contains the items of index 0, 1 and 2;
                            the item of index 3 is free

#### What's its drawback?

You have to make sure not to append the same value every time you resource tmux.conf.

To do so, write a guard surrounding the setting:

    if '[ "$TERM" != "#{default-terminal}" ]' { ... }

If there're several settings, group them (possibly  in a file), so that you only
have 1 guard to write.

##
## How to reset the whole value of an array option?

Don't use `-a` nor `[123]`.

    $ tmux set user-keys "\e[123"
    $ tmux show-options user-keys
    user-keys[0] "\\e[123"~

##
## Comma
### When do I need a comma to set the value of an array option?

When you want to set several items of the array in a single command.
In this case, the comma tells tmux when a item ends, and when the next one starts.

    $ tmux set user-keys 'foo,bar'
    $ tmux show user-keys
    user-keys[0] foo~
    user-keys[1] bar~

#### But a comma is used in other contexts in `example_tmux.conf` and in the faq!

Example from `example_tmux.conf`:

<https://github.com/tmux/tmux/blob/e8f4ca6a52bdfb7d8e2b8c39b867f2e2528a7631/example_tmux.conf#L17>

    set-option -as terminal-overrides ",xterm*:Tc"
                                       ^

and from the faq:

<https://github.com/tmux/tmux/wiki/FAQ#how-do-i-use-rgb-colour>

    set -as terminal-overrides ",gnome*:RGB"
                                ^

<https://github.com/tmux/tmux/wiki/FAQ#why-are-tmux-pane-separators-dashed-rather-than-continuous-lines>

    set -as terminal-overrides ",*:U8=0"
                                ^
##### Why?

I think that before 2.3, 'terminal-overrides' was a string option.

> * terminal-overrides and update-environment are now array options (the previous
<https://github.com/tmux/tmux/blob/8382ae65b7445a70e8a24b541cf104eedadd7265/CHANGES#L575>

And maybe a comma was needed for a string option.

But anyway, now, 'terminal-overrides' is an array option.
So, a comma should be useless most of the time.

---

If you want to be sure, try this experiment.

    set -s  terminal-overrides 'xterm*:Tc'
    set -as terminal-overrides 'st*:Cs=\E]12;%p1%s\007'

If tmux didn't split after  the value of 'terminal-overrides' after `xterm*:Tc`,
then it would consider `xterm*` as being  the terminal type pattern for the `Cs`
capability, which would  prevent us from resetting the color  of the cursor with
`$ printf '\033]12;3\007'` in st (since 'st-256color' doesn't match 'xterm*').
And yet,  in practice, we can  reset the color of  the cursor in st  + tmux with
this minimal `tmux.conf`.

###
### For 'terminal-overrides', do I need a comma to separate two capabilities for the same terminal type pattern?

No.

    $ tmux -Ltest -f/dev/null new
    $ tmux show-options -s terminal-overrides
    terminal-overrides[0] "xterm*:XT:Ms=\\E]52;%p1%s;%p2%s\\007:Cs=\\E]12;%p1%s\\007:Cr=\\E]112\\007:Ss=\\E[%p1%d q:Se=\\E[2 q"~
    terminal-overrides[1] "screen*:XT"~

Notice how the Ms, Cs, Cr, Ss, Se capabilities:

   - are on the same line
   - apply to the same terminal type pattern `xterm*`
   - are not separated by commas

##
# Issues
## Some options which set colors don't work!

Do you use hex color codes, and does your terminal support true colors?
If the answers are yes and no, then make sure the following line is not run when
tmux is started from your terminal:

    set -as terminal-overrides ',*-256color:Tc'

Setting `Tc` may prevent other settings to work, like these for example:

    set -gw window-style        'bg=#cacaca'
    set -gw window-active-style 'bg=#dbd6d1'

This issue is specific to terminals which don't support true colors.

Alternatively, you could use:

   - `colour123` instead of `#ab1234`
   - a terminal supporting true colors

---

MWE:

     $ cat <<'EOF' >/tmp/tmux.conf

     set -as terminal-overrides ',*-256color:Tc'
     set -gw window-style         'bg=#000000'
     set -gw window-active-style  'bg=#ffffff'

     set -g prefix 'M-space'
     unbind '"'
     bind _ splitw -v
     bind M-space last-pane
     EOF

     $ tmux -Ltest -f/tmp/tmux.conf

     pfx _
     pfx SPC

