# How to print some text in italic?

Press `C-c i` before the text, and press `C-c o` after it.

    /this is some C-c i italicized C-c o text

You can apply other attributes.
See here for more info:
<https://weechat.org/files/doc/stable/weechat_user.en.html#command_line_colors>

---

Note that some attributes (which ones?) may not work if the channel has the `+c`
mode on freenode.

   > Strip colour and formatting codes from channel messages.

Source: <https://freenode.net/kb/answer/channelmodes>

Most channels we visit atm have the `+c` mode, except `#ranger` and `#regex`.

---

You can combine attributes:

    /this is some C-c b C-c i bold and italicized C-c o text

# How to print the version of my WeeChat in the current channel?

    /v -o

# ?

Configurer un pseudo par défaut.

    /set irc.server_default.nicks        comma,separated,list,of,nicks
    /set irc.server.[SERVER_NAME].nicks  "

S'identifier automatiquement sur freenode:

    /set irc.server.freenode.command = "/msg NickServ identify {mdp}"

C-s C-u         Set unread marker on all windows
M-a             Next buffer with activity
M-0...9         go to buffer 0...9


Utiliser  l'*autocomplétion* pour  découvrir  de  nouvelles commandes,  options,
paramètres ou  pour taper  un message  en le  faisant précéder  du pseudo  de la
personne à laquelle il s'adresse.

La fenêtre  1 contient plusieurs  buffers correspondant aux  différents serveurs
auxquels on est  connecté (plus un, appelé weechat, qui  correspond au buffer de
l'application elle-même).

On peut changer le buffer ayant le focus via C-x.

Pour lire ses messages il peut s'avérer nécessaire de scroll via PgUp/PgDown car
les messages des différents buffers s'affichent sur la même fenêtre.

Le buffer ayant le focus influe sur la prochaine commande tapée.

Pex: on ne  peut pas rejoindre le chan  #ubuntu si on est pas dans  le buffer du
serveur ou d'un canal freenode.

##
##
##
# What's the chat area?

The part of the screen where the messages, nicks, and timestamps are displayed.

# What's the prefix in the chat area?

The text before the first pipe.
It contains the timestamps and the nicks.

# What's the bare display mode good for?

To easily open multi-line urls.

Alternatively, you could install the `urlserver.py` script to shorten long urls:

        https://weechat.org/scripts/source/urlserver.py.html/

Although, I'm concerned about the security:

        - you have to trust the script author
        - you have to trust to secure the http server embedded into the script
        - urls are obfuscated, you can't have a look at them and see whether they're suspicious

# How to toggle the filter in the current buffer?

Press `M--`.
         ^
         don't use `AltGr-f`,
         use the minus sign on the keypad or the one on the `6` key

##
# Configuration

    /help option    afficher une description de l'option, les valeurs (+le type) qu'elle peut prendre,
                    sa valeur par défaut, et sa valeur actuelle

    /set opt val

                    donner la valeur val à l'option opt
                    val peut être un booléen (on ou off)

    weechat.bar.nicklist.hidden    off par défaut

                    masquage de la barre des personnes ayant joint le channel

    weechat.look.buffer_time_format

                    formater de l'affichage de l'heure devant les messages
                    Pour afficher seulement les heures et les minutes, utiliser la valeur:    "%H:%M"

    weechat.look.prefix_align_max

                    largeur max de la barre des pseudos devant les messages (0 par défaut; 10 est une bonne valeur)

iset.pl est un script permettant de modifier la configuration de weechat via une interface en TUI plutôt qu'en cli.

    /iset       lance le script

    foo RET     limite l'affichage aux options contenant le mot foo (filtrage)
    * RET       annule le filtrage

    M-space     toggle un booléen (true, false)

    M- +-       augmenter / diminuer la valeur numérique d'une option
                ou pour avancer / reculer dans une liste de couleurs
                ne pas utiliser le pavé numérique pour les symboles + et -

    M-enter     modifier manuellement la valeur d'une option

    M-iri       réinitialiser la valeur d'une option

# Nickserv

NickServ permet d'enregistrer un pseudo dans une bdd afin d'empêcher les autres de l'utiliser.

    /msg NickServ help
    /msg NickServ help cmd

            Liste les commandes NickServ disponibles.

            Affiche l'aide de NickServ cmd.


    /msg NickServ REGISTER mdp foo@bar.com
    /msg NickServ VERIFY REGISTER <my nick> <code reçu par mail>
    /msg NickServ Identify mdp
    /msg NickServ access list

            Enregistre le pseudo courant en l'associant à l'adresse mail foo@bar.com et à un mdp
            sous weechat, on ne voit ni le mdp ni l'adresse mail tapée (remplacés par des *).

            Vérifie auprès du réseau irc qu'on est bien le propriétaire de l'adresse mail fournie.
            Bien lire le mdp qu'on a fourni (seul moment où il s'affiche en clair).

            S'authentifie auprès du réseau en fournissant mdp.

            Liste les @ autorisées à utiliser le pseudo courant sans s'authentifier.

