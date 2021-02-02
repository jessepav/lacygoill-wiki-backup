# finish PR to add completion for ":filetype" and ":set ft="

See: <https://github.com/vim/vim/pull/7747>

First, let's try to understand how Vim implements the completion for `:profile`.
To do that, let's find all relevant code.

Everything starts in this block in `src/cmdexpand.c`:

    case CMD_profile:
        set_context_in_profile_cmd(xp, arg);
        break;

We now need to explain what `CMD_profile` means, as well as `set_context_in_profile_cmd()`.
If any of those  objects refer to something we don't understand,  it needs to be
explained too.

## `CMD_profile`

Element (?) in the enumerated type `CMD_index` declared in `src/ex_cmds.h`:

    EXCMD(CMD_profile,	"profile",	ex_profile,
            EX_BANG|EX_EXTRA|EX_TRLBAR|EX_CMDWIN|EX_LOCK_OK,
            ADDR_NONE),

Referenced in `src/cmdexpand.c`, function `set_one_cmd_context()`:

    exarg_T		ea;
    ...
    // 6. Switch on command name.
    switch (ea.cmdidx)
    {
        ...
        case CMD_profile:

Note: `ex_filetype` is already implemented in `src/ex_docmd.c`.

---

It's also referenced twice in `src/debugger.c`.
But  I  think  those  are   irrelevant.   `CMD_filetype`  is  already  correctly
referenced in `src/ex_cmds.h`:

    EXCMD(CMD_filetype, "filetype",     ex_filetype,

### `ea`

Variable declared in `src/cmdexpand.c`, function `set_one_cmd_context()` (at the top):

    exarg_T		ea;

### `ea.cmdidx`

Element `cmdidx` of structure the structure tag `ea`.

Inside the  structure tag `ea`, the  element `cmdidx` is declared  with the type
`cmdidx_T`:

    cmdidx_T	cmdidx;		// the index for the command

##
## `CMD_index`

Enumerated type declared in `src/ex_cmds.h`:

    enum CMD_index
    {
    EXCMD(CMD_append,	"append",	ex_append,
            EX_BANG|EX_RANGE|EX_ZEROR|EX_TRLBAR|EX_CMDWIN|EX_LOCK_OK|EX_MODIFY,
            ADDR_LINES),
    EXCMD(CMD_abbreviate,	"abbreviate",	ex_abbreviate,
            EX_EXTRA|EX_TRLBAR|EX_NOTRLCOM|EX_CTRLV|EX_CMDWIN|EX_LOCK_OK,
            ADDR_NONE),
    EXCMD(CMD_abclear,	"abclear",	ex_abclear,
            EX_EXTRA|EX_TRLBAR|EX_CMDWIN|EX_LOCK_OK,
            ADDR_NONE),

##
## `set_context_in_profile_cmd()`

Function declared in `src/proto/profiler.pro`:

    void set_context_in_profile_cmd(expand_T *xp, char_u *arg);

Defined in `src/profiler.c`:

    /*
     * Handle command line completion for :profile command.
     */
        void
    set_context_in_profile_cmd(expand_T *xp, char_u *arg)
    {
        char_u	*end_subcmd;

        // Default: expand subcommands.
        xp->xp_context = EXPAND_PROFILE;
        pexpand_what = PEXP_SUBCMD;
        xp->xp_pattern = arg;

        end_subcmd = skiptowhite(arg);
        if (*end_subcmd == NUL)
            return;

        if (end_subcmd - arg == 5 && STRNCMP(arg, "start", 5) == 0)
        {
            xp->xp_context = EXPAND_FILES;
            xp->xp_pattern = skipwhite(end_subcmd);
            return;
        }

        // TODO: expand function names after "func"
        xp->xp_context = EXPAND_NOTHING;
    }

It's called  in `src/cmdexpand.c`, function `set_one_cmd_context()`  (whose body
is  told to  be mostly  copied  from `do_one_cmd()`  in `src/ex_docmd.c`,  which
itself is in charge of executing 1 Ex command):

    set_context_in_profile_cmd(xp, arg);

### `EXPAND_PROFILE`

It's an integer (35) which stands for the expansion of `:profile`.

Declared in `src/vim.h`:

    #define EXPAND_PROFILE		35

Referenced in `src/cmdexpand.c`, function `ExpandFromContext()`:

    {EXPAND_PROFILE, get_profile_name, TRUE, TRUE},

And in `src/profiler.c`, function `set_context_in_profile_cmd()`:

    xp->xp_context = EXPAND_PROFILE;

#### `get_profile_name()`

Function declared in `src/proto/profiler.pro`:

    char_u *get_profile_name(expand_T *xp, int idx);

Defined in `src/profiler.c`:

    /*
     * Function given to ExpandGeneric() to obtain the profile command
     * specific expansion.
     */
        char_u *
    get_profile_name(expand_T *xp UNUSED, int idx)
    {
        switch (pexpand_what)
        {
        case PEXP_SUBCMD:
            return (char_u *)pexpand_cmds[idx];
        default:
            return NULL;
        }
    }

Referenced in `src/cmdexpand.c`, inside the function `ExpandFromContext()`:

    {EXPAND_PROFILE, get_profile_name, TRUE, TRUE},

##### `pexpand_what`

Enumeration declared in `src/profiler.c`:

    // Command line expansion for :profile.
    static enum
    {
        PEXP_SUBCMD,	// expand :profile sub-commands
        PEXP_FUNC		// expand :profile func {funcname}
    } pexpand_what;

Referenced in `src/profiler.c`, function `get_profile_name()`:

    switch (pexpand_what)

And in `src/profiler.c`, function `set_context_in_profile_cmd()`:

    pexpand_what = PEXP_SUBCMD;

##### `pexpand_cmds`

In `src/profiler.c`:

    static char *pexpand_cmds[] = {
                            "start",
    #define PROFCMD_START	0
                            "pause",
    #define PROFCMD_PAUSE	1
                            "continue",
    #define PROFCMD_CONTINUE 2
                            "func",
    #define PROFCMD_FUNC	3
                            "file",
    #define PROFCMD_FILE	4
                            NULL
    #define PROFCMD_LAST	5
    };

In `src/profiler.c`, function `get_profile_name()`:

    return (char_u *)pexpand_cmds[idx];

###
### `PEXP_SUBCMD`

Enumeration constant inside the enumeration `pexpand_what`, in `src/profiler.c`:

    PEXP_SUBCMD,	// expand :profile sub-commands

Referenced in `src/profiler.c`, function `get_profile_name()`:

    case PEXP_SUBCMD:

And in `src/profiler.c`, function `set_context_in_profile_cmd()`:

    pexpand_what = PEXP_SUBCMD;

##
## Syntax
### What are these concepts?
#### structure

A data  type which can contain  several elements of different  types; the latter
can be  accessed by  their names  (using either  the dot  notation or  the arrow
notation; the former being more efficient).

#### enumeration

A data type for a specified list of possible values.

Each of these values is called an "enumeration constant".

Example:
```c
enum {CLUBS, DIAMONDS, HEARTS, SPADES} s1, s2;
```
This declares  2 variables  `s1` and  `s2`, with an  enumerated type  whose only
valid values are:

   - CLUBS
   - DIAMONDS
   - HEARTS
   - SPADES

###
### This snippet causes the compiler to give an error:
```c
struct foo { ... };
foo var;
```
#### Why?

`foo` is a tag.  A tag is  meaningful only when it's immediately preceded by the
`struct`  keyword, because  tags  and  other identifiers  are  in distinct  name
spaces.

As a result, the compiler can't find `foo` in the ordinary identifier name space.

#### How to fix the code?

Either use the  `struct` keyword to tell the compiler  that the `foo` identifier
should be looked up in the tag name space:
```c
struct foo { ... };
struct foo var;
```
Or declare a type alias with `typedef`:
```c
typedef struct foo { ... } bar;
bar var;
```
This works because type aliases are looked up in the ordinary identifier name space.

You can also use the same identifier for the tag and for the type alias:
```c
typedef struct foo { ... } foo;
foo var;
```
And you can omit the tag:
```c
typedef struct { ... } foo;
foo var;
```
###
### What do these keywords/identifiers mean?
#### `void`

Before a function name, it stands for the void return type.
It means that the function does not return a value.

####
#### `cmdidx_T`

A type alias which can replace the enumerated type `CMD_index`.

It's declared in `src/ex_cmds.h`:

    typedef enum CMD_index cmdidx_T;

#### `exarg_T`

A type alias  which can be used to  replace the tag `exarg` (which  itself is an
identifier for a struct type).

`exarg_T` and `exarg` are both declared in `src/ex_cmds.h`.
`exarg` contains various info about the arguments of an arbitrary Ex command.

#### `expand_T`

A type alias which  can be used to replace the tag `expand`  (which itself is an
identifier for a struct type).

It's declared in `src/structs.h`:

    /*
     * used for completion on the command line
     */
    typedef struct expand
    {
        char_u	*xp_pattern;		// start of item to expand
        int		xp_context;		// type of expansion
        int		xp_pattern_len;		// bytes in xp_pattern before cursor
    #if defined(FEAT_EVAL)
        char_u	*xp_arg;		// completion function
        sctx_T	xp_script_ctx;		// SCTX for completion function
    #endif
        int		xp_backslash;		// one of the XP_BS_ values
    #ifndef BACKSLASH_IN_FILENAME
        int		xp_shell;		// TRUE for a shell command, more
                                            // characters need to be escaped
    #endif
        int		xp_numfiles;		// number of files found by
                                            // file name completion
        int		xp_col;			// cursor position in line
        char_u	**xp_files;		// list of files
        char_u	*xp_line;		// text being completed
    } expand_T;

The whole statement is a common C idiom which combines 2 declarations:

   - `struct expand {...}` declares a structure tag, named `expand`

   - `typedef struct expand  {...} expand_T` declares a type alias, named
     `expand_T`,  which can be used to replace that structure tag

#### `sctx_T`

A type alias which can be used to replace a specific struct type.

It's declared in `src/structs.h`:

    /*
     * SCript ConteXt (SCTX): identifies a script line.
     * When sourcing a script "sc_lnum" is zero, "sourcing_lnum" is the current
     * line number. When executing a user function "sc_lnum" is the line where the
     * function was defined, "sourcing_lnum" is the line number inside the
     * function.  When stored with a function, mapping, option, etc. "sc_lnum" is
     * the line number in the script "sc_sid".
     *
     * sc_version is also here, for convenience.
     */
    typedef struct {
    #ifdef FEAT_EVAL
        scid_T	sc_sid;		// script ID
        int		sc_seq;		// sourcing sequence number
        linenr_T	sc_lnum;	// line number
    #endif
        int		sc_version;	// :scriptversion
    } sctx_T;

#### `linenr_T`

A type alias declared in `src/structs.h`:

    typedef long		linenr_T;

`long` is a signed integer type.

#### `scid_T`

A type alias declared in `src/structs.h`:

    typedef int			scid_T;		// script ID

####
#### `char`

A reserved keyword which describes a data type that holds one character of data.
For example, the value of a  `char` variable could be any one-character value, such as:

   - 'A'
   - '4'
   - '#'

#### `unsigned char`

`signed char` is an 8-bit two's complement  number ranging from -128 to 127, and
`unsigned char` is an 8-bit unsigned integer (0 to 255).

#### `char_u`

A type alias which can be used to replace `unsigned char`.

It's declared in `src/vim.h`:

    /*
     * Shorthand for unsigned variables. Many systems, but not all, have u_char
     * already defined, so we use char_u to avoid trouble.
     */
    typedef unsigned char	char_u;
    typedef unsigned short	short_u;
    typedef unsigned int	int_u;

####
#### `static`

#### `struct`

A keyword to declare a structure variable:
```c
struct {
    int number;
    char name[NAME_LEN+1];
    int on_hand;
} part1;
```
or a structure tag:
```c
struct part {
    int number;
    char name[NAME_LEN+1];
    int on_hand;
};
```
In the first snippet, `part1` is a variable name.
In the last snippet, `part` is a tag which can be used to declare variables:
```c
struct part part1, part2
```
#### `tag`

An identifier for a struct type, union type, or enum type.

The term  comes from the  fact that the  identifier can be  used to look  up one
specific type among many, a bit like a tag name.

#### `typedef`

A keyword which lets you declare that an  identifier can be used as an alias for
an *existing* type.  It does **not** let you create *new* types.

It's useful to replace a possibly complex type name.

##
# Patch

Needs more work.

First, if we've just completed `plugin`,  the next completion should not suggest
`plugin` again.  Same thing with `indent`.

Second, we can only complete up to 2 arguments; we should be able to complete up
to 3 arguments.

Third,  the suggestions  should never  include  sth which  generates an  invalid
command.  For  example, after  `:filetype plugin  indent`, and  `filetype indent
plugin` only `on` and `off` should be suggested.
```diff
diff --git a/src/cmdexpand.c b/src/cmdexpand.c
index d51f5c642..ad162a235 100644
--- a/src/cmdexpand.c
+++ b/src/cmdexpand.c
@@ -1747,6 +1747,10 @@ set_one_cmd_context(
 	    set_context_in_profile_cmd(xp, arg);
 	    break;
 #endif
+	case CMD_filetype:
+	    set_context_in_filetype_cmd(xp, arg);
+	    break;
+
 	case CMD_behave:
 	    xp->xp_context = EXPAND_BEHAVE;
 	    xp->xp_pattern = arg;
@@ -2141,6 +2145,7 @@ ExpandFromContext(
 # ifdef FEAT_PROFILE
 	    {EXPAND_PROFILE, get_profile_name, TRUE, TRUE},
 # endif
+	    {EXPAND_FILETYPECMD, get_filetype_arg, TRUE, TRUE},
 # if defined(HAVE_LOCALE_H) || defined(X_LOCALE)
 	    {EXPAND_LANGUAGE, get_lang_arg, TRUE, FALSE},
 	    {EXPAND_LOCALES, get_locales, TRUE, FALSE},
diff --git a/src/ex_docmd.c b/src/ex_docmd.c
index 8b9db6812..920a39f4b 100644
--- a/src/ex_docmd.c
+++ b/src/ex_docmd.c
@@ -9089,6 +9089,69 @@ ex_filetype(exarg_T *eap)
 	semsg(_(e_invarg2), arg);
 }
 
+// Command line expansion for :filetype.
+static enum
+{
+    FEXP_SUBCMD,	// expand :filetype sub-commands
+} fexpand_what;
+
+static char *fexpand_cmds[] = {
+                        "on",
+#define FILETYPECMD_ON		0
+                        "off",
+#define FILETYPECMD_OFF		1
+                        "plugin",
+#define FILETYPECMD_PLUGIN	2
+                        "indent",
+#define FILETYPECMD_INDENT	3
+                        NULL
+#define FILETYPECMD_LAST	4
+};
+
+/*
+ * Function given to ExpandGeneric() to obtain the filetype command
+ * specific expansion.
+ */
+    char_u *
+get_filetype_arg(expand_T *xp UNUSED, int idx)
+{
+    switch (fexpand_what)
+    {
+    case FEXP_SUBCMD:
+        return (char_u *)fexpand_cmds[idx];
+    default:
+        return NULL;
+    }
+}
+
+/*
+ * Handle command line completion for :filetype command.
+ */
+    void
+set_context_in_filetype_cmd(expand_T *xp, char_u *arg)
+{
+    char_u	*end_subcmd;
+
+    // Default: expand subcommands.
+    xp->xp_context = EXPAND_FILETYPECMD;
+    fexpand_what = FEXP_SUBCMD;
+    xp->xp_pattern = arg;
+
+    end_subcmd = skiptowhite(arg);
+    if (*end_subcmd == NUL)
+        return;
+
+    if (end_subcmd - arg == 6 && (STRNCMP(arg, "indent", 6) == 0
+                               || STRNCMP(arg, "plugin", 6) == 0))
+    {
+        xp->xp_context = EXPAND_FILETYPECMD;
+        xp->xp_pattern = skipwhite(end_subcmd);
+        return;
+    }
+
+    xp->xp_context = EXPAND_NOTHING;
+}
+
 /*
  * ":setfiletype [FALLBACK] {name}"
  */
diff --git a/src/option.c b/src/option.c
index b4893a10a..7a79d2e97 100644
--- a/src/option.c
+++ b/src/option.c
@@ -6209,6 +6209,12 @@ set_context_in_set_cmd(
 	    else
 		xp->xp_backslash = XP_BS_ONE;
 	}
+	else if (p == (char_u *)&p_ft) {
+	    xp->xp_context = EXPAND_FILETYPE;
+	}
+	else if (p == (char_u *)&p_ft) {
+	    xp->xp_context = EXPAND_FILETYPE;
+	}
 	else
 	{
 	    xp->xp_context = EXPAND_FILES;
diff --git a/src/optiondefs.h b/src/optiondefs.h
index 6cea0177c..9961bd477 100644
--- a/src/optiondefs.h
+++ b/src/optiondefs.h
@@ -946,7 +946,7 @@ static struct vimoption options[] =
 				    (char_u *)FALSE,
 #endif
 					(char_u *)0L} SCTX_INIT},
-    {"filetype",    "ft",   P_STRING|P_ALLOCED|P_VI_DEF|P_NOGLOB|P_NFNAME,
+    {"filetype",    "ft",   P_STRING|P_EXPAND|P_ALLOCED|P_VI_DEF|P_NOGLOB|P_NFNAME,
 			    (char_u *)&p_ft, PV_FT,
 			    {(char_u *)"", (char_u *)0L}
 			    SCTX_INIT},
diff --git a/src/proto/ex_cmds.pro b/src/proto/ex_cmds.pro
index 9036dd205..956b58d31 100644
--- a/src/proto/ex_cmds.pro
+++ b/src/proto/ex_cmds.pro
@@ -39,4 +39,5 @@ void ex_smile(exarg_T *eap);
 void ex_drop(exarg_T *eap);
 char_u *skip_vimgrep_pat(char_u *p, char_u **s, int *flags);
 void ex_oldfiles(exarg_T *eap);
+void set_context_in_filetype_cmd(expand_T *xp, char_u *arg);
 /* vim: set ft=c : */
diff --git a/src/proto/ex_docmd.pro b/src/proto/ex_docmd.pro
index 94770f2e3..d55de7052 100644
--- a/src/proto/ex_docmd.pro
+++ b/src/proto/ex_docmd.pro
@@ -61,4 +61,5 @@ void set_no_hlsearch(int flag);
 int is_loclist_cmd(int cmdidx);
 int get_pressedreturn(void);
 void set_pressedreturn(int val);
+char_u *get_filetype_arg(expand_T *xp, int idx);
 /* vim: set ft=c : */
diff --git a/src/testdir/test_options.vim b/src/testdir/test_options.vim
index c8b2700dd..19c62cc7b 100644
--- a/src/testdir/test_options.vim
+++ b/src/testdir/test_options.vim
@@ -332,6 +332,14 @@ func Test_set_completion()
   call feedkeys(":set key=\<Tab>\<C-B>\"\<CR>", 'xt')
   call assert_equal('"set key=*****', @:)
   set key=
+
+  " Expand filetypes for 'filetype'
+  call feedkeys(":set filetype=a\<C-A>\<C-B>\"\<CR>", 'xt')
+  call assert_equal('"set filetype=' .. getcompletion('a*', 'filetype')->join(), @:)
+
+  " Expand :filetype arguments
+  call feedkeys(":filetype \<C-A>\<C-B>\"\<CR>", 'xt')
+  call assert_equal('"filetype indent off on plugin', @:)
 endfunc
 
 func Test_set_errors()
diff --git a/src/vim.h b/src/vim.h
index de2482e8b..2d147af27 100644
--- a/src/vim.h
+++ b/src/vim.h
@@ -777,6 +777,7 @@ extern int (*dyn_libintl_wputenv)(const wchar_t *envstring);
 #define EXPAND_MAPCLEAR		47
 #define EXPAND_ARGLIST		48
 #define EXPAND_DIFF_BUFFERS	49
+#define EXPAND_FILETYPECMD	50
 
 // Values for exmode_active (0 is no exmode)
 #define EXMODE_NORMAL		1
```
