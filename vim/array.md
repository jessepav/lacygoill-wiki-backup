# What's an array?

A non-scalar data: a list or a dictionary.

##
# Lists
## What is slicing?

The process of getting a sublist by appending a list with a range of indexes:

    echo range(1,5)[1:-2]
    [2, 3, 4]~

### On which conditions does it work as expected?  (2)

The first index must describe an item  which comes *before* the one described by
the second index.

    echo range(1,5)[-1:0]
    []~

In this example, the output is `[]`, instead of `[1, 2, 3]`, because the item of
index `-1` comes *after* the item of index `0`.

OTOH, in this example, the slicing works:

    echo ['a', 'b', 'c'][-2:2]
    ['b', 'c']~

because the item of index `-2` (`b`) comes before the item of index `2` (`c`).

---

If the  first index is a  variable, you may need  to separate it from  the colon
with a space; otherwise, Vim may wrongly interpret it as a scope.

    let [s, e] = [0, 2]

    echo range(1,3)[s:e]
    E121: Undefined variable: s:e~

    echo range(1,3)[s: e]
    E731: using Dictionary as a String~

    echo range(1,3)[s :e]
    echo range(1,3)[s : e]
    [1, 2, 3]~

###
## How is a negative index argument interpreted by a function handling a list?

`-1` = last item
`-2` = second item from the end
`-3` = third item from the end
...

##
## What's the output of `echo [4] == ['4']`?

`0`

### What can you infer from this result?

Vim does no coercion when comparing lists.

##
## Getting info
### How to get the number of occurrences of a value in
#### a dictionary?

    echo count(dict, val)

---

    echo count({'a': 1, 'b': 123, 'c': 123}, 123)
    2~

####
#### a list?

    echo count(list, val)

---

    echo count(['a', 'b', 'a'], 'a')
    2~

##### ignoring the case?

Use the third optional argument:

    echo count(list, item, 1)

---

    echo count(['a', 'b', 'A'], 'a', 1)
    2~

---

It works with dictionaries as well:

    echo count({'one': 'a', 'two': 'b', 'three': 'A'}, 'a', 1)
    2~

##### counting from `{start}` items after the beginning of the list?

Use the fourth optional argument:

    echo count(list, item, 0, start)

---

    echo count(['a', 'a', 'a'], 'a')
    3~

    echo count(['a', 'a', 'a'], 'a', 0, 1)
    2~

###
### How to get the first item in `list` which matches `pat`?

    echo matchstr(list, pat)

---

    echo matchstr(['foo', 'bar', 'baz'], '^b')
    bar~

Note that you get the whole item, not just the part matching the pattern.

#### starting from the item of index `{start}`?

    echo matchstr(list, pat, start)

---

    echo matchstr(['-a', '_', '-b'], '-', 1)
    -b~

##### and only the `{count}`-th item matching the pattern?

    echo matchstr(list, pat, start, count)

---

    echo matchstr(['-a', '_', '-b', '-c'], '-', 1, 2)
    -c~

####
#### Instead of the item, how could I have got its index?

Replace `matchstr()` with `match()`:

    echo match(list, pat)
    echo match(list, pat, start)
    echo match(list, pat, start, count)

---

    echo match(['_', '-a'], '-')
    1~

    echo match(['-a', '_', '-b'], '-', 1)
    2~

    echo match(['-a', '_', '-b', '-c'], '-', 1, 2)
    3~

###
### How to get the byte index of the start and end of a match in the first matching item of a list?

Use `matchstrpos()`:

    echo matchstrpos(list, pat)

---

    echo matchstrpos(['_', '__x'], '\a')
    ['x', 1, 2, 3]~
      │   │  │  │
      │   │  │  └ byte index of the end of the match +1
      │   │  └ byte index of the start of the match inside the item
      │   └ index of the item
      └ match (`matchstr()` would have returned the whole item)

###
## Initializing
### How to initialize a list of length `5`, all items being `0`?

Use `map()` + `range()`:

                       ┌ a number is allowed (in addition to a string)
                       │
    echo map(range(5), 0)
    [0, 0, 0, 0, 0]~

Or `repeat()`:

    echo repeat([0], 5)
    [0, 0, 0, 0, 0]~

### How to initialize a table whose size is `4` rows times `3` columns, all items being `0`?

Use `map()` + `range()`:

    echo map(range(4), 'map(range(3), 0)')
    [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]~

##
### How to get the list of numbers
#### multiple of `5` from `20` up to `40`?

               ┌ start
               │   ┌ end
               │   │   ┌ step
               │   │   │
    echo range(20, 40, 5)
    [20, 25, 30, 35, 40]~

