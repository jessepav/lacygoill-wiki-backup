don't breathe
get out
it follows
tomorrowland
magic dance

tick tack
il était une fois ... la vie

duck tales
an american tail
the land before time

# TOC
## Informal Logic
### 1 Basic concepts

        1.1 Arguments, Premises and Conclusions
        1.2 Recognizing Arguments
        1.3 Deduction and Induction
        1.4 Validity, Truth, Soundness, Strength, Cogency
        1.5 Argument Forms: Proving Invalidity
        1.6 Extended Arguments

### 2 Language: Meaning and Definition

        2.1 Varieties of Meaning
        2.2 The Intension and Extension of Terms
        2.3 Definitions and Their Purposes
        2.4 Definitional Techniques
        2.5 Criteria for Lexical Definitions

### 3 Informal Fallacies

        3.1 Fallacies in General
        3.2 Fallacies of Relevance
        3.3 Fallacies of Weak Induction
        3.4 Fallacies of Presumption, Ambiguity, and Illicit Transference
        3.5 Fallacies in Ordinary Language

###
## Formal Logic
### 4 Categorical Propositions

        4.1 The components of Categorical Propositions
        4.2 Quality, Quantity, and Distribution
        4.3 Venn Diagrams and the Modern Square of Opposition
        4.4 Conversion, Obversion, and Contraposition
        4.5 The Traditional Square of Opposition
        4.6 Venn Diagrams and the Traditional Standpoint
        4.7 Translating Ordinary Language Statements into Categorical Form


### 5 Categorical Syllogisms

        5.1 Standard Form, Mood, and Figure
        5.2 Venn Diagrams
        5.3 Rules and Fallacies
        5.4 Reducing the Number of Terms
        5.5 Ordinary Language Arguments
        5.6 Enthymemes
        5.7 Sorites

### 6 Propositional Logic

        6.1 Symbols and Translation
        6.2 Truth Functions
        6.3 Truth Tables for Propositions
        6.4 Truth Tables for Arguments
        6.5 Indirect Truth Tables
        6.6 Argument Forms and Fallacies

### 7 Natural Deduction in Propositional Logic

        7.1 Rules of Implication I
        7.2 Rules of Implication II
        7.3 Rules of Replacement I
        7.4 Rules of Replacement II
        7.5 Conditional Proof
        7.6 Indirect Proof
        7.7 Proving Logical Truths

### 8 Predicate Logic

        8.1 Symbols and Translation
        8.2 Using the Rules of Inference
        8.3 Quantifier Negation Rule
        8.4 Conditional and Indirect Proof
        8.5 Proving Invalidity
        8.6 Relational Predicates and Overlapping Quantifiers
        8.7 Identity

##
## Inductive Logic
### 9  Analogy and Legal and Moral Reasoning

        9.1 Analogical Reasoning
        9.2 Legal Reasoning
        9.3 Moral Reasoning

### 10 Causality and Mill's Methods

        10.1 “Cause” and Necessary and Sufficient Conditions
        10.2 Mill's Five Methods
        10.3 Mill's Methods and Science

### 11 Probability

        11.1 Theories of Probability
        11.2 The Probability Calculus

### 12 Statistical Reasoning

        12.1 Evaluating Statistics
        12.2 Samples
        12.3 The Meaning of “Average”
        12.4 Dispersion
        12.5 Graphs and Pictograms
        12.6 Percentages

### 13 Hypothetical/Scientific Reasoning

        13.1 The Hypothetical Method
        13.2 Hypothetical Reasoning: Four Examples from Science
        13.3 The Proof of Hypotheses
        13.4 The Tentative Acceptance of Hypotheses

### 14 Science and Superstition

        14.1 Distinguishing Between Science and Superstition
        14.2 Evidentiary Support
        14.3 Objectivity
        14.4 Integrity
        14.5 Concluding Remarks

##
# propositional logic

        p > (p > p)
        T T  T T T
        F T  F T F
          ^
          tautology


        [(p > q) > q] > p
          T T T  T T  T T
          T F F  T F  T T
          F T T  T T  F F
          F T F  F F  T F
                      ^
                      contingent


        [(p > q) & (p v q)] > q
          T T T  T  T T T   T T
          T F F  F  T T F   T F
          F T T  T  F T T   T T
          F T F  F  F F F   T F
                            ^
                            tautology


        [p & (q v r)] ≡ [(~ q v ~ p) & (~ r v ~ p)]
         T T  T T T   F   F T F F T  F  F T F F T
         T T  T T F   F   F T F F T  F  T F T F T
         T T  F T T   F   T F T F T  F  F T F F T
         T F  F F F   F   T F T F T  T  T F T F T
         F F  T T T   F   F T T T F  T  F T T T F
         F F  T T F   F   F T T T F  T  T F T T F
         F F  F T T   F   T F T T F  T  F T T T F
         F F  F F F   F   T F T T F  T  T F T T F
                      ^
                      contradictoire

