# b
## branch

A conditional  GOTO, predicated on `ZF`,  and implemented via the  `je` or `jne`
instruction.

Example:

    je 0x1234

This jumps  to the address `0x1234`,  but only if the  last arithmetic operation
resulted in zero.

---

The test uses zero, because a simple  way to test the equality between 2 numbers
is to test whether their difference is zero.

So this pseudo-code:

    if 5 == 5

Could be written in assembly like this:

    mov eax, 0x5
    mov ebx, 0x5
    sub eax, ebx

    je 0x1234

The first instructions simply compute the difference between 5 and 5.
Since the difference is zero, `ZF` will be set.
And since  `je` is predicated  on `ZF` being set,  it will be  executed, storing
`0x1234` into `rip`, which in turn  will change the next instruction executed by
the CPU.

OTOH, in this code, `je` will not jump (i.e. it will leave `rip` unchanged):

    mov eax, 0x6
    mov ebx, 0x5
    sub eax, ebx

    je 0x1234

Because the difference between 6 and 5 is not 0.

---

`je` stands for "Jumps if Equal".
`jne` does the opposite of `je`; its acronym stands for "Jumps if Not Equal".

##
# c
## 64-bit CPU

A CPU capable of  transferring 64 bits of data per clock cycle.   64 bits is the
amount of  information it can process  each time it performs  an operation.  The
difference  between a  16-bit, 32-bit,  and 64-bit  CPU mainly  matters wrt  the
amount of RAM which can be addressed by the OS.

##
# f
## status flags

Most  operations on  registers like  additions  and subtractions  have the  side
effect  of  altering boolean  flags  which  are  set  into the  32-bit  `eflags`
register.  Each bit inside this register encodes a different flag.

- <https://en.wikipedia.org/wiki/FLAGS_register#FLAGS>
- <https://en.wikibooks.org/wiki/X86_Assembly/X86_Architecture#EFLAGS_Register>

### `OF`

The overflow  flag.  It's  set when  an arithmetic overflow  has occurred  in an
operation.

<https://en.wikipedia.org/wiki/Overflow_flag>

### `PF`

The parity flag.  It's set when the  least significant byte of the result of the
last operation had an even number of bits set to 1.

<https://en.wikipedia.org/wiki/Parity_flag>

### `SF`

The sign flag.  It's set when the  result of the last mathematical operation was
negative, which is why it's also often called the "negative flag".

Technically, it's set when the last operation produced a value in which the most
significant  bit  (the left  most  bit)  was set.   But  in  a two's  complement
interpretation of  the result (which  is the most common  interpretation?), that
happens only if the result was negative.

<https://en.wikipedia.org/wiki/Negative_flag>

### `ZF`

The zero flag.  It's set when the result of the last mathematical operation was 0.

Example:

    mov eax, 0x5
    add eax, 0x3

Here we've added 3 to 5, which gives us 8.
8 is different than zero, so inside the flag register, `ZF` is reset (0).

Next, we execute these instructions:

    mov ebx, 0x8
    sub eax, ebx

Here, we subtract the `ebx` register from the `eax` one.
Both held the same value (8), so the result is 0.
As a result, inside the flag register, `ZF` is set (1).

<https://en.wikipedia.org/wiki/Zero_flag>

##
# g
## GPR

General Purpose Register

A GPR can hold anything: a value (e.g. `123`) *or* an address (e.g. `0x456`).

`rax` is a GPR.
`rip` (instruction  pointer) and `eflags`  are not  GPRs, because they  can only
hold resp. an address and a list of flags.

##
# j
## jump

An unconditional GOTO implemented via the `jmp` instruction.
The latter stores a new address into `rip`.

Example:

    jmp 0x1234

This stores `0x1234` into `rip`.
As a  result, the  CPU will next  execute whatever instruction  is held  at this
address, forgetting whatever address was originally held by `rip`.

This `jmp` instruction is a bit similar to this `mov`:

    mov ip, 0x1234

##
# k
## keygen

Computer  program that  generates  a product  licensing key,  such  as a  serial
number, necessary to activate for use of a software application.

It can be  distributed legitimately (e.g. by a software  vendor to an enterprise
which bought licenses in bulk), or illegitimately (typically by crackers).

Stands for "KEY GENerator".

##
# m
## memory location

The address of a byte in the memory accessible to the CPU (which includes the RAM).

Example:

    mov rax, [0x123]
              ^----^

Here, `0x123` is a memory location.
Notice the presence  of surrounding brackets; without, `0x123` would  be just an
immediate value.

##
## mnemonic

Symbolic  name for  an opcode;  useful for  the programmer  when reading/writing
assembly code.

Names of mnemonics depend on the CPU architecture.

### `add`

Performs this operation:

    DEST ← DEST + SRC;

Adds  the destination  operand (first  operand)  to the  source operand  (second
operand), and then stores the result in the destination operand.

The  destination operand  can be  a register  or a  memory location;  the source
operand can be  an immediate value, a register, or  a memory location.  However,
two memory operands cannot be used  in one instruction.  When an immediate value
is used  as an  operand, it is  sign-extended to the  length of  the destination
operand format.