#### from `2` to `-2`, in descending order?

    echo range(2, -2, -1)
    [2, 1, 0, -1, -2]~

##
## Removing
### How to remove the item `garbage` from `list`, knowing its index?  (2)

`idx` being the index of `garbage`, use `:unlet` or `remove()`:

    unlet list[idx]

    call remove(list, idx)

---

    let list = ['a', 'garbage', 'b']
    unlet list[1]
    echo list
    ['a', 'b']~

    let list = ['a', 'garbage', 'b']
    call remove(list, 1)
    echo list
    ['a', 'b']~

### How to remove all the items from `list` beyond the index `2`?  (2)

    unlet list[2:]

    call remove(list, 2, -1)

---

    let list = ['a', 'b', 'foo', 'bar', 'baz']
    unlet list[2:]
    echo list
    ['a', 'b']~

    let list = ['a', 'b', 'foo', 'bar', 'baz']
    call remove(list, 2, -1)
    echo list
    ['a', 'b']~

### How to remove the item `garbage` from a list, not knowing its index?  (2)

Use `index()` + `remove()`:

    call remove(list, index(list, 'garbage'))

    unlet list[index(list, 'garbage')]

---

    let list = ['a', 'garbage', 'b']
    call remove(list, index(list, 'garbage'))
    echo list
    ['a', 'b']~

    let list = ['a', 'garbage', 'b']
    unlet list[index(list, 'garbage')]
    echo list
    ['a', 'b']~

### What's the output of `remove()`?

Whatever was removed.

##
## Adding
### How to add an item
#### in front of a list?

Use `insert()`:

    echo insert(list, item)

---

    let list = [1, 2]
    echo insert(list, 'a')
    ['a', 1, 2]~

#### in the middle of a list?

Use `insert()` and the index of the item *before* which you want your item to be
inserted:

    echo insert(list, item, idx)

---

    let list = ['a', 'c']
    echo insert(list, 'b', 1)
    ['a', 'b', 'c']~

#### before the last item of a list?

    echo insert(list, item, -1)

---

    let list = ['a', 'b', 'd']
    echo insert(list, 'c', -1)
    ['a', 'b', 'c', 'd']~

#### at the end of a list?

Use `add()`:

    echo add(list, item)

---

    let list = ['a', 'b']
    call add(list, 'c')
    echo list
    ['a', 'b', 'c']~

Note that `add()` operates in-place.

##### Why can't this be used to concatenate lists?

If you pass a second  list as an argument, it will be added  as a single item in
the first list.

    let list = [1, 2]
    call add(list, [3, 4])
    echo list
    [1, 2, [3, 4]]~

###
### How to concatenate lists?  (2)

Use the `+` operator or `extend()`.

    echo list1 + list2

    echo extend(list1, list2)

---

    let list = [1, 2, 3]
    echo list + [4, 5]
    [1, 2, 3, 4, 5]~

    let list = [1, 2, 3]
    echo extend(list, [4, 5])
    [1, 2, 3, 4, 5]~

#### What's the difference between the 2 methods?

The `+` operator doesn't make mutate any list:

    let list = [1, 2]
    echo list + [3, 4]
    [1, 2, 3, 4]~
    echo list
    [1, 2]~

OTOH, `extend()` makes the first list mutate:

    let list = [1, 2]
    echo extend(list, [3, 4])
    [1, 2, 3, 4]~
    echo list
    [1, 2, 3, 4]~

But not the second one:

    let alist = [1, 2]
    let blist = [3, 4]
    echo extend(alist, blist)
    [1, 2, 3, 4]~
    echo blist
    [3, 4]~

Remember: the  first argument **m**utates, the  second one **w**ins (in  case of
conflict) **w**ithout **k**eep being used (as third argument).
Mnemonic: "1. mutates, 2. wins without keep" ("MWWK").

####
### How to insert some list inside another list, at an arbitrary position?

Use `extend()`,  and provide the  index of the item  in the first  list *before*
which you want the items of the second list to be inserted.

    call extend(alist, blist, idx)

---

    let alist = ['a', 'd']
    let blist = ['b', 'c']
    echo extend(alist, blist, 1)
    ['a', 'b', 'c', 'd']~

##
## Transforming
### How to change the value of a range of consecutive items in a list, with a single statement?

Use an assignment: in the lhs, use slicing; in the rhs, use a list of values.

    let list[i:j] = [val1, val2, ...]

---

    let list = ['a', 'x', 'y', 'd']
    let list[1:2] = ['b', 'c']
    echo list
    ['a', 'b', 'c', 'd']~

###
### How to rotate the items of a list to the left?

Use a combination of  `add()` and `remove()`, to move the first  item to the end
of the list:

    call add(list, remove(list, 0))

