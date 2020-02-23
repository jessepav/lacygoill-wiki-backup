# Bugs?
## cannot use a bar

    def! Func()
        let x = 0 | let y = 0
    enddef
    call Func()
    E488: Trailing characters:  | let y = 0~

---

Source this:

    def! Func()
        let x = 123
        redraw! | echo x
    enddef
    call Func()
    Error detected while processing function Func:~
    line    1:~
    E121: Undefined variable: x~

Why `E121` and not `E488` like before?

