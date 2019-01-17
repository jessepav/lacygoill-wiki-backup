
    https://github.com/vermiculus/sx.el/

            SX – Stack Exchange for Emacs


    http://beatofthegeek.com/2014/02/my-setup-for-using-emacs-as-web-browser.html


    https://github.com/politza/pdf-tools

            https://www.reddit.com/r/emacs/comments/4srze9/watching_youtube_inside_emacs_25/d5btkdp/


    https://www.reddit.com/r/emacs/comments/4gudyw/help_me_with_my_orgmode_workflow_for_notetaking/

    https://emacs.stackexchange.com/questions/28429/how-do-i-troubleshoot-emacs-problems

    https://github.com/caiorss/Emacs-Elisp-Programming
    http://blog.aaronbieber.com/archive.html
    https://tuhdo.github.io/
    https://steve-yegge.blogspot.fr/2008/01/emergency-elisp.html
    https://www.youtube.com/user/howardabrams/videos
    https://www.gnu.org/software/emacs/manual/html_mono/eintr.html
    https://emacs.stackexchange.com/questions/20001/is-it-possible-to-read-user-input-from-stdin-while-tangling-a-source-block
    http://www.lunaryorn.com/2015/01/06/my-emacs-configuration-with-use-package.html
    org-mode
    https://sriramkswamy.github.io/dotemacs/
    http://doc.norang.ca/org-mode.html
    https://learnxinyminutes.com/docs/elisp/
    http://emacs-doctor.com/learn-emacs-lisp-in-15-minutes.html
    http://harryrschwartz.com/2014/04/08/an-introduction-to-emacs-lisp.html
    https://yoo2080.wordpress.com/2014/07/04/it-is-not-hard-to-read-lisp-code/
    https://yoo2080.wordpress.com/2014/07/20/it-is-not-hard-to-edit-lisp-code/
    https://web.archive.org/web/20140912224825/http://cjohansen.no/an-introduction-to-elisp
    http://ergoemacs.org/emacs/elisp.html

babel
use-package

# INSTALLATION

    sudo add-apt-repository ppa:ubuntu-elisp/ppa
    sudo aptitude install emacs-snapshot

# Tutorial
## Terminologie / Théorie

    delete  = supprimer sans possibilité de réinsérer
    kill    = supprimer avec possibilité de réinsérer
    yanking = réinsertion d'un texte killed

Les commandes qui suppriment peu de texte (un caractère, des espaces, lignes vides) delete.
Les commandes qui suppriment bcp de texte kill.

Contrairement à un yanking, une suppression de texte peut être défaite que la suppression soit
un delete ou un kill:
C-/, C-underscore, C-x u sont insensibles à la distinction entre kill et delete

Qd on répète successivement la commande C-k, les différents textes tués sont concaténés.
On peut donc les coller via un simple C-y.

Le minibuffer est le nom de la ligne en bas de l'écran où s'affiche le nom du fichier qu'on édite.
Le minibuffer permet de taper un input pour des commandes qui en attendent un.

## Raccourcis

    C-h t      tuto

    C-x C-c    quitter la session

    C-g        quitter une commande partiellement tapée ou en cours d'exécution
               parce qu'elle prend trop de temps


    C-l        nettoyer l'écran et redessiner le texte
               si on répète le raccourci, la ligne courante est affichée alternativement
               au milieu / en haut / en bas de l'écran
               C-l = zz, zt, zb

    C-v M-v    avancer / reculer d'une page
    C-n C-p    " d'une ligne
    M-a M-e    " d'une phrase
    M-< M->    se rendre au début / à la fin du buffer

    C-u 8 C-n  avancer de 8 lignes

               cette commande illustre le fait que C-u n permet de passer un argument / préfixe numérique
               à n'importe quelle commande pour la répéter plusieurs fois

               Exception: C-u n C-v / M-v ne bouge pas le curseur de n pages mais de n lignes

    C-x 1      fermer toutes les fenêtres sauf celle qui a le focus

    C-h k {key}

               ouvre une fenêtre affichant l'aide à propos du raccourci {key} ; ex: C-h k C-f

    <del> C-d  supprimer le caractère avant / après le curseur ; <del> = backspace (et non delete!)

    M-<del> M-d

               supprimer depuis le curseur jusqu'au début de mot précédent / suivant

    C-k M-k    supprimer du curseur jusqu'à la fin de la ligne / phrase

    C-u 8 *    insérer 8 caractères *

    C-<SPC> {motion} C-w

               supprimer un segment de texte arbitraire

    C-a C-u 2 C-k

               supprimer la ligne courante et la ligne qui suit
               qd on passe un argument numérique (ici 2) à la commande C-k, celle-ci change de comportement
               en temps normal il faut 2 C-k pour supprimer une ligne (un pour le contenu, un autre
               pour la ligne \n)

    C-y        coller le dernier texte killed (on parle de yanking)

    C-y M-y    coller l'avant dernier texte killed

    C-y C-u 4 M-y

               coller le 5e dernier texte killed

    C-u -1 M-y
               après avoir collé du texte via C-y, cette commande permet d'avancer dans l'historique
               des textes tués plutôt que de reculer via M-y

    C-/    C-_    C-x u

               défaire les changements de la dernière commande

    C-x C-f    chercher un fichier ou un buffer ouvert; la commande attend un argument qu'elle va lire
               cette commande permet aussi de créer un nouveau fichier

    C-x C-s    sauvegarder le buffer dans son fichier

    C-x C-b    afficher la buffer list

    C-x b foo  afficher le buffer foo présent dans la buffer list

    C-x s      sauvegarder tous les buffers contenant des changements non sauvegardés (via un prompt
               pour chacun)

