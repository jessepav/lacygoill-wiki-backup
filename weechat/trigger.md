https://weechat.org/files/doc/stable/weechat_user.en.html#trigger_plugin

Trigger is the  Swiss Army knife for  WeeChat: it can hook  many things (signal,
modifier,  print, …),  change  the content  of  data, and  execute  one or  more
commands.
A condition can be used to prevent the trigger to run in some circumstances.

Using triggers require you to know how the signals, modifiers, … are working.
So you might consider reading the WeeChat plugin API reference / Hooks.

# Anatomy of a trigger

A trigger has the following options:

┌─────────────┬──────────────────────────────┬────────────────────────────────────────────────────────────────────┐
│ Option      │ Values                       │ Description                                                        │
├─────────────┼──────────────────────────────┼────────────────────────────────────────────────────────────────────┤
│ enabled     │ on, off                      │ When option is off, the trigger is disabled                        │
│             │                              │ and actions are not executed any more.                             │
├─────────────┼──────────────────────────────┼────────────────────────────────────────────────────────────────────┤
│             │ signal, hsignal, modifier,   │ The hook used in trigger. For more information, see WeeChat        │
│ hook        │ print, command, command_run, │ plugin API reference / Hooks.                                      │
│             │ timer, config, focus         │                                                                    │
├─────────────┼──────────────────────────────┼────────────────────────────────────────────────────────────────────┤
│ arguments   │ string                       │ The arguments for the hook, it depends on the hook type used.      │
├─────────────┼──────────────────────────────┼────────────────────────────────────────────────────────────────────┤
│ conditions  │ string                       │ Conditions to execute the trigger; they are evaluated              │
│             │                              │ see /eval).                                                        │
├─────────────┼──────────────────────────────┼────────────────────────────────────────────────────────────────────┤
│             │                              │ One or more POSIX extended regular expressions, to change data     │
│ regex       │ string                       │ received in the hook callback (and some stuff added by trigger     │
│             │                              │ plugin), see regular expression.                                   │
├─────────────┼──────────────────────────────┼────────────────────────────────────────────────────────────────────┤
│ command     │ string                       │ Command to execute (many commands can be separated by semicolons); │
│             │                              │ it is evaluated (see /eval).                                       │
├─────────────┼──────────────────────────────┼────────────────────────────────────────────────────────────────────┤
│ return_code │ ok, ok_eat, error            │ The return code of callback (default is ok, which should be used   │
│             │                              │ in almost all triggers, the other values are rarely used).         │
├─────────────┼──────────────────────────────┼────────────────────────────────────────────────────────────────────┤
│             │                              │ Action to take on the trigger after execution                      │
│ post_action │ none, disable, delete        │ (default is none which should be used in almost all triggers,      │
│             │                              │ the other values are rarely used).                                 │
└─────────────┴──────────────────────────────┴────────────────────────────────────────────────────────────────────┘

The full name of a trigger option is:

        trigger.trigger.<trigger_name>.<option>

For example, the default beep trigger has the following options:

        trigger.trigger.beep.enabled = on
        trigger.trigger.beep.hook = print
        trigger.trigger.beep.arguments = ""
        trigger.trigger.beep.conditions = "${tg_highlight} || ${tg_msg_pv}"
        trigger.trigger.beep.regex = ""
        trigger.trigger.beep.command = "/print -beep"
        trigger.trigger.beep.return_code = ok
        trigger.trigger.beep.post_action = none

# Execution

When a trigger callback is called, following actions are executed, in this order, if triggers are globally enabled and
if the trigger itself is enabled:

 1. check trigger conditions: if false, exit

 2. replace text in trigger using regular expression(s)

 3. execute command(s)

 4. exit with a return code (except for hooks modifier and focus)

 5. perform post action (if different from none).

# Hook arguments

