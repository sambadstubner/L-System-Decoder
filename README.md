# L-System Decoder

This script attempts to find all rulesets of a deterministic L-System given at least two generations of output string.


## Usage

```bash
python decode.py [filepath]
```

The input file should be a text file representing at least two generations of the system separated by a new line. You can see many examples at l_systems/output


## Explanation
### Splitting
The crux of the finding rules to an L-System is effectively assigning groups of characters to single characters in the previous generation. As letters are repeated in a previous generation, corresponding groups of characters should also be repeated in the next generation as well.

Example:
Provided these two generations of basic algae L-System
```
AB
ABA
```
Because there are two characters in the previous generation, we must split the following generation twice. There are two possible ways to split the second generation.
```
AB, A    and    A, BA
```
This means that there are two possible sets of rules given these two generations.
```
A -> AB         or          A -> A
B -> A                      B -> BA
```
If the next generation is
```
ABA (previous generation)
ABAAB
```
We know it must grouped into three sets of characters.
```
A, B, AAB
A, BA, AB
A, BAA, B
AB, A, AB
...
```

However the first and last group of characters must be the same because the character A is repeated in the first generation. This meaning that the only valid way to split ABAAB is
```
AB, A, AB
```
This means that the rules for this L-System is:
```
A -> AB
B -> A
```
### Optimizing
It can be very intensive to iterate through all possible way to split a string a given number of ways so it is important that we check if a set of groups is valid as we split a string and stop the iteration immediately when is not valid.

To minimize the amount of generations needed to be split, after a set of possible rules are generated, we check to see if it applies to all generations. This is done by applying the rules to each generation and comparing it with the input generations. If the rules can correctly replicate the input, then it is a valid ruleset and there is no need to decode future generations.

In some more complex L-Systems, rules only apply on alternating generations or don't apply until much later. In this scenario, we keep track of previously found possible solutions. When a new set of solutions are found, we keep the previous solutions that do not contradict newly found solutions, and update the rule sets with the new information found.