# An Emacs Tutorial: Beginner's Guide to Emacs

By Mickey Petersen

The point is the  caret, or cursor, in other editors and in  most operating systems. Don’t confuse
it with the mouse cursor though.

Modes are  Emacs’ way of  switching between key  bindings, functionality, syntax  highlighting and
pretty much any other mutable item in Emacs.  Modes are always buffer-specific, and they come in two
flavors: major modes and minor modes.

In Emacs a buffer can only have one major mode, but any number of minor modes.

Minor modes  are similar to major  modes in that,  when enabled in  a buffer, provide a  variety of.
changes  and customizations  You tend  to have  lots of  minor modes  running in  a buffer  without.
necessarily noticing it  To get a complete list  of all modes running and all  the keybindings they.
introduce, type C-h m                                                                              .

The .emacs  file is the place  where all your emacs  customizations are typically kept.  The .emacs.
Thfile is also  called the init file  is file is different from  your custom file as  that is where.
Thyour Customization settings are stored - but more on Customize later                             .

When Emacs is starting it will look for the init file in ~/.emacs, ~/.emacs.el or ~/.emacs.d/init.el.

If you have  many distinct pieces of code you  can select them and type M-x  eval-region to evaluate
the region; you can also type M-x eval-buffer to re-evaluate the entire buffer.

To evaluate one piece of code individually you’re  better off just putting your point somewhere in
the expression and typing C-M-x.

Emacs has many, many settings, switches and toggles.

But changing settings  in Emacs has always remained  a tricky subject to teach  newbies, whether you
know Lisp  or not.  The big problem  stems from the  inconsistent way  that settings are  stored and
retrieved; some aren’t settings at all but functions that you toggle on or off (like tool-bar-mode
or menu-bar-mode for instance) and others take elisp functions that you have to write first.

Some settings are local to each buffer; others still are global, and some are re-set per “invocation”.

Where you  put the commands  to override settings  will in turn depend  on the specific  package and
functionality. I’ve tried to list some of the more obvious groupings here:

    Global; fire and forget.
    Local to a mode, so it should be set in that mode’s hook.
    Local to a buffer, so its default value should be overriden (for global changes) or when that buffer is created or initialised (for local changes)
    File local (settings are stored in a file, typically in a source code file’s header)
    Directory local (settings are stored in a special file and are read when files in that directory or any sub directory are opened)
    Files specific to a package or module, like Abbrevs and Yasnippet.
    “Customize” settings, more on those below.

To make matters worse, there’s another way of changing settings in Emacs: the Customize Menu.

The Customize Menu was introduced a long time ago as a way of standardizing and centralizing user settings. Chances are, if you’ve ever changed your syntax highlighter settings you’ve probably used it.

You can invoke it by typing M-x customize. Try it; browse around and go ahead and change things – Emacs is meant to be customized!

Your settings are saved to a file dictated by the variable custom-file (to read its value type C-h v custom-file) and are read once when Emacs starts up.

It is my personal recommendation that any changes that you can make through Customize are done so. Unless you really know your way around Emacs and possibly elisp it is by far the simplest and most user friendly way of doing it.

However, because I often reference changes directly I will suggest the more direct, brute, approach to changing things; this way is not necessarily better or worse, but it is easier to convey on a blog as the format the Customize menu uses is not conducive to “copying and pasting”.