---

    let list = range(1, 4)

    call add(list, remove(list, 0))
    echo list

#### to the right?

Use a  combination of `insert()`  and `remove()`, to move  the last item  to the
beginning of the list:

    call insert(list, remove(list, -1), 0)

---

    let list = range(1, 4)

    call insert(list, remove(list, -1), 0)
    echo list

####
### How to increment a number item?

Use an assignment.
In the  lhs, use  the index of  the item you  want to  change; and use  the `+=`
operator:

    let list[idx] += n

---

    let list = [1, 2, 3]
    let list[2] += 99
    echo list
    [1, 2, 102]~

### How to concatenate a string to a string item?

Use an assignment.
In the  lhs, use  the index of  the item you  want to  change; and use  the `.=`
operator.

    let list[idx] .= str

---

    let list = ['ab', 'c']
    let list[1] .= 'd'
    echo list
    ['ab', 'cd']~

###
### Mutation
#### What's the output of the last command in these snippets?
##### 1:

    fu Increment(list, i)
        let a:list[a:i] += 1
    endfu
    let list = [0, 0, 0]
    call Increment(list, 2)
    echo list

↣ [0, 0, 1] ↢

##### 2:

    fu Increment(list, i)
        let a:list[a:i] += 1
    endfu
    let counts = [0, 0, 0]
    let patterns = ['a_word', 'b_word', 'c_word']
    for i in range(3)
        exe '%s/'..patterns[i]..'/\=Increment(counts,'..i..')/gn'
    endfor
    echo counts

↣
    [1, 1, 1]~

Note that the list name changed inside the function (`counts` → `list`).
But it doesn't matter: `counts` has still mutated.
↢

##### 3:

    fu Func()
        let list = [1, 2, 3]
        let n = 42
        call FuncA(n)
        echo n
    endfu
    fu FuncA(n)
        let l:n = a:n
        let l:n += 1
    endfu
    call Func()

↣ 42 ↢

#####
##### How do you explain these results?

The lists have mutated because Vim passes arrays by reference, not by value.
`Increment()`  received a  reference  of `list`  in the  first  snippet, and  of
`counts` in the second one.

In the third snippet, the number has not been altered because Vim passes scalars
by value.

It  seems  that  Vim behaves  like  awk:  scalars  are  passed by  value,  while
non-scalar values are passed by reference.

##### What's the property of arrays without which these results would not be possible?

An array is mutable.

####
#### Does `let blist = alist` create a copy of `alist`?

No.

`blist` and `alist` share the same reference.
Any change you perform on `blist` will affect `alist`.

    let alist = [1, 2]
    let blist = alist
    let blist[1] += 1
    echo alist
    [1, 3]~

##### How to make a copy of `alist`?

If the items of the list are scalars, use `copy()`:

    let alist = [1, 2]
    let blist = copy(alist)
    let blist[1] += 1
    echo alist
    [1, 2]~

If the items of the list are non-scalars, use `deepcopy()`:

    let alist = [1, [2,3]]
    let blist = deepcopy(alist)
    let blist[1][1] += 1
    echo alist
    [1, [2, 3]]~

    let alist = [1, {'n': 2}]
    let blist = deepcopy(alist)
    let blist[1].n += 1
    echo alist
    [1, {'n': 2}]~

####
#### The next code mutates a dictionary so that the numbers in its list values are doubled.

    let dict = {'A': [1,2], 'B': [3,4], 'C': [5,6]}
    call map(dict, {_,v -> map(v, {_,v -> v * 2})})
    echo dict
    {'A': [2, 4], 'B': [6, 8], 'C': [10, 12]}~

##### Rewrite it using `items()`, a single `map()`, and without any additional `:let` assignment.

    let dict = {'A': [1,2], 'B': [3,4], 'C': [5,6]}
    for [k,v] in items(dict)
        call map(v, {_,v -> v * 2})
    endfor
    echo dict
    {'A': [2, 4], 'B': [6, 8], 'C': [10, 12]}~

Since the values of the dictionary are lists, Vim does not assign copies to `v`,
but references.

####
#### Which special list is unable to mutate?

`a:000` can't mutate:

    fu Func(...) abort
        return map(a:000, 'v:val+1')
    endfu
    echo Func(1, 2, 3)
    E742: Cannot change value of map() argument~

#### I can't append a new item to a list argument with `+=`!

    fu Func(list) abort
        let a:list += [2]
        echo a:list
    endfu
    call Func([1])
    E46: Cannot change read-only variable "a:list"~

Use `add()` instead of `+=`:

    fu Func(list) abort
        call add(a:list, 2)
        echo a:list
    endfu
    call Func([1])
    [1, 2]~

Imo, `+=` should work just like `add()`...

See `:h E742`:

