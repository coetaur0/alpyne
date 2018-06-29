"""
Adt for the String Sort.
"""
# Aurelien Coet, 2018.

from alpynet.adt import Sort, GenericSort
from alpynet.adts.boolean import boolean


chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
          'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
          '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '_']


# ---------------------------------------- #
# Definition of the character sort.
# ---------------------------------------- #

char = Sort('char')


# ---------- Operations on characters ---------- #
# Generators.
for i, c in enumerate(chars):
    char.operation(c, ())
    if i < 26:
        char.operation(c.upper(), ())

# Observer.
char.operation('equal', (char, char), boolean)


# ---------- Character variables ---------- #
char.variable('c1')
char.variable('c2')


# ---------- Rewrite rules on characters ---------- #
for i, c in enumerate(chars):
    if i < 26:
        c_upper = c.upper()
    else:
        c_upper = None

    for j, c2 in enumerate(chars):
        if j < 26:
            c2_upper = c2.upper()
        else:
            c2_upper = None

        if c == c2:
            rhs = boolean.true()
        else:
            rhs = boolean.false()
        char.rewrite_rule(char.equal(char.__dict__[c](),
                                     char.__dict__[c2]()),
                          rhs)

        if c_upper:
            if c_upper == c2:
                rhs = boolean.true()
            else:
                rhs = boolean.false()
            char.rewrite_rule(char.equal(char.__dict__[c_upper](),
                                         char.__dict__[c2]()),
                              rhs)

        if c2_upper:
            if c == c2_upper:
                rhs = boolean.true()
            else:
                rhs = boolean.false()
            char.rewrite_rule(char.equal(char.__dict__[c](),
                                         char.__dict__[c2_upper]()),
                              rhs)

        if c_upper and c2_upper:
            if c_upper == c2_upper:
                rhs = boolean.true()
            else:
                rhs = boolean.false()
            char.rewrite_rule(char.equal(char.__dict__[c_upper](),
                                         char.__dict__[c2_upper]()),
                              rhs)


# ---------------------------------------- #
# Definition of the string sort.
# ---------------------------------------- #
string = Sort('str')


# ---------- Operations on strings ---------- #
# Generators.
string.operation('empty', ())
string.operation('append', (string, char))
string.operation('concat', (string, string))

# Observers.
string.operation('equal', (string, string), boolean)


# ---------- String variables ---------- #
string.variable('s')
string.variable('t')


# ---------- Rewrite rules on strings ---------- #
string.rewrite_rules += char.rewrite_rules

# equal(empty, empty) -> true.
string.rewrite_rule(string.equal(string.empty(), string.empty()),
                    boolean.true())

# equal(empty, append(s, c)) -> false.
string.rewrite_rule(string.equal(string.empty(),
                                 string.append(string.s(), char.c1())),
                    boolean.false())

# equal(append(s, c), empty) -> false.
string.rewrite_rule(string.equal(string.append(string.s(), char.c1()),
                                 string.empty()),
                    boolean.false())

# equal(append(s, c), append(t, c)) -> equal(s, t).
string.rewrite_rule(string.equal(string.append(string.s(), char.c1()),
                                 string.append(string.t(), char.c1())),
                    string.equal(string.s(), string.t()))

# equal(c, d) == false => equal(append(s, c), append(t, d)) -> false.
string.rewrite_rule(string.equal(string.append(string.s(), char.c1()),
                                 string.append(string.t(), char.c2())),
                    boolean.false(),
                    [(char.equal(char.c1(), char.c2()), boolean.false())])

generic = GenericSort()
generic.operation('equal', (generic, generic))

string.rewrite_rule(generic.equal(string.s(), string.t()),
                    string.equal(string.s(), string.t()))

# TODO: concat rewrite rules.