<https://www.felixcloutier.com/x86/add>

### `call`

Pushes the address of the next instruction (aka the "return address") on the top
of the stack.  Then, stores the address of the first instruction of the function
specified  as operand  (aka the  "call  address") into  `rip`, so  that the  CPU
branches to the function's code in the next cycle.

<https://www.felixcloutier.com/x86/call>

### `cmp`

Performs this operation:

    temp ← SRC1 − SignExtend(SRC2);
    ModifyStatusFlags;

Compares the first operand with the second  operand and sets the status flags in
the `eflags` register according to the  results.  The comparison is performed by
subtracting  the second  operand from  the first  operand and  then setting  the
status flags  in the same  manner as the  `sub` instruction.  When  an immediate
value is  used as an  operand, it  is sign-extended to  the length of  the first
operand.

<https://www.felixcloutier.com/x86/cmp>

### `je`

Jumps  to target  instruction specified  by destination  operand, iff  the first
operand in the previous mathematical operation was equal to the second operand.

Technically,  `je` jumps  iff  `ZF`  is set,  i.e.  the  previous operation  has
produced  the result  zero.  Usually,  the previous  operation is  a subtraction
(e.g. happens with `cmp`), and the result of a subtraction is zero iff the first
operand is equal to the second operand.

<https://www.felixcloutier.com/x86/jcc>

### `jl`

Jumps  to target  instruction specified  by destination  operand, iff  the first
operand  in  the previous  mathematical  operation  was  lower than  the  second
operand.

Technically, `jl` jumps iff `SF` is  different than `OF`.  Assuming that `OF` is
not set (it should not be  in normal circumstances), the condition is equivalent
to `SF` being  set, i.e. the previous operation has  produced a negative result.
Usually, the previous operation is a  subtraction (e.g. happens with `cmp`), and
a  subtraction is  negative  iff the  first  operand is  lower  than the  second
operand.

<https://www.felixcloutier.com/x86/jcc>

### `jmp`

Unconditionally transfers  program control to  the instruction whose  address is
given as operand.

<https://www.felixcloutier.com/x86/jmp>

### `jne`

Jumps  to target  instruction specified  by destination  operand, iff  the first
operand in  the previous  mathematical operation was  different than  the second
operand.

For more info, see the `je` instruction, whose meaning is the opposite.

### `mov`

Copies the  second operand  (source operand) to  the first  operand (destination
operand).  The source operand can be  an immediate value, GPR, segment register,
or memory location; the destination register  can be a GPR, segment register, or
memory location.  Both  operands must be the  same size, which can be  a byte, a
word, a doubleword, or a quadword.

<https://www.felixcloutier.com/x86/mov>

### `movsx`

Performs this operation:

    DEST ← SignExtend(SRC);

Copies the contents  of the source operand (register or  memory location) to the
destination operand (register), and sign extends the value to 16 or 32 bits.

The size of the converted value depends on the operand-size attribute.
In 64-bit mode, the instruction's default operation size is 32 bits.

- <https://www.felixcloutier.com/x86/movsx:movsxd>
- <https://en.wikipedia.org/wiki/Sign_extension>

### `movsxd`

Same as `movsx`.
The only difference is that `movxsd` supports different sizes for the operands.

`movsx` supports these transfers:

     8 → 16
     8 → 32
     8 → 64
    16 → 32
    16 → 64

`movsxd` supports these ones:

    16 → 16
    32 → 32
    32 → 64

### `movzx`

Performs this operation:

    DEST ← ZeroExtend(SRC);

Copies the contents of the source operand (register or memory location) into the
destination operand  (register), and zero  extends the  value.  The size  of the
converted value depends on the operand-size attribute.

<https://www.felixcloutier.com/x86/movzx>

### `pop`

Loads the  value from the top  of the stack  to the location specified  with the
destination operand,  and then  increments the  stack pointer.   The destination
operand can be a GPR, memory location, or segment register.

<https://www.felixcloutier.com/x86/pop>

### `push`

Decrements the stack  pointer and then stores  the source operand on  the top of
the stack.

<https://www.felixcloutier.com/x86/push>

### `ret`

Pops the  address out  of the top  of the  stack, and stores  it into  `rip`, to
transfer program control right after the function call.

<https://www.felixcloutier.com/x86/ret>

### `sub`

Performs this operation:

    DEST ← DEST - SRC;

Subtracts  the source  operand  (second operand)  from  the destination  operand
(first operand) and then stores the result in the destination operand.

Among other flags, `OF`, `SF`, and `ZF` are set according to the result.

<https://www.felixcloutier.com/x86/sub>

### `test`

Computes the bitwise logical AND of  the first operand and second operands, then
sets the `SF`, `ZF`, and `PF` status  flags according to the result.  The latter
is discarded.

<https://www.felixcloutier.com/x86/test>

##
# o
## opcode

Binary number encoding a mnemonic in executable machine code.
##
## operand-size attributes
### `byte`

8 bits.

### `word`

