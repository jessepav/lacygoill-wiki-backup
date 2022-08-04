# m
## mnemonic

Symbolic  name for  an opcode;  useful for  the programmer  when reading/writing
assembly code.

##
# o
## opcode

Binary number encoding a mnemonic in executable machine code.

##
# r
## radare2(1)

Set of libraries, tools and plugins to ease reverse engineering tasks.

<https://github.com/radareorg/radare2>

## rax2(1)

Utility which comes with radare2, and can convert values between different bases
(notably binary, octal, hexadecimal).

##
## registers
### rax

64-bit, "long" size register.

---

There are 3 other similar registers:

   - `rbx`
   - `rcx`
   - `rdx`

And each of them is associated to the same family of registers:

   - `rbx`, `ebx`, `bx`, `bh`, `bl`
   - `rcx`, `ecx`, `cx`, `ch`, `cl`
   - `rdx`, `edx`, `dx`, `dh`, `dl`

### eax

32-bit, "int" size register.  It's the 32 low bits of `rax`.

### ax

16-bit, "short" size register.  It's the 16 low bits of `eax`.

### ah

8 bit, "char" size register.  It's the 8 *high* bits of the `ax` register.

### al

8 bit, "char" size register.  It's the 8 *low* bits of the `ax` register.

---

`ax` is:

   - partitioned into `ah` and `al`
   - contained inside `eax`, which itself is contained inside `rax`

Which gives this diagram:

      ┌──────────────────────────────────────────────────────────────────┐
      │                 ┌──────────────────────────────────────────────┐ │
      │                 │                ┌───────────────────────────┐ │ │
      │                 │                │        ax: 16-bit         │ │ │
      │                 │                │ ┌───────────┬───────────┐ │ │ │
      │  rax: 64-bit    │ eax: 32-bit    │ │ ah: 8-bit │ al: 8-bit │ │ │ │
      │                 │                │ └───────────┴───────────┘ │ │ │
      │                 │                └───────────────────────────┘ │ │
      │                 └──────────────────────────────────────────────┘ │
      └──────────────────────────────────────────────────────────────────┘

###
### `rip`

The 64-bit, long size, "Instruction Pointer" register.

At any given time, `rip` points to the next instruction to execute.
The CPU needs this information to know what to execute next.

And as soon  as it has executed  this instruction, `rip` is updated  so that the
process can go on.

### `eip`

The 32-bit, int size, "Instruction Pointer" register.  It's the 32 low bits of `rip`.

### `ip`

The 16-bit, "short" size, "Instruction Pointer" register.  It's the 16 low bits of `eip`.

###
### `rsp`

The 64-bit, long size, "Stack Pointer" register.

At any given time, `rsp` points to the value at the top of the stack.
The CPU needs this information to know:

   - where to push a new value on top of the stack
   - where to find the value to pop out of the stack

And as soon as  the CPU has pushed/popped a value, `rsp` is  updated so that the
process can go on.

### `esp`

The 32-bit, int size, "Stack Pointer" register.  It's the 32 low bits of `rsp`.

### `sp`

The 16-bit, "short" size, "Stack Pointer" register.  It's the 16 low bits of `esp`.

##
# s
## strace(1)

Utility which can  log the system calls  started by a given process,  as well as
the signals it receives.

---

A number printed  after a system call and  an equal sign is the  return value of
that system call.  For example:

    openat(AT_FDCWD, "/etc/ld.so.cache", O_RDONLY|O_CLOEXEC) = 3
                                                               ^

Here, `3` is the return value of the `openat(2)` system call.

##
# x
## xref

Abbreviation of "cross-reference".

In  some Linux  tools (like  `radare2(1)`), `XREF`  is written  to express  that
some  instruction/data  is  (cross-)referenced  from one  or  several  different
location(s).

<https://en.wikipedia.org/wiki/Cross-reference>