I will ensure that whatever customizations or changes I mention here are, with few exceptions, “plug and play” – just drop them in the file I tell you to and you’re ready to rock.
What Emacs Version should I use?

You should be running GNU Emacs. There are other Emacsen out there, but GNU Emacs is the one I will concern myself with, as that is what I and the vast majority of Emacs users use.

The only other “competitor” to Emacs is XEmacs, a competing project that forked from Emacs back in the 90s and for a long time had GNU Emacs playing catch-up. Now, though, the roles have reversed: GNU Emacs is far more advanced, far stabler and has a much larger community.

For GNU Emacs you should, barring technical limitations, use Emacs 23.2 or any newer release after that.

GNU Emacs, unlike a lot of software products, rarely crash and suffer few major regressions between releases. So there’s no need to worry about upgrading as most releases are backwards compatible and aim to keep as many third-party modules working. For example, it is possible to download a compiled and working version of the latest Emacs release for MS-DOS!
Running Emacs in a Terminal

OK, so this is one of my pet peeves. I see many, many people run Emacs in a terminal emulator on top of their graphical window manager. Stop it, please.

I know it’s nostalgic and it takes you back to the roots of Emacs and pre-millennial computing and yes, I’m sure Richard Stallman himself runs it directly from a terminal. But please don’t.

I help out a lot of people on IRC asking how they can work around the byzantine keyboard limitations of terminal emulators and why C-s freezes their Emacs session (hint: it’s a paleolithic remnant from the mainframe days called software flow control.)

If you find yourself in a spot where using a Terminal across a SSH session is the most effective way to accomplish the task at hand, don’t let me stop you. But if you’re running Emacs locally in a terminal on your own machine you’re intentionally handicapping yourself and disabling a lot of useful features that aren’t available to you in a terminal, like proper font and color support.

To help convince you let me dispel a few common “reasons”:

    Reason: It is the only effective way to edit files remotely.

    You can probably use TRAMP to manipulate files remotely. For tasks where that is not possible Emacs in a terminal may well be the only thing that’ll get the job done Right Now.

    Reason: Emacs in a terminal is faster.

    Maybe. It’ll still take as long to load as before, as loading libraries will happen regardless of the environment you’re running it in. If you’re talking about graphical lag then that is certainly a possibility. Emacs’s display engine has gotten slower as more and more features are piled on. It shouldn’t be a problem for most modern computers though.

    Reason: Emacs in a terminal means I can use screen to switch between shells.

    You should consider running your shells inside Emacs directly. Emacs has most of the facilities needed to emulate a dumb terminal (with stdin, stdout and stderr redirected to Emacs) or even an almost fully-compatible ANSI-capable terminal.

    Reason: I like the minimalist look of Emacs in a terminal

    That’s easy to fix. Put the following in your .emacs file to hide all the extraneous crap:

    (menu-bar-mode -1)
    (tool-bar-mode -1)
    (scroll-bar-mode -1)

    That’ll hide the menu-bar, tool-bar and scroll-bar.

CUA Mode

The first thing I want to mention is CUA-mode. CUA (Common User Access) was IBM’s attempt at reining in all the conflicting ways users could interact with their programs. Most of the standards set forth back then have carried over into most modern operating systems and the programs running on them.

Emacs does not play nice with most of those standards, mostly because Emacs has been around for a lot longer, and partly because – unlike WordPerfect, WordStar and similar “killer apps” of the 90s – they no longer exist or have changed their user interfaces.

Common conflicts include the eponymous C-x and C-c keyboard modifiers. To most of us they are cut text and copy text respectively, but in Emacs they are modifier keys.

Thankfully for the CUA fans out there there is an aptly-named mode called “CUA Mode”. To enable it type M-x cua-mode.

However, cua-mode is not perfect. There are side-effects and flaws you need to be aware of:

    cua-mode redefines C-z, C-x, C-c and C-v (undo, cut, copy and paste respectively)
    C-x and C-c will behave like it would without cua-mode when you do not have text selected (no “region”)
    When the region is active it will act like normal CUA editing operations: cut, copy, paste – and so on.
    If you want to use the C-x or C-c as modifier keys with a region active you must either type the modifier key twice in a row really fast or use the shift key with the prefix key (C-S-x, for example).
    You are likely to run into peculiarities with more exotic modes and features in Emacs that may not be aware of cua-mode.
    You are ignoring the many advantages Emacs’ own text editing facilities provide – facilities that are far more advanced and feature-rich than your standard CUA-style editor commands.

