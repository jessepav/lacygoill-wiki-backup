# egrep

    -i

            ignore-case

# syntax

The parentheses have three usages:

    - limit the scope of an alternation:

              ^(foo|bar)$    !=    ^foo|bar$

    - capture a sub-expression

    - apply a quantifier to a sub-expression


In a `grep`-like  program, writing an OPTIONAL sub-expression at  the end of the
pattern is useless.
Indeed, it only affects the length of the matched text; it doesn't affect whether
there IS a match or not (which is what `grep(1)` is mainly concerned with).

Ex:

        foo(bar)?
                ^
                is useless because it's at the end of the pattern

                Let's call:

                        - `t`  the (possible) text after `foo`
                        - `T`  the set of all possible texts
                        - `T₁` "                                 containing `bar`
                        - `T₂` "                             NOT containing `bar`

                        T = T₁ ∪ T₂

                Saying that `t` could contain `bar` means:

                        t ∈ T₁ ∪ T₂
                            │    │
                            │    └ the text does NOT contain `bar`
                            │
                            └ the text contains `bar`

                But we  already knew that,  because we had  no info on  the text
                after `foo` (t ∈ T):

                        t ∈ T
                      ⇔ t ∈ T₁ ∪ T₂


        foo(bar)?$
                ^
                `?` is useful, because it's NOT at the end of the pattern.

                Before `(bar)?`, we knew that:

                        t ∈ { ∅ }

                After `(bar)?`, we know that:

                        t ∈ { ∅, bar }

                Something has changed. `(bar)?` has added a new possibility.


More generally, describing an optional text before or after something is useless:

        (foo)?bar          ✘ saying that `foo` could be before `bar`, or not, doesn't add any info;
                             in both cases, any text could be before

              bar(baz)?    ✘ saying that `baz` could be after `bar`, or not, doesn't add any info;
                             in both cases, any text could be after

An optional text is only useful IN-BETWEEN two other texts:

         foo(bar)?baz      ✔ saying that `bar` could be between `foo` and `baz` ADDS info

Note that the two surrounding texts must contain some info:

         .*(foo)?.*     ✘
         .*(foo)?bar    ✘
        bar(foo)?.*     ✘

