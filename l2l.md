# Where to find documentation for a program?

   - $ man pgm

   - amazon book

   - wiki (github, gitlab, ...)

   - faq (often included in the github wiki)

   - configuration files

           $ git clone <url> && cd <dir> && find -type f -name '*.conf'

       e.g. `mpv`, `ranger`, ...

   - official website

       e.g. https://weechat.org/doc/

# How to write good documentation?

<https://writing.stackexchange.com/a/34138/30109>

# Accelerated learning techniques

Selon la théorie du cerveau triunique, on peut décomposer le cerveau en 3 parties:

    ┌───────────────────┬───────────────┬────────────────────────────────────────────────┐
    │ nom               │ emplacement   │ fonction                                       │
    ├───────────────────┼───────────────┼────────────────────────────────────────────────┤
    │ cerveau reptilien │ base du crâne │ fonctions vitales basiques:                    │
    │                   │               │ respiration, rythme cardiaque, pression        │
    │                   │               │ artérielle                                     │
    │                   │               │                                                │
    │                   │               │ comportements instinctifs (survie):            │
    │                   │               │ réponse combat-fuite                           │
    ├───────────────────┼───────────────┼────────────────────────────────────────────────┤
    │ cerveau limbique  │               │ régule les systèmes immunitaire et hormonal    │                                          │
    │                   │               │        la sexualité                            │
    │                   │               │        l'humeur                                │
    │                   │               │        les sentiments et émotions              │
    │                   │               │                                                │
    │                   │               │ contrôle une partie de la mémoire à long-terme │
    ├───────────────────┼───────────────┼────────────────────────────────────────────────┤
    │ néocortex         │               │ pensée                                         │
    └───────────────────┴───────────────┴────────────────────────────────────────────────┘

Qd on ressent de la _peur, de  l'anxiété, du stress_, le cerveau reptilien prend
le dessus, et met en oeuvre la réponse combat-fuite: de l'adrénaline est envoyée
dans notre corps, et le cerveau rétrograde en mode survie.
Cela nous empêche d'accéder à nos [facultés de réflexions d'ordre supérieures][1].

Cette rétrogradation mentale est une stratégie datant de le préhistoire.
Elle nous permettait de réagir rapidement face à un danger imminent (ex: fauve).

On la rencontre  encore aujourd'hui lors d'un examen au  cours duquel on devient
anxieux / stressé pour une raison donnée.
On perd alors la  faculté de penser clairement; même si on  connait la réponse à
une question, on est incapable de retrouver l'information.
Il existe  une technique pour  faire face à ce  problème, qui consiste  à entrer
dans un  mode mental optimisé  pour la  réflexion: dans ce  mode, on a  un accès
maximal à nos facultés de réflexions d'ordre supérieures.


Le système limbique contient entre autres:

   - le [thalamus][2]
   - l'[amygdale cérébrale][3]
   - l'[hippocampe][4]

Le  thalamus  contrôle   la  destination  où  les   informations  qu'on  perçoit
(visuelles, auditives, kinesthésiques)  sont envoyées dans le  cerveau pour être
traitées.

All of the visual, auditory, and  kinesthetic information from our senses enters
the thalamus, where it  is categorized and sent to different  parts of the brain
for processing.
The thalamus actually  sends sensory information in two  different directions at
the same time.
The first  direction (the high road)  leads to the sensory  cortices: the visual
cortex, the auditory cortex, and the somatosensory cortex.
These are located in  the neocortex and will be discussed in  more detail in the
next section.
As shown in the  figure below, the second direction in  which the thalamus sends
sensory information (the low road) leads to the amygdala.

# Comment assimiler un plugin Vim

    $ git clone https://github.com/romainl/vim-qf

Cloner le repo.

Pourquoi?

Il faudra commit le plus tôt possible.

De plus, dans un repo git,  `vim-gutentags` génère automatiquement un fichier de
tags nous permettant de nous déplacer vers la définition d'une fonction beaucoup
plus rapidement.

On peut aussi pousser une copie locale du repo après un 1er refactoring basique.


    $ cd ~/Dropbox/vim_plugins/vim-qf/
    :args ./**/*.vim

Peupler l'arglist avec tous les fichiers du projet.

    co C-s

Désactiver  la  sauvegarde  automatique   pour  pouvoir  facilement  annuler  un
refactoring ayant échoué.

Utiliser `:argdo update` à chaque fois qu'on pense qu'un refactoring a réussi.


    :argdo 1norm dic
    :argdo 1;/set cpo&vim/d_
    :argdo $?let &cpo?;$d_
    :argdo 1 | if empty(getline('.')) | d_ | endif
    :argdo $ | if empty(getline('.')) | d_ | endif