Depends on the CPU, but in x86 terminology, that's 16 bits.

### `dword`

Depends on the CPU, but in x86 terminology, that's 32 bits.
"dword" stands for doubleword.

### `qword`

Depends on the CPU, but in x86 terminology, that's 64 bits.
"qword" stands for quadword.

##
# p
## point to

A register/variable can hold a value, or an address which refers to a value.
In the latter case, we say that it *points to* the value.

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

Some kind of global variables.
Each CPU architecture gives you a limited amount of them (a few dozens).
They all have the same size (typically 32 or 64 bits).

### `eflags`

See "status flag".

<https://en.wikibooks.org/wiki/X86_Assembly/X86_Architecture#EFLAGS_Register>

###
### rax

64-bit GPR.

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

32-bit GPR.  It's the 32 low bits of `rax`.

### ax

16-bit GPR.  It's the 16 low bits of `eax`.

### ah

8-bit GPR.  It's the 8 *high* bits of the `ax` register.

### al

8 bit GPR.  It's the 8 *low* bits of the `ax` register.

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

The 64-bit "Instruction Pointer" register.

At any given time, `rip` points to the next instruction to execute.
The CPU needs this information to know what to execute next.

And as soon  as it has executed  this instruction, `rip` is updated  so that the
process can go on.

### `eip`

The 32-bit, int size, "Instruction Pointer" register.  It's the 32 low bits of `rip`.

### `ip`

The 16-bit, "short" size, "Instruction Pointer" register.  It's the 16 low bits of `eip`.

At any given time, `ip` points to the next instruction to execute.

The CPU needs this information to know what to execute.
And as  soon as it has  executed this instruction,  `ip` is updated so  that the
process can go on.

###
### `rsp`

The 64-bit "Stack Pointer" register.

At any given time, `rsp` points to the value at the top of the stack.
The CPU needs this information to know:

   - where to push a new value on top of the stack
   - where to find the value to pop out of the stack

And as soon as  the CPU has pushed/popped a value, `rsp` is  updated so that the
process can go on.

---

For example, suppose you only have 1 value in the stack: `0x123`.
The stack looks like this:

    0x123  top of stack    <--- rsp

And `rsp` holds the last address in RAM.

Now,  you push  a new  value on  top of  the stack,  `0x456`, by  executing this
instruction:

    push 0x456

The new stack looks like this:

    0x456  top of stack    <--- rsp
    0x123  end of stack

And `rsp` holds the last *but one* address in RAM.

Now, you push a new value on top of the stack, `0x789`:

    push 0x789

The new stack looks like this:

    0x789  top of stack    <--- rsp
    0x456
    0x123  end of stack

And `rsp` holds the last but *two* address in RAM.

Now, you pop the value at the top of the stack into the register `eax`:

    pop eax

The new stack looks like this:

    0x456  top of stack    <--- rsp
    0x123  end of stack

`rsp` holds the last but one address in RAM.
And `eax` holds the value `0x789`.

Etc.

BTW,  notice that  the  `push`  and `pop`  instructions  use  their operands  in
different ways:

   - `push` uses its operand as a source (*what* to push)
   - `pop` uses its operand as a destination (*where* to store what will be popped)

### `esp`

The 32-bit "Stack Pointer" register.  It's the 32 low bits of `rsp`.

### `sp`

The 16-bit "Stack Pointer" register.  It's the 16 low bits of `esp`.

###
### segment registers

One of:

   - `ss`, aka Stack Segment: pointer to the stack
   - `cs`, aka Code Segment: pointer to the code
   - `ds`, aka data segment: pointer to the data
   - `es`, aka extra segment: pointer to extra data
   - `fs`: pointer to more extra data (`f` comes after `e`)
   - `gs`: pointer to still more extra data (`g` comes after `f`)

<https://en.wikibooks.org/wiki/X86_Assembly/X86_Architecture#Segment_Registers>

##
# s
## sizes
### byte

8 bits.

### word

16 bits.

### doubleword

32 bits.

### quadword

64 bits.

##
## stack

An area  at the  end of the  RAM, on  the top  of which you  can perform  only 2
operations:

   - push a value
   - pop a value

---

The stack is useful for handling function calls.

When calling  a function, the  CPU jumps to  a different instruction,  where the
function's code starts.  When the function returns, the CPU must jump back right
after the function call, to execute the next instruction.

IOW, the CPU needs to remember where it was.
Besides, a function might call another function, and the process can repeat itself.
IOW, the CPU needs to remember an ordered list of addresses in the code.
That's exactly what the stack is good for.

Here is an example:

    0xcccc  top of stack    <--- rsp
    0xbbbb
    0xaaaa  end of stack

Here, you can imagine that the code has  called a function A, which has called a
function B, which has called a function C.

`0xaaaa`, `0xbbbb`,  `0xcccc` are the  addresses of the next  instructions after
the calls to the functions A, B, C.

So, when C,  then B, and finally A  return, the CPU will know where  to find the
next instructions to execute: respectively at `0xcccc`, `0xbbbb`, and `0xaaaa`.

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