And don’t forget, you can still use S-DEL, C-INS and S-INS to cut, copy and paste respectively.

Personally, I never bothered with cua-mode. Surprisingly I don’t find it difficult to switch between the different “mental modes” when I’m not using Emacs.

I’d recommend you don’t bother with it either though. It’s too much effort to compromise with such a core part of Emacs, especially when you will probably never use some of the more advanced editing concepts as a result.
Line numbers

It is possible to enable line numbers in the margin of the active buffer by running M-x linum-mode. To enable it globally for all buffers run M-x global-linum-mode.

To enable it globally and permanently add this to your .emacs file:

(global-linum-mode 1)

Now you can customize it further with:

M-x customize-group RET linum RET
IDO Mode

Ido, short for “Interactively Do Things”, is a fantastic addon that is bundled with Emacs. Basically it makes switching between buffers (and optionally files) really easy as you simply type parts of a name and Ido will automatically narrow the list to just the ones matching the search text.

I use Ido for everything (and it is extensible enough that you can use it to power your own code that requires completion) and I feel it is a must to use it in Emacs. No more fiddling around with typing out long, complicated buffer names or futile TAB’ing.

I’ll write a longer post espousing the virtues of Ido at some other point, but for now I recommend you put this in your .emacs file:

(ido-mode 1)

(setq ido-enable-flex-matching t)

IF you want Ido mode to work with C-x C-f (find-files) then add this as well:

(setq ido-everywhere t)

Some people find Ido’s find-files support a bit intrusive. Just remember that if you type C-f Ido will revert to the old-style completion engine!
Hiding the splash screen and banner

Emacs by default will pester you with a splash screen and a message in the echo area. To disable both, and have emacs default to its *scratch* buffer, add this to your .emacs:

(setq inhibit-startup-message t
inhibit-startup-echo-area-message t)  

Rebinding the CAPS LOCK key

If you ever plan on making Emacs your home away from home, your first step is to rebind your CAPS LOCK key. I know some people actually use it, but I’m one of the people who do not. So to me, rebinding CAPS LOCK is a good way to avoid the dreaded emacs pinky (so named because your pinky has to contort itself to reach the CTRL key on most keyboards.)

Getting used to the rebound CTRL key will take some time, so I suggest rebinding CAPS LOCK but leaving your old CTRL key intact so you wean yourself off the old CTRL key. On MS Windows I recommend SharpKeys, a free tool that permanently rebinds the keys. On Linux you can use xmodmap or the ‘System -> Prefs -> Keyboard’ section if you’re using Ubuntu and Gnome.

And finally, to make up for the fact that you no longer have a CAPS LOCK key I suggest learning the following keys instead:

    To UPCASE A REGION type C-x C-u; to UPCASE a single word, type M-u
    To downcase a region type C-x C-l; to downcase a single word, type M-l
    To Capitalize A Region type M-x capitalize-region; to Capitalize a single word, type M-c

You can use the universal argument construct to alter how many words are transformed ahead of point; and to make the transformation go backwards (behind point) use the negative argument modifier.
Making Emacs Auto Indent

For some insane reason Emacs will not auto-indent the point when you press RET. To do that you must type C-j. I don’t like that at all; yes, there are perfectly valid reasons for why you wouldn’t want to indent automagically. I prefer to enable it globally and then disable it locally for each mode I do not like.

Here’s how you would enable it globally:

