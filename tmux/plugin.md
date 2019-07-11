# tmux-fingers
## It doesn't let me search outside the current screen!

Use our `M-c` key binding, which writes the whole scrollback buffer in a Nvim buffer.

##
## It wrongly renames the current window!

This is fixed by the unmerged PR #67:
<https://github.com/Morantron/tmux-fingers/pull/67/files>

We've merged it locally, but it may break in a future update.
Try to assimilate the plugin.

## Sometimes it fails, and gawk prints an error message!

I don't know how to fix this atm.

---

MWE:

Press `pfx ?`, then `pfx f`.

    gawk: ~/.tmux/plugins/tmux-fingers/scripts/hinter.awk:139: (FILENAME=- FNR=1) warning: regexp escape sequence `\"' is not a known regexp operator~

## Every time I press `pfx f`, my 'terminal-overrides' option is being appended with the item `,*:dim=\\E[2m`!

It comes from the `force_dim_support()` function called in
`~/.tmux/plugins/tmux-fingers/scripts/fingers.sh`.

Remove it; it seems useless.

##
## Why should I avoid installing tmux-copycat?

First, it installs a bunch of key bindings which are hard to remember.
And tmux namespace for key bindings seems rather small.

Besides, it's buggy:

   - it can be [slow][1]
   - remapping the Escape key in copy mode may [break][2] the plugin
   - after you use one of its key bindings, it may override and break some of yours

---

When you press a key binding from copycat, this line overrides some key bindings:

    # Source: ~/.tmux/plugins/tmux-copycat/scripts/copycat_mode_bindings.sh:42
    extend_key "$key" "$CURRENT_DIR/copycat_mode_quit.sh"

This is because `Y` is in the output of `copycat_quit_copy_mode_keys()` which is defined here:

    ~/.tmux/plugins/tmux-copycat/scripts/helpers.sh:160

The latter runs:

    tmux list-keys -T copy-mode-vi |
            \grep cancel |
            gawk '{ print $4 }' |
            sort -u |
            sed 's/C-j//g' |
            xargs echo

Basically, it finds any lhs of key binding whose rhs contains the pattern `cancel`.
And our current `Y` key binding *does* contain `cancel`:

    bind -T copy-mode-vi Y send -X copy-selection-and-cancel \; paste-buffer -p
                                                      ^^^^^^

---

Here's a command equivalent to what the plugin does with our original `Y` key binding:

    $ tmux bind -T copy-mode-vi Y run "tmux send -X copy-selection-and-cancel \
        ; paste-buffer -p \
        ; ~/.tmux/plugins/tmux-copycat/scripts/copycat_mode_quit.sh \
        ; true"

It's broken, because:

   1. the original rhs contained a semicolon
   2. the new rhs runs a shell command, where the semicolon has a special meaning
   3. a semicolon is special for the shell, and so needs to be escaped
   4. the plugin doesn't take care of escaping a semicolon from the original key binding

If you  remove everything after  `paste-buffer -p`, you  can see that  the shell
exits with  the error  code 127, because  it tried to  run `$  paste-buffer` and
didn't find it in `$PATH`.

    $ tmux bind -T copy-mode-vi Y run "tmux send -X copy-selection-and-cancel ; paste-buffer -p"
    # press pfx Y in copy-mode
    'tmux send -X copy-selection-and-cancel ; paste-buffer -p' returned 127~

##
# Reference

[1]: https://github.com/tmux-plugins/tmux-copycat/issues/129
[2]: https://github.com/tmux-plugins/tmux-copycat/blob/master/docs/limitations.md