The arguments depend on the hook used. They are separated by semicolons.

       Hook                         Arguments                                   Examples               Documentation (API)
                1. signal name (priority allowed) (required)       *,irc_in_privmsg
    signal      2. signal name (priority allowed)                  *,irc_in_privmsg;*,irc_in_notice    hook_signal
                3. …                                              signal_sigwinch

                1. signal name (priority allowed) (required)
    hsignal     2. signal name (priority allowed)                  nicklist_nick_added                 hook_hsignal
                3. …

                1. modifier name (priority allowed) (required)     weechat_print
    modifier    2. modifier name (priority allowed)                5000|input_text_display;5000|       hook_modifier
                3. …                                              history_add

                1. buffer name                                     irc.freenode.*
    print       2. tags                                            irc.freenode.#weechat               hook_print
                3. message                                         irc.freenode.#weechat;irc_notice
                4. strip colors (0/1)                              *;;;1

                1. command name (priority allowed) (required)
                2. description                                     test
    command     3. arguments                                       5000|test                           hook_command
                4. description of arguments
                5. completion

                1. command (priority allowed) (required)
    command_run 2. command (priority allowed)                      /cmd arguments                      hook_command_run
                3. …

                1. interval in milliseconds (required)
    timer       2. alignment on second (default: 0)                3600000                             hook_timer
                3. max number of calls (default: 0, which means    60000;0;5
                "no end")

                1. option name (priority allowed) (required)
    config      2. option name (priority allowed)                  weechat.look.*                      hook_config
                3. …

                1. area name (priority allowed) (required)
    focus       2. area name (priority allowed)                    buffer_nicklist                     hook_focus
                3. …

# Conditions

The conditions are used to continue processing in trigger, or stop everything.

They are  evaluated, and  data available in  callback can be  used (see  data in
callbacks and command /eval).

Example: the  default beep trigger  uses this condition to  make a beep  only on
highlight or private message:

        ${tg_highlight} || ${tg_msg_pv}

# Regular expression

The regular expression is used to change variables in callback hashtable.

The format is: "/regex/replace" or "/regex/replace/var" (where var is a variable
of the hashtable).
If var is not specified, the default variable is used, it depends on hook type:

   Hook      Default variable

signal      tg_signal_data

hsignal

modifier    tg_string

print       tg_message

command     tg_argv_eol1

command_run tg_command

timer       tg_remaining_calls

config      tg_value

focus

Many  regular   expressions  can   be  separated  by   a  space,   for  example:
"/regex1/replace1/var1 /regex2/replace2/var2".

The char "/" can be replaced by any char (one or more identical chars).

Matching groups can be used in "replace":

  • ${re:0} to ${re:99}: ${re:0} is the whole match, ${re:1} to ${re:99} are groups captured

  • ${re:+}: the last match (with highest number)

  • ${hide:c,${re:N}}: match "N" with all chars replaced by "c" (example: ${hide:*,${re:2}} is the group #2 with all
    chars replaced by *).

Example: use bold for words between "*":

        /\*(\S+)\*/*${color:bold}${re:1}${color:-bold}*/

Example:  default  trigger server_pass  uses  this  regular expression  to  hide
password in  commands /server and /connect  (chars in passwords are  replaced by
\*):

        ==^(/(server|connect) .*-(sasl_)?password=)(\S+)(.*)==${re:1}${hide:*,${re:4}}${re:5}

In this example, the delimiter used is "==" because there is a "/" in the regular expression.

# Command

The command is executed after replacement of text with the regular expression.
Many commands can be separated by semicolons.

It is evaluated  (see `/eval`), and the text replaced  with a regular expression
can be used in the command.

Example: default beep trigger uses this command to make a beep (BEL):

        /print -beep

# Data in callbacks

Data received in callbacks are stored in hashtables (pointers and strings) and can be used in following options:

  • conditions

  • regex

  • command

The content of hashtables depend on the hook type.

A convenient way to see data in a trigger is to open trigger monitor buffer, using the command:

        /trigger monitor

Signal

The "signal" callback sets following variables in hashtable:

   Variable     Type         Description
tg_signal      string Name of signal

tg_signal_data string Data sent with the signal

If the signal contains an IRC message, the message is parsed and following data is added in hashtable:

      Variable        Type                                          Description
irc_server           pointer Pointer to IRC server (variables in hdata of type "irc_server" can be used, like $
                             {irc_server.name}).

irc_channel          pointer Pointer to IRC channel (variables in hdata of type "irc_channel" can be used, like $
                             {irc_channel.name}).

server               string  Name of server (example: "freenode").

tags                 string  Tags in message (rarely used).

message_without_tags string  Message without tags.

nick                 string  Nick.

host                 string  Hostname.

command              string  IRC command (example: "PRIVMSG", "NOTICE", …).

channel              string  IRC channel.

arguments            string  Arguments of command (includes value of channel).

text                 string  Text (for example user message).

pos_command          string  The index of command in message ("-1" if command was not found).

pos_arguments        string  The index of arguments in message ("-1" if arguments was not found).

pos_channel          string  The index of channel in message ("-1" if channel was not found).

pos_text             string  The index of text in message ("-1" if text was not found).

