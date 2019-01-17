https://github.com/brookhong/Surfingkeys
https://github.com/knsv/mermaid


    Unreadable input fields with dark GTK+ themes
    https://wiki.archlinux.org/index.php/Firefox#Unreadable_input_fields_with_dark_GTK.2B_themes

            Solution 1:

            Créer le fichier `~/.mozilla/firefox/xxxxxxxx.default/chrome/userContent.css`, et y écrire:

                    input:not(.urlbar-input):not(.textbox-input):not(.form-control):not([type='checkbox']) {
                        -moz-appearance: none !important;
                        background-color: white;
                        color: black;
                    }

                    #downloads-indicator-counter {
                        color: white;
                    }

                    textarea {
                        -moz-appearance: none !important;
                        background-color: white;
                        color: black;
                    }

                    select {
                        -moz-appearance: none !important;
                        background-color: white;
                        color: black;
                    }

            Solution 2:

            Installer l'addon suivant:
            https://addons.mozilla.org/en-US/firefox/addon/text-contrast-for-dark-themes/

            Si on installe l'addon `Text Contrast for Dark Themes`, et qu'il introduit du lag sur YouTube
            ou Reddit, cliquer sur son icône, et dans le menu qui apparaît cliquer sur `Toggle standard colors`.


    about:config > zoom.minPercent > change value from 30 to 150 (or whatever value)

            Solution pour zoomer automatiquement toutes les pages web.

            Pb: une fois la valeur de `zoom.minPercent` changée, on ne peut plus réduire le zoom
            en-dessous de cette dernière.


    ┌────────────────────┬──────────────────────────────────────────────┐
    │     raccourci      │                   fonction                   │
    ├────────────────────┼──────────────────────────────────────────────┤
    │ C-S-t              │ restaure un onglet fermé                     │
    │                    │                                              │
    │ C-S-n              │ restaure une fenêtre fermée                  │
    │                    │                                              │
    │ C-Tab    C-S-Tab   │ avance / recule d'un onglet                  │
    │                    │                                              │
    │ S-Space            │ scroll en arrière dans la page               │
    │                    │                                              │
    │ S-Tab              │ sélectionne l'élément précédent dans la page │
    │                    │                                              │
    │ C-S-p              │ lance une session de navigation privée       │
    │                    │                                              │
    │ S-Backspace/Scroll │ navigue dans l'historique de l'onglet        │
    │                    │                                              │
    │ S-Click            │ ouvre le lien dans un nouvel onglet          │
    │                    │                                              │
    │ C-S-r              │ recharge la page (sans utiliser le cache)    │
    └────────────────────┴──────────────────────────────────────────────┘

