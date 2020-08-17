# CLI

    dot -Txxx
    dot -Tpng:

            Display the output formats supported by dot.

            Display the variants of the `png` output format.
            The 1st one is the default:

   > Format: "png:" not recognized. Use one of: png:cairo:cairo png:cairo:gd png:gd:gd
   >                                            └─────────────┤
   >                                                          └ default


               ┌ automatically generate an output filename based on the input filename
               │ and the -T format
               │
    dot -Tpng -O graph.dot
    dot -Tpng graph.dot -o graph.pdf

            Create `graph.pdf` from the code stored in `graph.dot`.

            Here, we use the `dot` command, but depending on the type of graph
            we're interested in, we could use another:

                        dot   = directed graph
                        neato = non-directed graph
                        circo = circular graph
                        …

# Syntax

    // comment


    graph <id> {
        …
    }

    digraph <id> {
        …
    }

            Definition of an (un)directed graph.


    A -> B

            An edge between 2 nodes, whose label will be A and B.

    A -> {B, C}

            2 edges between 3 nodes, A to B and A to C.
            The label of the nodes will be A, B, C.

    A -- B

            Undirected edge between the nodes A and B.


    {rank = same ; A, B}

            The nodes A and B must have be on the same level.

    rankdir = LR

            The graph must be directed from left to right.
            Other possible values:

                    - BT     bottom -> top
                    - RL     right  -> left
                    - TB     top    -> bottom

    nodesep = 1.0

            Size of the gap  between any pair of nodes.
            Increasing the value can make the graph more readable.
            Decreasing the value can make more information fit on the screen.


    bgcolor = "#<hex>"

            Background color of the graph.

# Attributes

You can change the appearance of a node / edge by suffixing them with:

        [attribute1 = val1, attribute2 = val2 ...]


Each attribute may be given to different objects:

    [E] = edge
    [N] = node
    [G] = graph
    [S] = subgraph
    [C] = cluster


Here are some common attributes:


    edge[color = "red"]

        [ENC]

            Set the color of all edges which will be created after this statement to red.

            For more colors, see:

                    https://graphviz.gitlab.io/_pages/doc/info/colors.html


    dir = back
    dir = both

        [E]

            In a directed graph:

                    - reverse the direction of an arrow
                    - add an arrow in the other direction


    fontcolor
    fontname
    fontsize

        [ENGC]

            Settings of the police used to write the text in a node/edge.


    node_a           [label = "stuff"]
    node_a -> node_b [label = "action"]

        [ENGC]

            Set the label of:

                    - the node `node_a` to 'stuff'
                    - the edge from `node_a` towards `node_b`, to 'action'

            With the 1st line, we'll refer to the node with the id `node_a`.
            But in the graph, it will be named `bar`.
            This is useful when the text of a node contains special characters
            which can't be included in an id (example: newline).

            If the value of `label` contains  a backslash or a double quote, you
            must escape it.  To include a newline, write `\n`.

            And if  it contains multiple  lines, you can  justify a line  to the
            left or right, by surrounding it with `\l` or `\r`.


    shape = box
    shape = plaintext

        [N]

            Shape of a node.
            plaintext = no outline

            For more shapes, see:

                    https://graphviz.gitlab.io/_pages/doc/info/shapes.html


    size = "x,y"

        [G]

            Maximum size of the graph in inches.


    splines = line

        [G]

            The edges must be straight lines.

            (FR: spline = cannelure, languette)


    style = dashed
    style = dotted
    style = bold

    style = filled, fillcolor = yellow

        [ENCG]

            The outline of a node / edge must be dashed/dotted/bold.

            Set the background color of a node to yellow.


    weight = 8

        [E]

            Weight  of  edge.  In  dot,  the heavier  the  weight,  the  shorter,
            straighter and more vertical the edge is.

# Examples

    digraph {
        A -> B;
    }

    digraph G {
        main -> init -> make_string;
        main -> parse -> execute -> make_string;
        main -> cleanup;
        main -> printf;
        execute -> compare;
        execute -> printf;
    }

    digraph G {
        size = "4,4";
        main [shape=box]; // this is an inline comment
        main -> parse [weighted=8];
        parse -> execute;
        main -> init [style=dotted];
        main -> cleanup;
        execute -> { make_string; printf };
        init -> make_string;
        edge [color=red];
        main -> printf [style=bold,label="100 times"];
        make_string [label="make a \nstring"];
        node [shape=box,style=filled,color=".7 .3 1.0"];
        execute -> compare;
    }

# Glossary

    attribute

            name-value pair of character strings,  used in the input file, which
            allows to adjust the representation or placement of nodes, edges, or
            subgraphs in the layout.


    DOT

            DOT is a  declarative language in which you express  nodes and their
            relations in a graph.  You can label the nodes and their edges (links
            between nodes) and you can use a lot of styling and shaping tools.


    dot

            `dot` is  a cli tool  able to draw a  graph, which can  be described
            with the DOT language.  It belongs to the `graphviz` package.


    graph
    digraph

            A  graph  is  just  a  collection  of  connected  nodes.  There's  no
            “parent-child” relationship between 2 nodes.

            A digraph is a graph where the connections have a direction.

            In the DOT language, you write the connections in:

                    - a graph   with  --
                    - a digraph with  ->


    edge operator

            Operator which creates an edge between 2 nodes:

                    * ->  (directed graph)
                    * --  (undirected graph)


    subgraph

            subset of nodes and edges.

# Links

    http://www.graphviz.org/documentation/

            Official documentation.


    http://www.tonyballantyne.com/graphs.html#sec-5-2

            records


    http://www.tonyballantyne.com/graphs.html#sec-6-3

            subgraphs