Supprimer  des  lignes  inutiles   (commentaire  d'introduction,  sauvegarde  et
restauration `'cpo'`, ligne vide).

    :argdo Refactor

Refactoring de base dans tous les fichiers.

    :argdo RefQuotes

Remplacer des chaînes non littérales en chaînes littérales aussi souvent que possible.

    :argdo RefDots

Supprimer des espaces superflus autour de chaque opérateur de concaténation.

    :vim  /exists(/gj  ./**/*.vim
    :vim  /has(/gj     ./**/*.vim
    :vim  /\<get(/gj   ./**/*.vim

Chercher des  tests ou des  options inutiles,  qu'on pourrait supprimer  afin de
simplifier le code.


Dans chaque fichier:

   - Déplacer un  commentaire au-dessus de  la définition d'une fonction  sous
     son nom  (pour qu'il soit à  l'intérieur).  Utiliser `]a` et  `]m` pour
     passer d'un  fichier à un autre,  et d'une fonction à une autre.

   - Ajouter un marqueur de pliage `{{{1|2|…` après chaque définition de
     fonction.

   - Utiliser `:RefDots`, `:RefIf`, `:RefQuotes`, `:RefVval` à chaque fois que c'est possible.

   - Si un nom de fonction utilise la casse `camelCase` ou `MixedCase`, le
     forcer à utiliser `snake_case`:

       - *                   peupler le registre recherche avec le nom de la fonction
       - vim // ./**/.vim      peupler la qfl avec les lignes où le nom de la fonction apparaîte
       - ]q crs              demander une conversion vers `camelCase`
       ; .
       ; .
       …

      Une fois le refactoring effectué, dans le buffer `qf`, exécuter `:Cupdate` pour vérifier
      que tout s'est bien passé.

      TODO:
      J'ai essayé d'automatiser cette étape via:

            :cdo norm crs

      Parfois ça marchait, mais par moment  j'ai l'impression que ça échouait et
      peut-être même qu'une édition indésirable avait lieue.

      Peut-être que le  pb vient de `:norm`  qui ne place pas le  curseur sur la
      bonne colonne avant d'exécuter `crs`.
      La prochaine fois tenter ça:

            :cdo call feedkeys('crs', 'it')


Pousser une copie du repo sur github, et après chaque refactoring, tester le bon
fonctionnement du plugin via:

    $ vim -Nu /tmp/vimrc file
              └────────┤
                       └ peuplé via le snippet `vimrc`

Commit si tout fonctionne correctement.


Écrire la documentation au fur et à mesure qu'on assimile le plugin.
En particulier, rédiger  une partie destinée à un  utilisateur avancé:  Internal
details.
L'utiliser pour expliquer l'idée générale  utilisée par le plugin pour accomplir
son travail.
Qd  on  l'écrit,  s'imaginer  qu'on  est  en  train  de  parler  à  un  collègue
programmeur, qui cherche à implémenter le même genre de plugin, mais qui ne sait
pas dans quelle direction partir.
On ne lui expliquera pas le  fonctionnement du plugin dans ses moindres détails;
les appels de fonctions, les noms de variables, ...

# Comment prendre ses notes

    Bonne structure globale

Qd on cherche une info, on trouve rapidement la section où elle se trouve.
Section = chemin pour y parvenir = chapitre + sous-chapitre + ...

    Bonne structure fine

Au sein d'une section, théorie vers le haut, pratique vers le bas.
Ordre alphabétique pour des commandes.

    Éviter la répétition

Une répétition signifie qu'il faut:

   - supprimer qch

   - restructure ses notes
     fusionner 2 sections, et éventuellement faire péter la fusion si trop grande

   - reformuler une idée dont on vient de voir plusieurs aspects différents
     faire des liens participe à une meilleure compréhension

En évitant de se répéter, on est amené à dégager des règles.
Ceci a 2 avantages:

   - qd on tombera sur un nouveau cas de figure où la règle s'applique, on le
     saura immédiatement. Pas besoin d'expérimenter. Gain de temps.

   - les notes sur différents cas de figures seront plus courtes. On cernera
     mieux l'info pertinente, càd propre à ce cas de figure.

Format question-réponse

Pas forcément de vraies questions.
Une commande / une citation / une affirmation / une date (truc bref dont on aura besoin en pratique)
+
description et explication

    Éviter la pure théorie au maximum

La pure  théorie ne devrait être  nécessaire que pour définir  quelques nouveaux
concepts / idées / mots de voca.

Le faire au début d'une section qd c'est nécessaire.
Comme ça qd on  trouve une info pratique ds une section,  mais qu'on ne comprend
pas bien un  mot, on sait tout de  suite qu'il faut chercher vers le  haut de la
section.

    Synthétiser

Faire des phrases courtes.
Faire péter les longues.

Réduire en utilisant de nouveaux mots de voca.
Faire apparaître l'info importante dans une phrase vers le début.
Si on peut pas réduire un concept en qq lignes, il est encore trop tôt.
Il nous manque des concepts intermédiaires.

# Résoudre un problème

Qd  on émet  une hypothèse  pour expliquer  l'origine d'un  problème, dès  qu'on
trouve une contradiction, en chercher une nouvelle.

On perd souvent du temps en s'entêtant  à essayer de prouver la 1e hypothèse qui
nous est venue à l'esprit.
En effet, cette dernière bénéficie sans doute d'un effet de primauté.
C'est la plus évidente, donc on rejette l'idée même qu'elle puisse être fausse.

Ceci est un piège.
Contradiction = tout de suite chercher une autre hypothèse.
Ne pas approfondir une hypothèse avant d'en avoir exploré un maximum:

            “breadth before depth”



Qd  on rencontre  un  problème difficile,  ne  pas s'obstiner  à  chercher à  le
résoudre.
Un tel problème vient rarement seul.
Il est souvent accompagné par/décomposable en plusieurs autres problèmes.

Les noter TOUS explicitement, et le plus clairement possible, au fur et à mesure
qu'on en rencontre au cours de notre tentative de résolution.

Passer  régulièrement de  l'un à  l'autre  dès qu'on  n'arrive plus  à faire  de
progrès.
Il  se peut  que l'un  d'eux soit  plus  facile que  les autres,  et qu'il  nous
permette de résoudre facilement les autres.

Il faut  voir un problème  difficile comme un PUZZLE,  pas comme un  roman qu'on
doit lire du début à la fin.



Qd on rencontre un bug, il ne faut pas chercher à le réparer immédiatement.
Au préalable, il faut chercher à le simplifier un maximum.
En    effet,   on    ne    sait    pas   à    l'avance    combien   de    cycles
"hypothèse-tentative-échec" il faudra réaliser avant de trouver la solution.
Si ce  nombre est  grand, on a  tout intérêt  à réduire la  durée d'un  cycle au
maximum.
Autrement le déboguage sera long et décourageant.

Il s'agit de trouver un MWE.
Toutefois, un MWE ne signifie pas nécessairement un minimium de texte.
En effet, si un MWE ne permet pas  de mieux comprendre le problème, il peut être
judicieux de rajouter un peu de texte, afin d'expliciter l'implicite.
Pour rappel, il  nous est arrivé de  perdre du temps à comprendre  une regex qui
nous donnait  l'impression que le  moteur de Vim  n'utilisait pas la  1e branche
matchant  du  texte,  mais  celle  matchant  le plus  long  texte,  ce  qui  est
inhabituel.
En réalité, il y avait plusieurs matchs qu'on confondait en un seul.
La confusion a été levé en explicitant l'ancre `^` au début de la 2e branche:

    .*pat\|^.*



Il y a un thème récurrent qui se dégage jusqu'ici:

Qd qch attire notre attention (solution, problème, bug), on a souvent tendance à
ne plus rien voir autour, ce qui nous fait perdre parfois beaucoup de temps.
Il  faut s'habituer  à prendre  du  recul dès  que  qch devient  pénible, et  se
demander s'il  n'y a pas qch  d'autre qui mérite davantage  notre attention dans
l'immédiat.

---

If:

   - you have an issue which you fully understand

   - you think you have a solution, but for some reason it doesn't work

   - after spending quite some time, you still can't find anything wrong with
     the solution

ask yourself these questions:

   1. What am I trying to do?
   2. What makes me think it's possible?
   3. What could explain that my belief is wrong?

Example of answers:

   1. I'm trying to find a condition to prevent my autocmd to install a match
      (trailing whitespace) in a fzf buffer

   2. when my autocmd is fired, I can detect the filetype of the buffer

   3. the filetype has not been set yet

# Modularisation

Réduire le temps d'accès.

    Cartes répétition espacée

    Notes wiki personnel

    Cheatsheets

    Snippets

    Fichier de conf commentés

# Cartes mentales

Structue un gd nb de sources d'infos variées:
capture d'écran ; liens vers pages, vidéo, documents...

Les cartes mentales sont sans doute très utiles pour s'organiser avant d'agir.
Mais pas pour prendre des notes et comprendre qch.
Pour prendre des notes, un wiki et des diagrammes sont plus adéquates.

# Cognitif vs métacognitif

Les stratégies cognitives sont les procédures, les techniques qu'on utilise pour
réussir une tâche.

Les stratégies  métacognitives consistent  à réfléchir sur  sa façon  de penser,
d'agir et d'apprendre pour en évaluer l'efficacité et pour l'améliorer.

Pour  rendre sa  manière d'apprendre  plus efficace,  on doit  s'interroger pour
savoir comment on apprend.

# Top-Down vs Bottom-Up

    Top-Down

Technique d'apprentissage dans  laquelle on commence par  comprendre le contexte
général avant de passer aux détails.

    Bottom-Up

Dans le  cadre du  bottom-up il  est important de  constituer des  “chunks”, des
ensembles  neuronaux très  serrés que  notre cerveau  sera capable  de manipuler
comme des blocs.

Inutile de lire et de relire un texte indéfiniment pour être sûr d'avoir compris
et maîtrisé un sujet.
En  fait, il  est  beaucoup plus  malin  de se  répéter ce  qu'on  a appris,  de
reformuler le contenu  de la leçon jusqu'à  être capable de le  réexpliquer à sa
façon.

Cette technique est plus efficace que  d'autres méthodes plus élaborées comme la
création de schémas conceptuels.

En effet on essaie  trop souvent de bâtir des relations  entre des concepts sans
avoir  auparavant maîtrisé  les clusters  correspondant  à ces  concepts ce  qui
équivaut à apprendre des stratégies avancées  du jeu d'Échecs sans connaître les
règles de base.

# Concentration

Principe de Pareto:

    https://fr.wikipedia.org/wiki/Principe_de_Pareto

Mode concentré vs mode diffus:

    http://www.internetactu.net/2015/09/08/apprendre-a-apprendre-14-deux-modes-dapprentissage/

# Astuces

    Structurer l'info

Plus  facile d'intégrer  une grande  quantité d'infos  quand elle  nous apparaît
comme cohérente.

Structurer l'info  signifie la transformer sous  une forme qui nous  paraît plus
accessible.
Moins on a besoin de faire d'efforts de compréhension mieux c'est.

Rendre l'info + accessible fait partie d'un processus d'assimilation.

Cette page est une excellent illustration du principe:

    https://noahfrederick.com/log/a-list-of-vims-lists/

Plusieurs notions complexes sont regroupées et comparées.
On constate qu'elles sont proches les unes des autres, on peut les manipuler via
des commandes similaires, et emplissent un objectif similaire.

    Définir objectif clair et motivant

La clarté est nécessaire  pour pouvoir faire le tri entre  les sources qu'il est
utile d'analyser et celles qui ne sont pas intéressantes.

La motivation est nécessaire pour s'investir bcp.

    Dialogue entre théorie et pratique

    Partir de ce qui marche

Quand on  a plusieurs  sources pour  accomplir un objectif  donné, et  que l'une
d'elles fournit des infos qui semblent  erronées, il faut commencer à travailler
à partir d'une  autre source pour lesquelles les infos  fonctionnent puis tenter
d'intégrer un maximum d'infos de la source problématique.

Ne pas perdre son temps à chercher à comprendre tout de suite pourquoi des infos
ne  fonctionnent pas,  car le  pb peut  se résoudre  en lisant  d'autres sources
d'infos.

    Relire ses notes avec un esprit critique

Quand on relit  ses notes, cheatsheets, rester  attentif à ce qui  ne marche pas
(pex.
une  info qu'on  met trop  de temps  à trouver  ou à  comprendre), apporter  les
modifications nécessaires et  en tirer un enseignement pour  améliorer les notes
futures.

    Laisser reposer (agilité mentale)

Quand on a noté bcp d'infos sur un sujet donné et qu'on sent qu'on a du mal à en
assimiler plus :

   1. passer à un autre sujet

   2. revenir sur le sujet précédent le lendemain, en relisant ses notes à haute
      voix pour vérifier qu'on comprend bien et si besoin les éditer / modifier
      pour les rendre plus claires

        Condenser

Qd on  prend ses  notes, il faut  aller à l'essentiel  et toujours  chercher une
formulation qui prend un minimum de caractères.

Si  on  n'arrive  pas  à  condenser  une  information  en  suffisamment  peu  de
caractères, ça signifie probablement qu'il  faut la décomposer en plusieurs sous
informations, pas forcément au même endroit.
C'est peut-être aussi dû au fait que l'information est encore trop complexe pour
être assimilé, il nous manque des notions importantes.

Condenser  l'information est  utile  pour  retrouver +  rapidement  ce qui  nous
intéresse (temps d'accès),  et aussi pour créer des cartes  Anki (qui ont besoin
de questions / réponses courtes).

    Couleurs

commandes en bleu sortie / résultat des commandes en vert ...

# J'apprends si ...

Je suis concerné par ce que j'apprends.
J'y trouve un intérêt, un sens.
J'ai confiance en mes capacités.
Je m'appuie sur mes connaissances.
Je fais des liens entre les connaissances acquises.
Je m'appuie sur mes stratégies privilégiées.
Je prends conscience du savoir que j'ai acquis.
Je me confronte aux autres.

# Comment aborder un sujet confus

   1. Trouver et dumper les info liées au sujet qui semble confus.

   2. Réduire l'info en:

       - supprimant le "bruit", càd des infos:

       * redondantes
       * pas ou peu intéressantes
       * expliquées par des règles déduites dans l'étape 3

       - factorisant le + possible

   3. Déduire des règles. Puis revenir à l'étape 2. Répéter jusqu'à ce qu'il n'y
      ait plus qu'un minimum d'infos et un max de règles.

---

Notes can be confusing because of its terminology.
A good example is the manpage for `update-alternatives`.
It refers to 3 related concepts with different words:

   - generic name, alternative link
   - alternative name
   - alternative, alternative path

`generic name` is confusing because it's completely different than all the other words.
`alternative` is confusing  because whenever you read it, you  wonder whether it
means “alternative path”, or an alternative as a whole (link, name, path).

If the documentation uses different terminologies, edit it to make it more consistent.
Always use the same word to refer to the same concept.
Choose the word which is used the most often in the official documentation.

Exception:

If  the most  used word  is confusing  in itself  (e.g. generic  name), and  the
subject you're  studying is has a  very limited area of  application, and you're
not  going to  study it  for a  long time,  then it's  ok to  use another  word,
provided it's still used somewhere in the documentation.

So,  in the  previous example,  it's  ok to  use “alternative  link” instead  of
“generic name”.

---

If the documentation is still confusing, that's probably because it lacks some info.

How to gain more info?
Use  the info  you have  noted  to do  sth  practical; for  anything related  to
computer science, it means running commands.

This implies that you should remove any note which can't be used in practice.
After using the info, study the effects of what you did to gather more info.

For example, in computer science, running commands is useful because you can see
whether  files were  created,  how many,  where,  ... or  you  can run  commands
verbosely and read a logfile...

However, you'll likely need to re-run  the same commands many times, with slight
changes, to get a better understanding of the documentation.
This implies two things:

   1. For every group of commands you run, you need to find the opposite
      commands which will undo all their effects. You need it so that the second
      time you run your commands, their effects won't be affected by the
      previous run.

      Example: the opposite of `update-alternatives --install ...` is
      `update-alternatives --remove all ...`.

   2. You need to write a temporary script to avoid having to run the same long
      commands over and over. With it,  all you'll have to  do is edit a  script
      to add your  change and re-run it. It's much quicker to change a word in
      a command, then to retype several long commands just for one little
      change.

# Design

When  you  encounter  the  same   problem  regularly,  but  it's  insufficiently
specified, you need to develop a design.

The purpose of the design is to  answer all the implicit questions not mentioned
in the original problem.

Example:

        Problem:

write some code to show the snippets available in the current buffer.

        Implicit questions:

   - Where should I display the info (horizontal/vertical split, tabpage)?
   - Should I use syntax highlighting?
   - If so, how to implement it (syntax plugin vs `matchadd()`) and which colors should I use?
   - Should I use a preview window?
   - Which buffer-local options should I set?
   - Which buffer-local mappings should I install?
   ...


Without a design, you'll:

   - lose time answering those questions over and over again

   - forget to answer some of them

   - create an inconsistent environment
     (because every time, you'll solve the problem in a slightly different way)

   - have a hard time to refactor and improve your solutions
     (because they'll all be slightly different)

##
# Reference

[1]: https://en.wikipedia.org/wiki/Higher-order_thinking
[2]: https://fr.wikipedia.org/wiki/Thalamus#/media/File:Thalamus_small.gif
[3]: https://fr.wikipedia.org/wiki/Amygdale_(cerveau)#/media/File:Amygdala.gif
[4]: https://fr.wikipedia.org/wiki/Hippocampe_(cerveau)#/media/File:Hippocampus.gif