When the data is a pointer, the variable tg_signal_data can be used like this to read a hdata property (in this
example this is a pointer on a buffer):

${buffer[${tg_signal_data}].full_name}

Hsignal

The "hsignal" callback sets following variables in hashtable:

Variable   Type    Description
tg_signal string Name of signal

The hashtable contains all keys/values from hashtable received (type: string/string).

Modifier

The "modifier" callback sets following variables in hashtable:

    Variable       Type             Description
tg_modifier       string Name of modifier.

tg_modifier_data  string Data sent with modifier.

tg_string         string The string that can be modified.

tg_string_nocolor string The string without color codes.

For the weechat_print modifier, variables using message tags are added (see hook print below), and following
variables:

     Variable       Type                    Description
buffer             pointer Buffer where message is printed.

tg_plugin          string  Plugin of buffer where message is printed.

tg_buffer          string  Full name of buffer where message is printed.

tg_prefix          string  Prefix of message printed.

tg_prefix_nocolor  string  Prefix without color codes.

tg_message         string  Message printed.

tg_message_nocolor string  Message without color codes.

If the modifier contains an IRC message, the message is parsed and extra data is added in hashtable (see hook
signal).

Print

The "print" callback sets following variables in hashtable:

     Variable       Type                     Description
buffer             pointer Buffer.

tg_date            string  Message date/time (format: YYYY-MM-DD hh:mm:ss).

tg_displayed       string  "1" if displayed, "0" if line filtered.

tg_highlight       string  "1" if highlight, otherwise "0".

tg_prefix          string  Prefix.

tg_prefix_nocolor  string  Prefix without color codes.

tg_message         string  Message.

tg_message_nocolor string  Message without color codes.

Variables set using tags in message (they are set in modifier weechat_print too):

     Variable       Type                            Description
tg_tags            string Tags of message (with comma added at beginning/end of string).

tg_tags_count      string Number of tags in message.

tg_tag_nick        string Nick (from tag "nick_xxx").

tg_tag_prefix_nick string Color of nick in prefix (from tag "prefix_nick_ccc").

tg_tag_host        string User name and host, format: username@host (from tag "host_xxx").

tg_tag_notify      string Notify level (none, message, private, highlight).

tg_notify          string Notify level, if different from none.

tg_msg_pv          string "1" for a private message, otherwise "0".

Command

The "command" callback sets following variables in hashtable:

  Variable    Type                  Description
buffer       pointer Buffer.

tg_argvN     string  Argument #N.

tg_argv_eolN string  From argument #N until end of arguments.

Command_run

The "command_run" callback sets following variables in hashtable:

 Variable   Type      Description
buffer     pointer Buffer.

tg_command string  Command executed.

Timer

The "timer" callback sets following variables in hashtable:

     Variable       Type                    Description
tg_remaining_calls string Number of remaining calls.

tg_date            string Current date/time (format: YYYY-MM-DD hh:mm:ss).

Config

The "config" callback sets following variables in hashtable:

Variable   Type  Description
tg_option string Option.

tg_value  string Value.

Focus

The "focus" callback sets following variables in hashtable:

Variable  Type   Description
window   pointer Window.

buffer   pointer Buffer.

The hashtable contains all keys/values from hashtable received (type: string/string).

# Examples

Color for URLs

Display URLs in green:

/trigger add url_color modifier weechat_print "${tg_notify}" "==\S+://\S+==${color:green}${re:0}${color:reset}=="

 The simple regex used to detect URL may not catch well all URLs, but it is faster than a complex regex.

Auto pong on ping queries

When someone sends a "ping" in a private buffer, this trigger will auto-reply with pong:

/trigger add pong print "" "${type} == private && ${tg_message} == ping" "" "pong"

Responsive layout

Following triggers can be used to customize things displayed when the size of terminal is changed:

/trigger add resize_small signal signal_sigwinch "${info:term_width} < 100" "" "/bar hide nicklist"
/trigger add resize_big signal signal_sigwinch "${info:term_width} >= 100" "" "/bar show nicklist"

The triggers catch the signal "signal_sigwinch", which is sent by WeeChat when signal SIGWINCH is received (when
terminal size is changed).

The condition with ${info:term_width} checks the width of terminal (you can also use ${info:term_height} if needed).

In the example, when the terminal becomes small, the nicklist is hidden. And the bar is restored when the width is
greater or equal to 100 chars.

Automatic save of configuration

You can automatically save configuration files (\*.conf), for example each hour:

/trigger add cfgsave timer 3600000;0;0 "" "" "/mute /save"

