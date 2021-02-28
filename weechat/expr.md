# What's the expression evaluated to...
## the name of the current server?

    ${server}

## the type of the current buffer (channel, server, ...)?

    ${type}

## 1 if the type of the current buffer is a channel, 0 otherwise?

    ${if:${type}==channel}

---

This is a shorthand for:

    ${if:${type}==channel?1:0}

---

You need the `${if:}` part to evaluate the expression as a condition.
Otherwise, WeeChat would just evaluate `${type}`:

    /eval -n ${type}==channel
    [channel==channel]~

Alternatively if you use `/eval`, you could add the `-c` option:

    /eval -c -n ${type}==channel
          ├───┘
          └ you can't merge the options (`-cn` ✘)

##
## the name of the current buffer?   (2)

    ${buffer.name}
    ${buffer.full_name}

`full_name`, contrary to `name`, includes the name of the plugin which created the buffer.

See here for all possible buffer-related info you can get:
<https://weechat.org/files/doc/stable/weechat_plugin_api.en.html#_buffer_get_string>

## the name the plugin which created the current buffer?   (2)

    ${buffer.plugin.name}
    ${plugin}

`${buffer.plugin.name}`  evaluates  to  an  empty string  in  the  core  buffer,
contrary to `${plugin}` which evaluates to 'core'.

## the name of the dictionary used in the current buffer?

    ${info:aspell_dict,${buffer.full_name}}
           │           │
           │           └ required argument
           │
           └ name of the info we want

See here for all possible WeeChat or plugin-related info you can get:
<https://weechat.org/files/doc/stable/weechat_plugin_api.en.html#_info_get>

##
## the substring 'bar' from the string 'foobar'?

    ${rev:${cut:3,,${rev:foobar}}}
            │
            └ From `/help eval`:

                    4. a string with max chars, format:
                           "cut:max,suffix,string" or "cut:+max,suffix,string"

                       or max chars displayed on screen, format:
                           "cutscr:max,suffix,string" or "cutscr:+max,suffix,string"

Source: <https://github.com/weechat/weechat/issues/1200>

## the repetition of the string '-abc-' 5 times?

    ${repeat:5,-abc-}

