# Table of (some) operators in descending order of precedence

    ┌───────────┬────────────────────────┬─────────────────────────┐
    │ Symbol(s) │ Name                   │ Associativity           │
    ├───────────┼────────────────────────┼─────────────────────────┤
    │ ++        │ Increment postfix      │ Left                    │
    │ --        │ Decrement postfix      │ Left                    │
    ├───────────┼────────────────────────┼─────────────────────────┤
    │ ++        │ Increment prefix       │ Right                   │
    │ --        │ Decrement prefix       │ Right                   │
    │ +         │ Unary plus             │ Right                   │
    │ -         │ Unary minus            │ Right                   │
    │ !         │ Logical negation       │ Right                   │
    ├───────────┼────────────────────────┼─────────────────────────┤
    │ * / %     │ Multiplicative         │ Left                    │
    ├───────────┼────────────────────────┼─────────────────────────┤
    │ + -       │ Additive               │ Left                    │
    ├───────────┼────────────────────────┼─────────────────────────┤
    │ < > <= >= │ Relational             │ Left                    │
    ├───────────┼────────────────────────┼─────────────────────────┤
    │ == !=     │ Equality               │ Left                    │
    ├───────────┼────────────────────────┼─────────────────────────┤
    │ &&        │ Logical and            │ Left                    │
    ├───────────┼────────────────────────┼─────────────────────────┤
    │ ||        │ Logical or             │ Left                    │
    ├───────────┼────────────────────────┼─────────────────────────┤
    │ ?:        │ Conditional            │ Left                    │
    ├───────────┼────────────────────────┼─────────────────────────┤
    │ =  *= /=  │ Assignment             │ Right                   │
    │ %= += -=  │                        │                         │
    ├───────────┼────────────────────────┼─────────────────────────┤
    │ ,         │ Comma                  │ Left                    │
    └───────────┴────────────────────────┴─────────────────────────┘

Operators in the same cell have the same precedence.
If you have several operators of  equal precedence adjacent to the same operand,
you need to know  another one of their property to  determine how the operations
will be grouped: their associativity.