Arguments for the timer hook are:

  • 3600000: 3600 * 1000 milliseconds, the callback is called each hour

  • 0: alignment on second (not aligned here)

  • 0: max number of calls (0 = no end for the timer)

The command /mute /save will silently save configuration files (nothing displayed on core buffer).

# Commands

  • trigger: manage triggers, the Swiss Army knife for WeeChat

/trigger  list|listfull|listdefault
          add|addoff|addreplace <name> <hook> ["<arguments>" ["<conditions>" ["<regex>" ["<command>" ["<return_code>" ["<post_action>"]]]]]]
          addinput [<hook>]
          input|output|recreate <name>
          set <name> <option> <value>
          rename|copy <name> <new_name>
          enable|disable|toggle [<name>|-all [<name>...]]
          restart <name>|-all [<name>...]
          show <name>
          del <name>|-all [<name>...]
          restore <name> [<name>...]
          default -yes
          monitor [<filter>]

       list: list triggers (without argument, this list is displayed)
   listfull: list triggers with detailed info for each trigger
listdefault: list default triggers
        add: add a trigger
     addoff: add a trigger (disabled)
 addreplace: add or replace an existing trigger
       name: name of trigger
       hook: signal, hsignal, modifier, print, command, command_run, timer, config, focus
  arguments: arguments for the hook, depending on hook (separated by semicolons):
             signal: name(s) of signal (required)
             hsignal: name(s) of hsignal (required)
             modifier: name(s) of modifier (required)
             print: buffer, tags, message, strip colors
             command: command (required), description, arguments, description of arguments, completion
             command_run: command(s) (required)
             timer: interval (required), align on second, max calls
             config: name(s) of option (required)
             focus: name(s) of area (required)
 conditions: evaluated conditions for the trigger
      regex: one or more regular expressions to replace strings in variables
    command: command to execute (many commands can be separated by ";")
return_code: return code in callback (ok (default), ok_eat, error)
post_action: action to take after execution (none (default), disable, delete)
   addinput: set input with default arguments to create a trigger
      input: set input with the command used to create the trigger
     output: send the command to create the trigger on the buffer
   recreate: same as "input", with option "addreplace" instead of "add"
        set: set an option in a trigger
     option: name of option: name, hook, arguments, conditions, regex, command, return_code
             (for help on option, you can type: /help trigger.trigger.<name>.<option>)
      value: new value for the option
     rename: rename a trigger
       copy: copy a trigger
     enable: enable trigger(s) (without arguments: enable triggers globally)
    disable: disable trigger(s) (without arguments: disable triggers globally)
     toggle: toggle trigger(s) (without arguments: toggle triggers globally)
    restart: restart trigger(s) (recreate the hooks)
       show: show detailed info on a trigger (with some stats)
        del: delete a trigger
       -all: do action on all triggers
    restore: restore trigger(s) with the default values (works only for default triggers)
    default: delete all triggers and restore default ones
    monitor: open the trigger monitor buffer, with optional filter:
     filter: filter hooks/triggers to display (a hook must start with "@", for example "@signal"), many filters can be separated by commas; wildcard "*" is allowed in each trigger name

When a trigger callback is called, following actions are performed, in this order:
  1. check conditions; if false, exit
  2. replace text using POSIX extended regular expression(s) (if defined in trigger)
  3. execute command(s) (if defined in trigger)
  4. exit with a return code (except for modifiers and focus)
  5. perform post action

Examples (you can also look at default triggers with /trigger listdefault):
  add text attributes *bold*, _underline_ and /italic/ (only in user messages):
    /trigger add effects modifier weechat_print "${tg_tag_nick}" "==\*(\S+)\*==*${color:bold}${re:1}${color:-bold}*== ==_(\S+)_==_${color:underline}${re:1}${color:-underline}_== ==/(\S+)/==/${color:italic}${re:1}${color:-italic}/"
  hide nicklist bar on small terminals:
    /trigger add resize_small signal signal_sigwinch "${info:term_width} < 100" "" "/bar hide nicklist"
    /trigger add resize_big signal signal_sigwinch "${info:term_width} >= 100" "" "/bar show nicklist"
  silently save config each hour:
    /trigger add cfgsave timer 3600000;0;0 "" "" "/mute /save"
  open trigger monitor and show only modifiers and triggers whose name starts with "resize":
    /trigger monitor @modifier,resize*

# Options

Sections in file trigger.conf:

Section     Control command       Description
look    /set trigger.look.*     Look and feel.

