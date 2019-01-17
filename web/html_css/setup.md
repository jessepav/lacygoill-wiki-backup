# How to set up a local testing server?
## make sure `python` is installed

        $ python -V

## enter your project

        $ cd /path/to/project

## choose a port number for your server

Without  providing  a  port  number, the  python  module  `SimpleHTTPServer`  or
`http.server` will choose 8000.
Make sure it's free:

        $ netstat -tuplen

## start the server

                                      ┌ optional port number
                                      │
        $ python -m SimpleHTTPServer [1234]
Or:
        $ python3 -m http.server [1234]

## visit your local website

        http://localhost:8000

## create a layout for your project

        $ mkdir -p ./{images,styles,scripts}
                      │      │      │
                      │      │      └ javascript
                      │      └ css
                      └ images

It should produce the following layout:

        .
        ├── images
        ├── index.html
        ├── scripts
        └── styles
            └── basic.css

            3 directories, 2 files

## create an index for your site

        $ cat index.html

                <!DOCTYPE html>
                <html>
                <head>
                  <meta charset="utf-8">
                  <title>This an index page</title>
                  <link rel="stylesheet" href="/styles/basic.css">
                </head>
                <body>
                  <p>This is my own custom index</p>
                </body>
                </html>

You can get this code by pressing:

        ! C-g ,

Then, insert a title inside the `<title>` tag.
Below, insert a `<link>` tag, by pressing:    link C-g ,
Insert the  path to  the stylesheet, relative  to the root  of the  project (ex:
`/styles/basic.css`).
You'll use it to set the style of the index page.

Insert some text in the paragraph in the body of the page.

## set the style of the index page

        $ cat styles/basic.css

                body {
                    font-family: sans-serif;
                }

## further reading

    https://developer.mozilla.org/en-US/docs/Learn/Common_questions/set_up_a_local_testing_server

