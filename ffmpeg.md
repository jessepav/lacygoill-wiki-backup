# Information
## How to get the list of streams contained in a video?

        $ ffprobe <file> |& grep -i stream

Example output:

        Stream #0:0(eng): Video: h264 (High), yuv420p(tv, bt709), 1280x720 [SAR 1:1 DAR 16:9], 23.98 fps ...
        Stream #0:1(eng): Audio: ac3, 48000 Hz, 5.1(side), fltp, 448 kb/s (default)
        Stream #0:2(eng): Audio: ac3, 48000 Hz, stereo, fltp, 192 kb/s
        Stream #0:3(eng): Subtitle: subrip (default)

In the  `#x:y` identifiers,  `x` match the  number of the  input file  passed to
`ffprobe`, while `y` match the number of the stream in the file.

You can use `x`  and `y` when you want `ffmpeg` to target  a specific stream via
the `-map` option.

---

Warning:
If you use  `a`, `s`, `v` to specify  the kind of the stream, you  can't use the
number `y` as reported by `ffprobe`:

        ┌────────────┬────────────────────────────────────────────────┐
        │ -map 0:s:0 │ first subtitle stream of the first input file  │
        ├────────────┼────────────────────────────────────────────────┤
        │ -map 0:0   │ stream whose id is `0` in the first input file │
        └────────────┴────────────────────────────────────────────────┘

## How to get the original title of a video file (before we renamed it)?  (2)

    $ ffprobe <file> |& grep title
                     ├┘
                     └ bashism ⇔ `2>&1 |`

I think the reason  why you need to redirect the standard error  to the pipe, is
because `ffprobe` uses its standard error for its output.

##
# Video
##
# Audio
##
# Subtitles
## How to list all the kind of subtitles supported by `ffmpeg`?

        $ ffmpeg -codecs | grep subtitle

## How to convert a `.ass` subtitle to a `.srt` one?

        $ ffmpeg -i file.ass file.srt

##
# Muxing
## How to mux `file.mp4`, `sub.en.srt` and `sub.fr.srt` into `file.mkv`?

        $ ffmpeg -i file.mp4 \
                 -i sub.en.srt \
                 -i sub.fr.srt \
                 -map 0 \
                 -map 1 \
                 -map 2 \
                 -c copy \
                 -metadata:s:s:0 language=en \
                 -metadata:s:s:1 language=fr \
                 file.mkv

Source:

        https://superuser.com/a/958711/913143

---

Note that  the conversion from `mp4`  to `mkv` seems necessary,  because a `mp4`
container doesn't support `.srt` files.
Otherwise, you would have to re-encode the subtitles:

        https://stackoverflow.com/a/46522467/9780968

Also, there should  be no quality loss  during the conversion thanks  to the `-c
copy` argument passed to `ffmpeg`.

##
# COMMANDES

            ┌─ fmt (input/output); force input or output file format
            │
            │        ┌─ input file url
            │        │
    ffmpeg -f pulse -i default out.wav

            Enregistrer le son qui sort du pc.

            Au préalable, il faut lancer le mixer du serveur pulse (`pavucontrol`), sélectionner l'onglet
            'recording', et dans le menu déroulant sélectionner 'Monitor of Built-in Audio Analog Sound'.
            Pas besoin de le refaire à chaque fois qu'on enregistre du son.  Une fois suffit, car ffmpeg
            mémorisera ce réglage.



            TODO:

            Finir de lire:
            http://blog.pkh.me/p/21-high-quality-gif-with-ffmpeg.html


                    ┌──────────── niveau de verbosité 'warning'
                    │
                    │     ┌───── commence la conversion à partir de 5s (Seek Start)
                    │     │
                    │     │     ┌ limiter à 10s la durée des données lues
            ┌───────┤  ┌──┤  ┌──┤
    ffmpeg -v warning -ss 5 -t 10 -i input.mkv -vf scale=900:-1 -y out.gif
                                                └─────────────┤  │
           filtre le flux vidéo avec `scale` (nom du filtre)  ┘  │
           pour redimensionner la largeur du fichier de sortie   │
           à 900 pixels,                                         │
           et la hauteur de sorte que le ratio d'origine soit    │
           conservé (-1)                                         │
                                                                 │
                    écrase le fichier de sortie s'il existe déjà ┘
                    sans demande de confirmation;
                    très pratique qd on fait des tests


                                     NOTE:

            L'ordre des options est important.

            `-ss` et `-t` sont des options propres à un fichier d'entrée.  Elles doivent donc se trouver avant `-i`.
            `-vf` est une option propre à un fichier de sortie.  Elle doit donc se trouver après `-i`.


                                     NOTE:

        `-vf` est un alias pour `-filter:v`.
                                         │
                                         └─ spécificateur de flux (stream_specifier)

            Un fichier peut contenir plusieurs types de flux:

                    - vidéo
                    - audio
                    - sous-titres
                    - pièce-jointe

            … et plusieurs flux d'un même type.
            Pour indiquer à un filtre sur quel flux il doit opérer, il faut donc utiliser un spécificateur de flux.


                                     NOTE:

            Pour plus d'infos sur:

                    - les filtres applicables à un flux, lire `man ffmpeg-filters`
                    - le filtre `scaler` en particulier, lire `man ffmpeg-scaler`


    -gifflags -transdiff

            Désactive l'option `transdiff`.

            Ceci a pour effet de désactiver un mécanisme de transparence qui est activé par défaut
            (`-gifflags +transdiff`).
            Le désactiver est recommendé pour une image contenant beaucoup de mouvement ou de changements
            de couleurs, mais cela fait augmenter le poids de l'image.


    -filters

            Liste tous les filtres supportés.


    -vf scale=900:-1:sws_dither=ed

            Demande au filtre scaler d'appliquer au flux vidéo l'algo de tramage `ed` (Error Diffusion).

            L'option `sws_dither`  permet d'améliorer la qualité  d'une image GIF, en  gérant les
            erreurs de quantification via un algo déterminé.


                                     NOTE:

            Modifie aussi la largeur du flux vidéo à 900 pixels, en conservant l'aspect ratio.


                                     NOTE:

            `sws` signifie probablement `SoftWare Scaler`.
            Le terme software fait référence au fait que le filtrage est géré par le cpu, et pas par
            un hardware externe tel qu'une carte graphique.


                                     NOTE:

            Attention, ça flingue l'algo de compression GIF, et on obtient donc une image au poids démultiplié.


                                     NOTE:

            Il existe d'autres algos de tramage, entres autres `bayer`.
            `bayer` a l'avantage d'être prévisible et rapide (bonne compression → petite taille de fichier).
            Toutefois, ce n'est pas le plus joli, et il est reconnaissable à un pattern hachuré de taille 8x8.


   scale

       Scale (resize) the input video.

       The scale  filter forces  the output display  aspect ratio to  be the  same of the  input, by
       changing the output sample aspect ratio.

       If the  input image format  is different from  the format requested  by the next  filter, the
       scale filter will convert the input to the requested format.

       Options

       The filter accepts the  following options, or any of the options  supported by the libswscale
       scaler.

       See the ffmpeg-scaler manual for the complete list of scaler options.

       width, w
       height, h

           Set the output video dimension expression.  Default value is the input dimension.

           If the value is 0, the input width is used for the output.

           If one of the values  is -1, the scale filter will use a  value that maintains the aspect
           ratio of the input image, calculated from  the other specified dimension.  If both of them
           are -1, the input size is used

           If one  of the values  is -n  with n >  1, the scale  filter will  also use a  value that
           maintains  the aspect  ratio of  the  input image,  calculated from  the other  specified
           dimension.  After that  it will,  however,  make sure  that the  calculated dimension  is
           divisible by n and adjust the value if necessary.

           See below for the list of accepted constants for use in the dimension expression.

       flags

           Set  libswscale scaling  flags.  See  the ffmpeg-scaler  manual for  the complete  list of
           values.  If not explicitly specified the filter applies the default flags.