(define-key global-map (kbd "RET") 'newline-and-indent)

How do I customize the Font and Background

There are a couple of ways of telling Emacs how to do this. I personally prefer using the Customize menu.

To customize the default font and color, type M-x customize-face RET default RET.

To customize the default syntax highlighter (also called “font locking”) typeM-x customize-group RET font-lock-faces RET.

Don’t forget to save your settings.
Undoing changes

Emacs has a very unique clipboard (called kill ring) and undo feature (called the undo ring) that few other editors have. Both are based on the concept that it should be impossible (or next to it, anyway) to lose your changes. So don’t worry about undoing changes and then editing your document; the changes you undid are still there. Simply “undo” the changes you just made and eventually Emacs will “undo” the “undone” changes. Confused? Yeah, me too.

Most people type C-x u or C-_. I prefer the far more accesible C-/, but then again I use US keyboard settings.
Loading New Packages

Packages, modules, files, collections. I don’t think the Emacs community ever really settled on a particular word for one or more files you download and load. I tend to prefer package or module myself, though.

Loading packages is usually a simple matter of, well, reading the manual… OK, so that’s not an answer but that’s usually true. It does happen though that the file does not come with a manual – maybe you got it on EmacsWiki and the author never intended for it to be used by newbies.

So if you’re stuck without a manual try opening the file (in Emacs of course!) and look in the comment header for instructions. Most files will have the instructions listed there and possibly even some usage examples, depending on what the package sets out to do.

If that fails, you can try loading it yourself with this generic, handy-dandy guide.
Setting up your load path

Your load path is where Emacs will search for files to load.

To inspect the load path you can type C-h v load-path RET. That command asks Emacs to tell us the value (and any documentation associated with the variable) and print it in a buffer.

If you put your package anywhere in one of those places, Emacs will find it. That’s not very flexible though, and you may not have permissions to write in any of them. So let’s add our own. Add this to your .emacs, substituting the example path below with one of your own choosing. I recommend ~/.emacs.d/ or another sub-directory to your home directory.

;; You can change the path here
(add-to-list 'load-path "~/.emacs.d/")

Now that you’ve added a custom path you can put your files in there. If your package has lots of files and its own directory structure you can go ahead and explicitly instead.
Loading the package

Emacs can load files in one of several ways:

    By invoking (require 'feature) if the package has (provide 'feature) somewhere in the file.
    By explicitly calling (load-library "packagefilename"). I would recommend this unless you know the name of the feature provided by the package.

Whichever way you pick, add it to your .emacs – but add it after you update the load-path!
Testing that it worked

Now you can either restart Emacs and see if it works, or you can select commands you added above and run M-x eval-region. If it worked, not much will happen. You can switch to the buffer *Messages* and see if you can spot any errors.

Now you’re ready to use your new package.
Conclusion

That covers some of the major questions the tutorial leaves unanswered, plus a few of my own personal preferences thrown in for good measure. Feel free to share yours by either contacting me or posting a comment.
Further Reading

I recommend reading my article series Effective Editing in Emacs. It will teach you how to move, edit and find what you’re looking for – all things people spend years mastering.



# Basic usage

  Indent              Select text then press TAB
  Cut                 CTRL-w
  Copy                ALT-w
  Paste               CTRL-y
  Search/Find         CTRL-s
  Replace             ALT-% (ALT-SHIFT-5)
  Save                CTRL-x CTRL-s
  Load/Open           CTRL-x CTRL-f
  Undo                CTRL-x u
  Highlight all text  CTRL-x h
  Directory listing   CTRL-x d
  Cancel a command    ESC ESC ESC
  Font size bigger    CTRL-x CTRL-+
  Font size smaller   CTRL-x CTRL--

#  Buffers

  Split screen vertically                         CTRL-x 2
  Split screen vertically with 5 row height       CTRL-u 5 CTRL-x 2
  Split screen horizontally                       CTRL-x 3
  Split screen horizontally with 24 column width  CTRL-u 24 CTRL-x 3
  Revert to single screen                         CTRL-x 1
  Hide the current screen                         CTRL-x 0
  Kill the current screen                         CTRL-x k
  Move to the next buffer                         CTRL-x O
  Select a buffer                                 CTRL-x b
  Run command in the scratch buffer               CTRL-x CTRL-e

# Other stuff

  Open a shell         ALT-x eshell
  Goto a line number   ALT-x goto-line
  Word wrap            ALT-x toggle-word-wrap
  Spell checking       ALT-x flyspell-mode
  Line numbers         ALT-x linum-mode
  Toggle line wrap     ALT-x visual-line-mode
  Compile some code    ALT-x compile
  List packages        ALT-x package-list-packages

#  Sudoing within eshell

  By default when using the sudo command within eshell you'll just
  get "permission denied" messages. To overcome that type:

    alias sudo '*sudo $*'

# Line numbers

  To add line numbers and enable moving to a line with CTRL-l:

    (global-set-key "\C-l" 'goto-line)
    (add-hook 'find-file-hook (lambda () (linum-mode 1)))

# Org-mode

  To begin org-mode                            ALT-x org-mode
  Table column separator                       Vertical/pipe character
  Reorganize table                             TAB
  Section heading                              *
  Open/collapse section                        TAB
  Open/collapse All                            CTRL-TAB
  Export in other file formats (eg HTML,PDF)   CTRL-c CTRL-e

  To make org-mode automatically wrap lines:

    (add-hook 'org-mode-hook
              '(lambda ()
                 (visual-line-mode 1)))