color   /set trigger.color.*    Colors.

        /trigger add
trigger /trigger set       Trigger options.
        /set trigger.trigger.*

Options:

  • trigger.color.flag_command

      □ description: text color for command flag (in /trigger list)

      □ type: color

      □ values: a WeeChat color name (default, black, (dark)gray, white, (light)red, (light)green, brown, yellow,
        (light)blue, (light)magenta, (light)cyan), a terminal color number or an alias; attributes are allowed before
        color (for text color only, not background): "*" for bold, "!" for reverse, "/" for italic, "_" for underline

      □ default value: lightgreen

  • trigger.color.flag_conditions

      □ description: text color for conditions flag (in /trigger list)

      □ type: color

      □ values: a WeeChat color name (default, black, (dark)gray, white, (light)red, (light)green, brown, yellow,
        (light)blue, (light)magenta, (light)cyan), a terminal color number or an alias; attributes are allowed before
        color (for text color only, not background): "*" for bold, "!" for reverse, "/" for italic, "_" for underline

      □ default value: yellow

  • trigger.color.flag_post_action

      □ description: text color for post action flag (in /trigger list)

      □ type: color

      □ values: a WeeChat color name (default, black, (dark)gray, white, (light)red, (light)green, brown, yellow,
        (light)blue, (light)magenta, (light)cyan), a terminal color number or an alias; attributes are allowed before
        color (for text color only, not background): "*" for bold, "!" for reverse, "/" for italic, "_" for underline

      □ default value: lightblue

  • trigger.color.flag_regex

      □ description: text color for regex flag (in /trigger list)

      □ type: color

      □ values: a WeeChat color name (default, black, (dark)gray, white, (light)red, (light)green, brown, yellow,
        (light)blue, (light)magenta, (light)cyan), a terminal color number or an alias; attributes are allowed before
        color (for text color only, not background): "*" for bold, "!" for reverse, "/" for italic, "_" for underline

      □ default value: lightcyan

  • trigger.color.flag_return_code

      □ description: text color for return code flag (in /trigger list)

      □ type: color

      □ values: a WeeChat color name (default, black, (dark)gray, white, (light)red, (light)green, brown, yellow,
        (light)blue, (light)magenta, (light)cyan), a terminal color number or an alias; attributes are allowed before
        color (for text color only, not background): "*" for bold, "!" for reverse, "/" for italic, "_" for underline

      □ default value: lightmagenta

  • trigger.color.regex

      □ description: text color for regular expressions

      □ type: color

      □ values: a WeeChat color name (default, black, (dark)gray, white, (light)red, (light)green, brown, yellow,
        (light)blue, (light)magenta, (light)cyan), a terminal color number or an alias; attributes are allowed before
        color (for text color only, not background): "*" for bold, "!" for reverse, "/" for italic, "_" for underline

      □ default value: white

  • trigger.color.replace

      □ description: text color for replacement text (for regular expressions)

      □ type: color

      □ values: a WeeChat color name (default, black, (dark)gray, white, (light)red, (light)green, brown, yellow,
        (light)blue, (light)magenta, (light)cyan), a terminal color number or an alias; attributes are allowed before
        color (for text color only, not background): "*" for bold, "!" for reverse, "/" for italic, "_" for underline

      □ default value: cyan

  • trigger.color.trigger

      □ description: text color for trigger name

      □ type: color

      □ values: a WeeChat color name (default, black, (dark)gray, white, (light)red, (light)green, brown, yellow,
        (light)blue, (light)magenta, (light)cyan), a terminal color number or an alias; attributes are allowed before
        color (for text color only, not background): "*" for bold, "!" for reverse, "/" for italic, "_" for underline

      □ default value: green

  • trigger.color.trigger_disabled

      □ description: text color for disabled trigger name

      □ type: color

      □ values: a WeeChat color name (default, black, (dark)gray, white, (light)red, (light)green, brown, yellow,
        (light)blue, (light)magenta, (light)cyan), a terminal color number or an alias; attributes are allowed before
        color (for text color only, not background): "*" for bold, "!" for reverse, "/" for italic, "_" for underline

      □ default value: red

  • trigger.look.enabled

      □ description: enable trigger support

      □ type: boolean

      □ values: on, off

      □ default value: on

  • trigger.look.monitor_strip_colors

      □ description: strip colors in hashtable values displayed on monitor buffer

      □ type: boolean

      □ values: on, off

      □ default value: off


##
##
##
# How to delete a trigger?

        /trigger del my_trigger