# Messages

    /buffer clear

            Nettoyer l'affichage des messages du buffer.


    /nick <new nick>

            Changer de pseudo.


    /query <nick>

            Ouvre une fenêtre de discussion privée avec <nick>.


    irc.server_default.username

            Option définissant notre nom utilisateur affiché dans un /who(is) (~user@ip).

                    suggestion : john

                    irc.server.foo.username a la priorité quand on se connecte au serveur foo


    irc.server_default.realname

            Option définissant notre vrai nom affiché dans un /who(is).

                    suggestion : doe

                    irc.server.foo.realname a la priorité quand on se connecte au serveur foo

# Modes

    /mode #chan
    /mode <my nick>

            Affiche les modes de #chan.
            Affiche nos modes.


    /mode <my nick> {+i -i}

            Ajoute / supprime notre mode invisible.

            Mode invisible = seule une personne connaissant notre pseudo ou présente sur le même chan
            peut nous voir avec un /who.

# Filtrage

    C-r foo

        Chercher toutes les occurrences de la chaîne foo dans les messages.
        Flèche haut / bas pour naviguer entre les occurrences.
        En  réappuyant sur  C-r on  peut faire  une recherche  par regex  plutôt
        qu'une chaîne.


    /help filter

        Aide de la commande /filter.


    /debug tags

        Toggle the display of the tags bound to each message.
        tags allow you to filter messages.

    M-=

        Toggle le filtrage globalement.


    /filter list | enable | disable | toggle [myfilter]

        Affiche la liste de tous les filtres, les active, désactive, toggle.
        Optionnellement,  on peut  donner le  nom  d'un filtre  pour limiter  la
        portée d'une action à un filtre précis.


    /filter add joinquit * irc_join,irc_part,irc_quit *

        Filtre n'importe quel message (2e *) portant les tags irc_join, irc_part
        ou irc_quit dans tous les buffers (1er *).

        La syntaxe générale de la commande /filter est:

                /filter {cmd} {name} {buffers} {tags} {regex}

        {buffers}, {tags}, et {regex} permettent de limiter la portée d'un filtre selon:

                - le nom du buffer où on se trouve
                - le tag que porte le message
                - le contenu du message

        {buffers}  et  {tags}  sont  des  listes de  valeurs  séparées  par  des
        virgules.
        Une  valeur présente  dans  {buffers}  peut être  un  nom explicite,  un
        pattern utilisant * (wildcard), et/ou ! (inversion du pattern).

        {regex} doit:

                - utiliser \t pour séparer le préfixe du message dans ce cas
                  2 regexes sont créées (à gauche pour le préfixe, à droite pour
                  le message)

                - échapper les caractères spéciaux tq le pipe (et !)
                - utiliser ! au début pour inverser la regex
                - utiliser (?-i) au début pour devenir insensible à la casse


    /filter add irc_smart * irc_smart_filter *

        utilise le filtrage intelligent sur tous les buffers

        FIXME: c'est quoi le filtrage intelligent / tag irc_smart_filter ?

        Il semble que ce soit un  tag spécial permettant de filtrer les messages
        join/part/quit sauf si ça concerne qn qui a parlé récemment:

            https://weechat.org/files/doc/weechat_faq.en.html#filter_irc_join_part_quit


    /filter add irc_smart *,!*#weechat* irc_smart_filter *

        utilise le filtrage intelligent sur tous les buffers sauf (!) ceux qui contiennent #weechat dans leur nom


    /filter add toto irc.freenode.#weechat nick_toto *

        crée le filtre toto qui masque les messages de l'utilisateur toto sur le channel #weechat
        du réseau freenode


    /filter add sucks irc.freenode.#weechat * weechat sucks

        crée le filtre sucks qui masque les messages contenant 'weechat sucks' sur le channel #weechat
        du réseau freenode


    /filter del myfilter
    /filter del -all

        supprime myfilter ou tous les filtres

# Navigation

    [alt + ] pgup / pgdown          scroll vertical du texte par lot de [3] 20 lignes

    alt + flèches              naviguer entre les différentes fenêtres (serveurs, canaux, ...)
    alf + <n>               se rendre à la fenêtre <n> (ne pas taper <n> via le pavé numérique)

# Layout

    /window splitv                      diviser la fenêtre verticalement
    /window splith                      idem mais horizontalement
    /window merge                       fusionner 2 splits
    /window swap                        échanger la position de 2 splits

    /window +1 -1 left right up down    changer le focus entre plusieurs splits

    weechat.bar.nicklist.position       option gérant la position de la barre des pseudos (par défaut "right")

    weechat.bar.nicklist.size           option définissant la largeur (en nb de caractères) de la barre des pseudos

# Script

script est un plugin intégré à weechat permettant de gérer ses scripts via la commande /script.

flèche haut / bas, PgUp / PgDown permet la navigation au sein de la liste.

    /help script

            Affiche une liste complète des commandes et hotkeys, ainsi que la signification des infos
            affichées dans le buffer.