>     The a: scope and the variables in it cannot be changed, they are fixed.
>     However, if a composite type is used, such as |List| or |Dictionary| , you can
>     change their contents.  Thus you can pass a |List| to a function and have the
>     function add an item to it.

###
# Dictionaries
## What are the benefits of the syntax `dict['key']` over `dict.key`?

It allows the usage of:

   - more characters

   - a key whose name is the evaluation a variable

        ✘
        dict.var

        ✔
        dict[var]

##
## Getting info
### How to get the number of occurrences of a value in a dictionary?

Use `count()`:

    echo count(dict, val)

---

    let dict = {'a': 1, 'b': 2, 'c': 3}
    echo count(dict, 3)
    1~

The value `3` is present once in the the dictionary.

##
## Adding
### How to add all the items of a dictionary to another dictionary?

Use `extend()`:

    call extend(adict, bdict)

---

    let adict = {'one': 1, 'two': 2}
    let bdict = {'three': 3, 'four': 4}
    echo extend(adict, bdict)
    {'four': 4, 'one': 1, 'two': 2, 'three': 3}~

### In case of conflict between two keys with different values, how to
#### make the value of the first dictionary win?

Use the optional third argument `keep`:

    echo extend(adict, bdict, 'keep')

---

    let adict = {'one': 1, 'two': 2}
    let bdict = {'one': 4, 'three': 3}
    echo extend(adict, bdict, 'keep')
    {'one': 1, 'two': 2, 'three': 3}~

#### raise an error?

Use the optional third argument `error`:

    echo extend(adict, bdict, 'error')

---

    let adict = {'one': 1, 'two': 2}
    let bdict = {'one': 4, 'three': 3}
    echo extend(adict, bdict, 'error')
    E737: Key already exists: one~

##
## Removing
### How to remove an item from a dictionary knowing its key?  (2)

Use `:unlet` or `remove()`:

    unlet dict.key

    call remove(dict, 'key')

---

    let dict = {'one': 1, 'two': 2}
    unlet dict.two
    echo dict
    {'one': 1}~

    let dict = {'one': 1, 'two': 2}
    call remove(dict, 'two')
    echo dict
    {'one': 1}~

### What is the output of `remove()`?

The *value* (!= item) of the removed key.

    let dict = {'one': 1, 'two': 2}
    let var = remove(dict, 'two')
    echo var
    2~

##
### How to remove all the items of a dictionary, based on a condition on
#### its values?

Use `filter()` and a condition inspecting the value (`v`):

    call filter(dict, {k,v -> cond(v)})

---

    let dict = {'ab': 1, 'cd': 2, 'abcd': 3}
    echo filter(dict, {k,v -> v > 1})
    {'abcd': 3, 'cd': 2}~

Here, you removed all the items whose values were not greater than `1`.

#### its keys?

Use `filter()` and a condition inspecting the key (`k`):

    call filter(dict, {k,v -> cond(k)})

---

    let dict = {'ab': 1, 'cd': 2, 'abcd': 3}
    echo filter(dict, {k,v -> k =~# '^a'})
    {'abcd': 3, 'ab': 1}~

Here, you removed all the items whose keys didn't begin with `a`.

##
## I have a list of words.  What's the most efficient way to build a dictionary of words frequencies?

Iterate over the words of the list, to build the dictionary.

    let list = ['one', 'two', 'two', 'three', 'three', 'three']
    let freq = {}
    for word in list
        let freq[word] = get(freq, word, 0) + 1
    endfor
    echo freq
    {'one': 1, 'two': 2, 'three': 3}~

Note that you can't write one of these statements:

    let freq[word] += 1
    let freq[word] = freq[word] + 1

Because when  the loop will  encounter `word` for  the first time,  `freq` won't
have any key yet  for it; so `freq[word]` won't exist which  will raise an error
in the rhs of the assignment.

---

Don't use `count()`; it would be less effecient:

    fu Func()
        let words = []
        %s/\<\k\+\>/\=add(words, submatch(0))/gn
        let freq = {}
        for word in uniq(sort(copy(words)))
            let freq[word] = count(words, word)
        endfor
        echo freq
    endfu
    10Time sil call Func()

    fu Func()
        let words = []
        %s/\<\k\+\>/\=add(words, submatch(0))/gn
        let freq = {}
        for word in words
            let freq[word] = get(freq, word, 0) + 1
        endfor
        echo freq
    endfu
    10Time sil call Func()

Indeed, assuming your list contains 10  unique words, you would invoke `count()`
10 times.
And  assuming  you have  100  words  in total,  each  time,  it would  make  100
comparisons  to  get  the  number  of  occurrences  of  the  word:  that's  1000
comparisons in total.

