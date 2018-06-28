"""
Adt for the Natural Sort.
"""
# Aurelien Coet, 2018.

from alpynet.adt import Sort, GenericSort
from alpynet.adts.boolean import boolean


# Sort Definition.
nat = Sort('nat')


# ---------- Operations on naturals ---------- #
# Generators.
nat.operation('zero', ())
nat.operation('succ', (nat,))

# Modifiers.
nat.operation('add', (nat, nat))

# Observers.
nat.operation('equal', (nat, nat), boolean)


# ---------- Variables ---------- #
nat.variable('x')
nat.variable('y')


# ---------- Rewrite rules ---------- #
# add(x, 0) -> x.
nat.rewrite_rule(nat.add(nat.x(), nat.zero()), nat.x())

# add(x, succ(y)) -> succ(add(x, y)).
nat.rewrite_rule(nat.add(nat.x(), nat.succ(nat.y())),
                 nat.succ(nat.add(nat.x(), nat.y())))

# equal(0, 0) -> true.
nat.rewrite_rule(nat.equal(nat.zero(), nat.zero()),
                 boolean.true())

# equal(succ(x), 0) -> false.
nat.rewrite_rule(nat.equal(nat.succ(nat.x()), nat.zero()),
                 boolean.false())

# equal(0, succ(x)) -> false.
nat.rewrite_rule(nat.equal(nat.zero(), nat.succ(nat.x())),
                 boolean.false())

# equal(succ(x), succ(y)) -> equal(x, y).
nat.rewrite_rule(nat.equal(nat.succ(nat.x()), nat.succ(nat.y())),
                 nat.equal(nat.x(), nat.y()))

generic = GenericSort()
generic.operation('equal', (generic, generic))

nat.rewrite_rule(generic.equal(nat.x(), nat.y()),
                 nat.equal(nat.x(), nat.y()))
