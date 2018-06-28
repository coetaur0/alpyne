"""
Adt for the Boolean Sort.
"""
# Aurelien Coet, 2018.

from alpynet.adt import Sort, GenericSort

# Sort Definition.
boolean = Sort('bool')

# ---------- Operations on booleans ---------- #
# Generators.
boolean.operation('true', ())
boolean.operation('false', ())

# Modifiers.
boolean.operation('not_', (boolean,))
boolean.operation('and_', (boolean, boolean))
boolean.operation('or_', (boolean, boolean))

# Observers.
boolean.operation('equal', (boolean, boolean))


# ---------- Variables ---------- #
boolean.variable('b')
boolean.variable('c')


# ---------- Rewrite rules ---------- #
# not(true) -> false.
boolean.rewrite_rule(boolean.not_(boolean.true()), boolean.false())

# not(false) -> true.
boolean.rewrite_rule(boolean.not_(boolean.false()), boolean.true())

# and(b, false) -> false.
boolean.rewrite_rule(boolean.and_(boolean.b(), boolean.false()),
                     boolean.false())

# and(b, true) -> b.
boolean.rewrite_rule(boolean.and_(boolean.b(), boolean.true()),
                     boolean.b())

# or(b, false) -> b.
boolean.rewrite_rule(boolean.or_(boolean.b(), boolean.false()),
                     boolean.b())

# or(b, true) -> true.
boolean.rewrite_rule(boolean.or_(boolean.b(), boolean.true()),
                     boolean.true())

generic = GenericSort()
generic.operation('equal', (generic, generic))

boolean.rewrite_rule(generic.equal(boolean.b(), boolean.c()),
                     boolean.equal(boolean.b(), boolean.c()))
