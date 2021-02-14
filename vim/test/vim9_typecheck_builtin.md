Let's write a shell and Vim script to  test how a given Vim function handles all
possible types of values.

We need to test these functions:

    vim9script

    var IsCustomFunc: func = (v) => v[0] !~ '[a-z]'
    var AcceptArg: func = (v) => v[-1] == '('
    var NoAutoload: func = (v) => v !~ '#'

    new

    getcompletion('*', 'function')
        ->filter((_, v) => !IsCustomFunc(v) && AcceptArg(v) && NoAutoload(v))
        ->setline(1)

Let's start with the first ten ones:

    abs( ✔
    acos( ?
    add( ?
    and( ?
    append( ?
    appendbufline( ?
    argc( ?
    arglistid( ?
    argv( ?
    asin( ?

---

Source this script to generate snippets for the `abs()` function:

    vim9script
    const TESTDIR: string = '/tmp/test'
    delete(TESTDIR, 'rf')
    def GenerateSnippets(funcname: string)
        mkdir(TESTDIR .. '/def/' .. funcname, 'p')
        var lines: list<string>
        for value in [
          123,
          1.23,
          0z1234,
          '''string''',
          true,
          v:none,
          [0],
          {key: 'val'},
          'function(''len'')',
          'job_start('':'')',
          'job_start('':'')->job_getchannel()',
          ]
            lines = [
                'vim9script',
                printf('echom "%s"', 'in def function'),
                printf('echom "%s(%s) = "', funcname, value),
                'echom " "'
                'def Func()',
                printf('    echom %s(%s)', funcname, value),
                'enddef',
                'Func()'
                ]
            var scriptname: string
            if value->typename() == 'string' && value != '"string"'
                scriptname = value =~ '_getchannel()$'
                    ?     'channel'
                    : value =~ '^job'
                    ?     'job'
                    : value =~ '^function('
                    ?     'function'
                    :     typename(value)
            else
                scriptname = value->typename()
            endif
            writefile(lines, printf(TESTDIR .. '/def/%s/%s.vim',
                funcname,
                scriptname,
                ))
            lines = [
                'vim9script',
                printf('echom "%s"', 'at script level'),
                printf('echom "%s(%s) = "', funcname, value),
                'echom " "'
                printf('echom %s(%s)', funcname, value),
                ]
            mkdir(TESTDIR .. '/script/' .. funcname, 'p')
            writefile(lines, printf(TESTDIR .. '/script/%s/%s.vim',
                funcname,
                scriptname,
                ))
        endfor
    enddef
    GenerateSnippets('abs')
    qa!

Run this shell command to test each snippet:

    $ for f in /tmp/test/**/*.vim; do vim -Nu NONE -S "$f"; done
