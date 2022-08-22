# Why should I avoid a mutable object for the default value of an optional parameter?

It would mutate across function calls which is probably not what you want:
```python
def func(opt=[]):
    opt += [0]
    print(opt)

func()
func()
func()
```
    [0]
    [0, 0]
    [0, 0, 0]

If `opt` had always been assigned the  default value `[]`, then the output would
always have been the same:

    [0]
    [0]
    [0]

But that's not  what happened.  During the first call,  `opt` has correctly been
assigned `[]`,  hence why  the function  prints `[0]` after  the item  `"x"` was
added.  But during the subsequent calls, `opt` has *not* been assigned `[]`

---

This is an issue for lists and dictionaries; not for tuples which are immutable.

## But why does that happen?  Why is the default value sometimes ignored?

Because default  parameter values are  evaluated when the function  is *defined*
(i.e. when the `def` statement is executed); not when the function is *called*.

This means that a default value is  only assigned once, no matter how many times
you call the function.

In turn, this  implies that the default  value is bound to  the function object;
otherwise, the value would not be preserved across function calls.

## OK.  And how do I work around that?

First, use `None` as the default value.
Then, in the  function body, assign the default value  to the optional parameter
iff it's `None`.
```python
 #           v--v
def func(opt=None):
    #      v-----v
    if opt is None:
        opt = []
    opt.append(0)
    print(opt)

func()
func()
func()
```
    [0]
    [0]
    [0]

##
# Why should I avoid `from module import *`?

It makes it hard:

   - to avoid conflicting names
   - to find where an imported item is defined

   - to know which items are imported (in particular, if you're in A, and import
     module B, which itself imports another module C, C will be imported in A)

   - for  the  editor to  provide  extra  features such  as  code completion,
     go-to definition, and inline documentation