# DOCUMENTATION

https://www.ostechnix.com/20-ffmpeg-commands-beginners/


HOWTO: Proper Screencasting on Linux :

        https://ubuntuforums.org/showthread.php?p=8746719#post8746719


        https://en.wikipedia.org/wiki/Standard_(warez)#High_definition_video

        How to make youtube videos on the command-line:
        https://www.youtube.com/watch?v=sIs0-6F08Us


https://trac.ffmpeg.org/wiki ; lire les pages des sections suivantes:

        Encoding
        Hardware acceleration
        Grabbing / Capturing
        Streaming
        Filtering
        Images / Frames
        Subtitles
        Miscellaneous

# VOCA

    banding

            Le colour banding est un problème de représentation de couleur inexacte.
            Il se traduit par des changements brusques entre des nuances (teinte/luminosité)
            de la même couleur.
            Particulièrement visible pour de faibles valeurs de bpp.

            https://upload.wikimedia.org/wikipedia/commons/9/9a/Colour_banding_example01.png


    bpp
    bpc

            bits per pixel
            bits per channel/color/component

            La couleur d'un pixel résulte d'un mélange entre 3 couleurs de rouge, vert et bleu (RGB).
            Chacune de ces couleurs est parfois appelée canal ou composant.


    erreur de quantification

            Le format GIF est limité à une palette de 256 couleurs.
            De plus, par défaut, ffmpeg utilise une palette _générique_ qui tente de couvrir tout l'espace
            des couleurs.

            Pour chauqe pixel, il existe donc une différence entre la couleur choisie au sein de la
            palette et la couleur d'origine: on parle d'erreur de quantification.


    profondeur des couleurs

            Nombre de bits utilisés pour représenter la couleur d'un pixel dans une image.
            Elle s'exprime en bpp.

            Plus la profondeur de couleurs est élevée, plus l'image est fidèle à la scène capturée:

                    https://en.wikipedia.org/wiki/Color_depth


                                     NOTE:

            Qd la profondeur des couleurs d'une image est de 8 bpp, 3 sont alloués au rouge, 3 au vert
            et seulement 2 au bleu.  En effet, l'oeil humain est moins sensible au bleu (2/3 des récepteurs
            de l'oeil traitent des longueurs d'ondes plus grandes).
            Plus généralement, l'oeil distingue d'avantage de nuances de certaines couleurs suivant
            l'ordre de priorité suivante:

                    vert > rouge > bleu


    tramage / dithering

            Technique  d'amélioration   d'image  numérique   dont  le   but  est
            d'empêcher les motifs tels que le banding.

            La plupart  des algos de tramage  sont basés sur la  répartition des
            erreurs de quantification  sur les pixels voisins:  chaque erreur de
            quantification sur un pixel est  répartie sur l'ensemble de l'image,
            produisant un effet de “fourmillement“.

