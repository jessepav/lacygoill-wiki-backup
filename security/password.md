# passphrase
## What's a passphrase?

A sequence  of words  used to control  access to a  computer system,  program or
data.

### How does it differ from a password?

It's similar  to a password in  usage, and easier  to remember, but needs  to be
longer to provide the same level of security.

### Which programs often rely on a passphrase?

Cryptographic programs which derive an encryption key from it.
E.g., keepass, gpg, ...

### Do I need to add a space between two consecutive words?

You can, but it's not a necessity.

### How to measure the strength of a passphrase?

Compute  the maximum  number of  guesses  an attacker  should make  to find  the
passphrase, assuming they know everything about how it was generated; let's call
it G.

The strength is then expressed as a number of bits of entropy; let's call it E.
E is derived from G, with the formula `E = ln(G)/ln(2)`.
This is because `G = 2^E`.

###
## What's Diceware?

A  method for  creating passphrases  using ordinary  dice as  a hardware  random
number generator.

### What does it need?  (2)

Dice, and a list of words indexed by numbers whose digits are between 1 and 6.
Such a list is sometimes called a Diceware word list.

### How does it work?

You choose the length of the passphrase you want to generate, in number of words.
E.g., seven.

You choose a Diceware word list.
E.g., the large Diceware word list published by the EFF in 2016.

For each word in the passphrase, you roll the dice five times.
The numbers from 1 to 6 that come  up in the rolls are assembled as a five-digit
number, e.g. 43146.
You use that number to look up a word in the word list.
E.g., in the EFF's large Diceware word list, 43146 corresponds to “overcook”.

You repeat the process seven times to progressively build your passphrase.

#### I don't have dice!

Then use a software to generate pseudo-random numbers.

<https://github.com/ulif/diceware>

###
### EFF's Diceware word lists
#### How many words does the large list contain?

7776

##### Why this particular number?

It's equal to the number of possible  ordered rolls of *five* six-sided dice (7776
= 6^5), making it suitable for using standard dice as a source of randomness.

####
##### How many bits of entropy does a word from the large list add to a passphrase?

12.9

Indeed, `2^12.9 ≈ 7776`.

---

This number of bits is cumulative.
Indeed, if you choose  2 words, then an attacker would need at  most 7776 * 7776
guesses, and:

    7776 * 7776
    ≈
    2^12.9 * 2^12.9
    =
    2^25.8

###### How many words should I choose from the large list to make up a strong passphrase?

At least 6.

   > However, starting  in 2014, Reinhold  recommends that  at least six  words (77
   > bits) should be used.

Source: <https://en.wikipedia.org/wiki/Diceware>

For more security, you may want to go up to 7, or even 8 words.

---

If you're interested in a table mapping the entropy of a password to the time it
takes to crack it, have a look here:

<https://www.reddit.com/r/dataisbeautiful/comments/322lbk/time_required_to_bruteforce_crack_a_password/>

####
#### How many words does the short list contain?

1296

##### Why this particular number?

It's equal to the number of possible ordered rolls of *four* six-sided dice (1296 = 6^4).

##### How many bits of entropy does a word from the short list add to a passphrase?

10.3

Indeed, `2^10.3 ≈ 1296`.

##### What's the benefit of the short list over the large one?

It's designed to  include the 1,296 most memorable and  distinct words, with the
hope that it yields passphrases that are easier to remember.

Further study is needed to determine whether it succeeds in doing that.

#####
#### Which of the two lists should I use?

Use the large one.
If you have difficulties to remember the passphrases it generates, try the short
list.

###
### What makes a good Diceware word list?

A good one should only contain words which are easy to spell and remember.

It should also avoid the [prefix code][1] problem.
I.e., it should not contain words that start with other words in the list.
Otherwise a generated passphrase may contain less entropy than expected.

For example, if you choose the two words “in” and “put”, you expect to add twice
the number of bits of entropy contained in a word; let's call the latter E.
But if you don't add spaces between  the words, you get the single word “input”,
and you only add E once (not twice).

Note that  to avoid  the issue, you  can also capitalize  each word,  instead of
adding spaces:

    in + put = InPut != Input

#### Is a passphrase more secure if it uses longer words on average?

No.
The security of  a passphrase is entirely  determined by the number  of words it
contains, and the size of the Diceware word list.

###
# Cracking
## When trying to crack a password with a brute-force attack, how many guesses could make a desktop computer in 2018?

About 15 million passwords per second.

Source: <https://www.eff.org/deeplinks/2018/08/dragon-con-diceware>

### How about the fastest supercomputer?

About 92 trillion passwords per second.

##
# Reference

[1]: https://en.wikipedia.org/wiki/Prefix_code

