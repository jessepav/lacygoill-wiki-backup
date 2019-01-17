
    https://github.com/akhodakivskiy/VimFx/issues/860

            VimFx devrait mourir d'ici la fin de 2017 (novembre), car Firefox ne supportera plus
            qu'un seul type d'extension: les WebExtensions.

            L'auteur de VimFx ne pense pas pouvoir convertir VimFx en WebExtension.
            Il suggère de garder un oeil sur Vimium (addon Chrome) qui devrait bientot supporter Firefox.

            Autres alternatives possibles:

                    - pale moon:   https://linux.palemoon.org/ (fork de firefox)
                    - qutebrowser: https://github.com/qutebrowser/qutebrowser
                    - uzbl:        https://www.uzbl.org/


    https://github.com/philc/vimium/issues/2425

            Discussion autour du support de Firefox par Vimium.


    https://github.com/akhodakivskiy/VimFx/blob/master/documentation/commands.md

    ┌──────────┬───────────────────────────────────────────────────────────────────────────────────────┐
    │ , ;      │ naviguer dans la jumplist (originellement g[, g])                                     │
    ├──────────┼───────────────────────────────────────────────────────────────────────────────────────┤
    │ af       │ ouvrir tous les liens de la page dans de nouveaux onglets                             │
    ├──────────┼───────────────────────────────────────────────────────────────────────────────────────┤
    │ f        │ ouvrir un lien dans l'onglet courant                                                  │
    │          │                                                                                       │
    │          │ si on s'est trompé car on voulait taper `F` ou `et`, on peut appuyer sur `C-<indice>` │
    │          │ ou `<M-indice>` pour ouvrir le lien dans un nouvel onglet sans lui donner le focus,   │
    │          │ ou en lui donnant le focus                                                            │
    │          │                                                                                       │
    │          │ si VimFx ne propose pas d'indice pour l'élément qui nous intéresse, on peut appuyer   │
    │          │ sur `C-backspace` pour forcer la génération d'indices à un max d'éléments             │
    ├──────────┼───────────────────────────────────────────────────────────────────────────────────────┤
    │ F   et   │ ouvrir un lien dans un nouvel onglet, sans lui donner/en lui donnant le focus         │
    ├──────────┼───────────────────────────────────────────────────────────────────────────────────────┤
    │ 3f       │ cliquer sur 3 liens, les 2 premiers liens sont ouverts dans d'autres onglets          │
    │          │                                                                                       │
    │          │ économise des touches car pas besoin de répéter `F` à chaque fois                     │
    │          │ fonctionne aussi avec des cases à cocher                                              │
    │          │                                                                                       │
    │ 3F       │ idem, mais le 3e est ouvert dans un nouvel onglet, sans lui donner le focus           │
    │ 3et      │ idem, mais on lui donne le focus                                                      │
    │          │                                                                                       │
    │          │ si on s'aperçoit qu'on veut ouvrir un 4e lien alors qu'on a déjà commencé à ouvrir    │
    │          │ des liens, on peut appuyer sur `Up` pour incrémenter le count a posteriori            │
    ├──────────┼───────────────────────────────────────────────────────────────────────────────────────┤
    │ et ew ep │ ouvrir un lien dans un nouvel onglet / fenêtre / fenêtre privée                       │
    ├──────────┼───────────────────────────────────────────────────────────────────────────────────────┤
    │ eb       │ cliquer sur un élément du Browser (ex: bouton dans toolbar)                           │
    ├──────────┼───────────────────────────────────────────────────────────────────────────────────────┤
    │ ec       │ ouvrir le menu Contextuel sur un élément de la page (ex: image)                       │
    ├──────────┼───────────────────────────────────────────────────────────────────────────────────────┤
    │ ef       │ donner le Focus à un élément de la page                                               │
    ├──────────┼───────────────────────────────────────────────────────────────────────────────────────┤
    │ yf       │ copier un lien                                                                        │
    ├──────────┼───────────────────────────────────────────────────────────────────────────────────────┤
    │ 2g^ 3g$  │ donner le focus au 2e onglet en partant du début, ou au 3e en partant de la fin       │
    ├──────────┼───────────────────────────────────────────────────────────────────────────────────────┤
    │ gi       │ donner le focus au dernier champ l'ayant reçu                                         │
    │          │                                                                                       │
    │ 1gi 3gi  │ "               au 1er / 3e champ                                                     │
    ├──────────┼───────────────────────────────────────────────────────────────────────────────────────┤
    │ gJ gK    │ déplacer l'onglet courant                                                             │
    ├──────────┼───────────────────────────────────────────────────────────────────────────────────────┤
    │ gu       │ remonte d'un niveau dans la hiérarchie de l'url (supprime son dernier composant)      │
    ├──────────┼───────────────────────────────────────────────────────────────────────────────────────┤
    │ i        │ ignore mode                                                                           │
    │          │                                                                                       │
    │ S-escape │ exit ignore mode                                                                      │
    ├──────────┼───────────────────────────────────────────────────────────────────────────────────────┤
    │ g/       │ chercher une url                                                                      │
    ├──────────┼───────────────────────────────────────────────────────────────────────────────────────┤
    │ '/       │ revenir à l'endroit où on se trouvait avant la dernière recherche                     │
    ├──────────┼───────────────────────────────────────────────────────────────────────────────────────┤
    │ v        │ passer en mode caret                                                                  │
    │          │                                                                                       │
    │          │ en mode caret, on peut utiliser les mouvements 0, ^, $, h, j, k, l, w, b              │
    │          │ on peut aussi alterner entre les limites de la sélection via `o`                      │
    ├──────────┼───────────────────────────────────────────────────────────────────────────────────────┤
    │ av       │ sélectionner visuellement un bout de texte de la page                                 │
    ├──────────┼───────────────────────────────────────────────────────────────────────────────────────┤
    │ yv       │ copier un bout de texte de la page                                                    │
    ├──────────┼───────────────────────────────────────────────────────────────────────────────────────┤
    │ C-space  │ alterner entre 2 indices qd ils sont partiellement superposés                         │
    │ S-space  │                                                                                       │
    └──────────┴───────────────────────────────────────────────────────────────────────────────────────┘


                                     NOTE:

Les modes sont locaux à un onglet, et non globaux.
On peut donc passer en mode ignore dans un onglet, tout en continuant à utiliser VimFx dans les autres.


                                     NOTE:

Qd plusieurs éléments cliquables sont proches les uns  des autres, il est difficile de cliquer sur
l'un d'eux au milieu. Pour éliminer les éléments indésirables, on peut taper une partie du texte
contenu par  celui qui  nous intéresse.  Après chaque  frappe, VimFx  met à  jour et  réduit les
éléments cliquables.  En revanche, il ne  faut jamais taper  un caractère qui est  utilisé comme
indice d'un autre élément, même s'il est présent au sein du texte de l'élément intéressant.


                                     FIXME:

Il semble que plusieurs commandes censées accepter un count, ne le font pas.
Ex, `5d` devrait fermer 5 onglets. `3gJ` devrait déplacer l'onglet courant après le 3e qui suit. Etc.