Les noms des scripts peuvent être précédés d'un ou plusieurs flags (statuts) :

        * : populaire
        i : installé
        a : chargé automatiquement (autoloaded)
        r : en cours d'exécution (running)

    /help script.look.sort      liste les différents tris dispo et la commande à taper pour chacun
                                cette option gère le filtrage par défaut

    s:i RET             liste d'abord les scripts installés
    s:p,n               liste d'abord les scripts les + populaires (p), puis trie les scripts par nom
    s:p,-n              idem mais cette fois inverse le tri par nom (- = inversion du tri)

    foo RET             filtre les scripts en n'affichant que ceux dont le nom ou la description contient foo

    * RET               supprime le filrage

    M-i r               installe, supprime le script sélectionné

    M-v                 alterne entre la description détaillée du script sélectionné
                        et la liste globale des scripts

    q RET               quitter le buffer script

    /foo                lance le script foo

##
# Todo
## To Read

From the less to the most complex:

- <https://weechat.org/files/doc/stable/weechat_quickstart.en.html>
- <https://weechat.org/files/doc/stable/weechat_faq.en.html>
- <https://guides.fixato.org/setting_up_weechat.html>
- <https://github.com/weechat/weechat/wiki>
- <https://gist.github.com/pascalpoitras/8406501>

- <https://weechat.org/files/doc/stable/weechat_user.en.html>
- <https://weechat.org/files/doc/stable/weechat_scripting.en.html>
- <https://weechat.org/files/doc/stable/weechat_plugin_api.en.html>
- <https://weechat.org/files/doc/stable/weechat_relay_protocol.en.html>

Misc:

- <https://news.ycombinator.com/item?id=12267254>
- <https://aaronparecki.com/2015/08/29/8/why-i-live-in-irc>
- <https://botbot.me/how-to-setup-irc-channel/>

---

Web interface:

- <https://hveem.no/a-modern-IRC-experience>
- <https://github.com/glowing-bear/glowing-bear/>

Pro:

   - access weechat from any device with a browser
   - images, videos, and other content are embedded

---

Network-specific rules:

- <https://freenode.net/kb/all>
- <https://www.abjects.net/page.php?10>

## learn how to paste multiline message

<https://weechat.org/scripts/source/multiline.pl.html/>

## Should we restore those default key bindings?   (which I've removed)

4 key bindings added or redefined for context "default":

        meta-meta-OP => /bar scroll buflist * b
        meta-meta-OQ => /bar scroll buflist * e
        meta-OP => /bar scroll buflist * -100%
        meta-OQ => /bar scroll buflist * +100%

16 key bindings added or redefined for context "mouse":

        @bar(buflist):ctrl-wheeldown => hsignal:buflist_mouse
        @bar(buflist):ctrl-wheelup => hsignal:buflist_mouse
        @chat(fset.fset):button1 => /window ${_window_number};/fset -go ${_chat_line_y}
        @chat(fset.fset):button2* => hsignal:fset_mouse
        @chat(fset.fset):wheeldown => /fset -down 5
        @chat(fset.fset):wheelup => /fset -up 5
        @chat(script.scripts):button1 => /window ${_window_number};/script go ${_chat_line_y}
        @chat(script.scripts):button2 => /window ${_window_number};/script go ${_chat_line_y};/script installremove -q ${script_name_with_extension}
        @chat(script.scripts):wheeldown => /script down 5
        @chat(script.scripts):wheelup => /script up 5
        @item(buflist):button1* => hsignal:buflist_mouse
        @item(buflist):button2* => hsignal:buflist_mouse
        @item(buflist2):button1* => hsignal:buflist_mouse
        @item(buflist2):button2* => hsignal:buflist_mouse
        @item(buflist3):button1* => hsignal:buflist_mouse
        @item(buflist3):button2* => hsignal:buflist_mouse

## learn how to use cursor mode

Cursor mode  lets you interact  with some pieces  of information present  in the
buffer more easily.
For example,  you can  quote someone by  moving your cursor  over a  message and
pressing `m`.

   - <https://github.com/weechat/weechat/wiki/Cursor-mode>
   - <https://weechat.org/files/doc/devel/weechat_user.en.html#key_bindings_cursor_context>

Try to install key bindings using the keys h, j, k, l to move in cursor mode.
You'll probably need to make them local to cursor mode.
To achieve that, you'll need to understand the concept of “context” in `/help key`.
Read also `/help cursor`.

## learn how to bind a key differently depending on the type of the buffer

    vejetaryen▹│ Is there a way to bind keys for specific window? I mean, I want meta-j to bind /window page_down in all
               │ windows except for fset's window. In fset, I want meta-j to bind /fset -down. Is it possible?
               │ I mean, I won't use /window page_down in fset anyways.
        sim642 │ You can bind it to some /eval, which uses ${if:...} to output one of the two commands
               │ Based on the current buffer name

