# What's this case study which is mentioned in every chapter?

Some kind of  project, in which we'll  be building a classifier  for iris flower
species.

It will  teach us how  to automate a job  called "classification", which  is the
main idea behind  product recommendations: last time, a  customer bought product
X,  so maybe  they would  be  interested in  a  similar product  Y, which  we've
classified to belong to the same class.

But classifying  consumer products can  be complex, which  is why we  start with
something easier: classifying iris flower species.

# What do we need?

A  training  data set,  which  the  classifier  algorithm  uses as  examples  of
correctly classified irises.

Each  training sample  (iris) should  have a  number of  attributes (e.g.  petal
shape, size, ...) encoded into a numeric vector which represents the iris.
For example:

    5.1,3.5,1.4,0.2

Here, the vector has 4 dimensions whose coordinates are `5.1`, `3.5`, `1.4` and `0.2`.

A training sample should also have a correct species label:

    Iris-setosa

## Where can I find this?

<https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data>

Or Google "Iris Classification data".

##
# What algorithm will we use?

k-NN which stands for the k-nearest neighbors.

## How does it work?

Given an unknown sample (an iris whose  species we want to know), we compute the
distance between  the unknown sample and  the nearest `k` known  samples.  Among
them, if  we find out  that a majority  is of a  given species, we  classify our
unknown sample in that same species (we say that we "take a vote").

## How about a concrete example?

Let's assume our samples have only 2 attributes.
First, we use their vectors to position them in a 2-dimensional space:

    +-----------------------------------+
    |                                   |
    |       ●                           |
    |                                   |
    |                   ●               |
    |                                   |
    |               ●                   |
    |                                   |
    |                   ◆               |
    |                                   |
    |                       ■           |
    |                                   |
    |                                   |
    |                                   |
    |               ■       ■           |
    |                                   |
    |                                   |
    |                                   |
    +-----------------------------------+

Our unknown sample is the diamond in the middle.
It's surrounded by known samples of the Square and Circle species.

Next, we draw a small disk (here represented with asterisks) centered around our
unknown sample, and containing only the latter:

    +-----------------------------------+
    |                                   |
    |       ●                           |
    |                                   |
    |                   ●               |
    |                                   |
    |               ●                   |
    |                  ***              |
    |                 * ◆ *             |
    |                  ***              |
    |                       ■           |
    |                                   |
    |                                   |
    |                                   |
    |               ■       ■           |
    |                                   |
    |                                   |
    |                                   |
    +-----------------------------------+

Then, we progressively increase the radius of  the disk so that it includes more
and more  neighbors.  Let's say we  chose `k = 3`; we  stop as soon as  the disk
includes 3 neighbors:

    +-----------------------------------+
    |                                   |
    |       ●                           |
    |               *********           |
    |            ***    ●    ***        |
    |          **               **      |
    |         *     ●             *     |
    |        *                     *    |
    |        *          ◆          *    |
    |        *                     *    |
    |         *             ■     *     |
    |          **               **      |
    |            ***         ***        |
    |               *********           |
    |               ■       ■           |
    |                                   |
    |                                   |
    |                                   |
    +-----------------------------------+

Among them, 2 are of the Circle species,  while only 1 is of the Square species.
The majority of the neighbors is of the Circle species, which means that – for
`k = 3` – the algorithm decides that the  unknown sample is most likely of the
Circle species.

---

Note that  we assumed  our samples only  had 2 attributes  because it's  hard or
impossible to draw a  diagram in 3 or more dimensions inside  a text document; 2
is the highest we can go for a simple diagram.

### But if `k = 5` the result would be different!

Indeed, in that case the 5 nearest neighbors would be inside this disk:

    +-----------------------------------+
    |               *********           |
    |       ●     **         **         |
    |           **             **       |
    |          *        ●        *      |
    |         *                   *     |
    |        *      ●              *    |
    |        *                     *    |
    |        *          ◆          *    |
    |        *                     *    |
    |        *              ■      *    |
    |         *                   *     |
    |          *                 *      |
    |           **             **       |
    |             **■       ■**         |
    |               *********           |
    |                                   |
    |                                   |
    +-----------------------------------+

This time,  there are 3 known  samples of the  Square species, and only  2 known
samples of the Circle  species.  The majority of the neighbors  is of the Square
species, and the algorithm decides that the unknown sample is most likely of the
Square species.

This illustrates the influence of the `k` factor.
By  changing  its value,  we  change  the composition  of  the  pool of  nearest
neighbors, which in turn can affect the result of the vote.

### Which one is correct?  `k = 3` or `k = 5`?

There is no correct choice.

If the value is  too small, you'll often get inaccurate  results, but you'll get
them fast.  If the  value is too big, you'll get accurate  results, but it'll be
computationally expensive  (in part because  the algorithm will have  to compute
more distances).

As a simple heuristic, start with $k  = \sqrt{n}$, where `n` is the total number
of samples in your training data set.
See: <https://stats.stackexchange.com/a/535051>

##
# Resources
## example code files

<https://github.com/PacktPublishing/Python-Object-Oriented-Programming---4th-edition>
