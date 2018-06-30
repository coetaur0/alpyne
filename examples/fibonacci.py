#!usr/bin/python3

from alpynet.adts.natural import nat
from alpynet.apn import AlgebraicPetriNet


# Useful variables.
nat.variable("a")
nat.variable("b")

# Creation of an APN.
fib = AlgebraicPetriNet("fibonacci", rewrite_rules=nat.rewrite_rules)

# Places.
fn_1 = fib.add_place("f_n-1", nat, [nat.zero()])
fn = fib.add_place("f_n", nat, [nat.succ(nat.zero())])

# Transitions.
t = fib.add_transition('t')

# Arcs.
fib.add_arc(fn_1, t, [nat.a()])
fib.add_arc(t, fn_1, [nat.b()])
fib.add_arc(fn, t, [nat.b()])
fib.add_arc(t, fn, [nat.add(nat.a(), nat.b())])

# Visualisation before and after the firing of a transition.
fib.visualise('init_state')

print("Fireable transitions:")
for t in fib.fireables():
    print(t)
fib.fire_random()

fib.visualise('after_fire')
