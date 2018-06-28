"""
Adt for the Map Sort.
"""
# Aurelien Coet, 2018.

from alpynet.adt import Sort, GenericSort
from alpynet.adts.boolean import boolean


# Sort Definition.
kv_map = Sort('map')
generic = GenericSort()


# ---------- Operations on maps ---------- #
# Generators.
kv_map.operation('empty', ())
kv_map.operation('add', (kv_map, generic, generic))

# Observers.
kv_map.operation('get', (kv_map, generic))
kv_map.operation('isempty', (kv_map,), boolean)

# Modifiers.
kv_map.operation('delete', (kv_map, generic))

# Operations for the generic sort.
generic.operation('equal', (generic, generic))


# ---------- Variables ---------- #
kv_map.variable('m')
kv_map.variable('n')

# Generic variables for map keys.
generic.variable('k')
generic.variable('l')

# Generic variables for map values.
generic.variable('v')
generic.variable('w')


# ---------- Rewrite rules ---------- #
# isempty(empty) -> true.
kv_map.rewrite_rule(kv_map.isempty(kv_map.empty()),
                    # ->
                    boolean.true())

# isempty(empty, add(m, k, v)) -> false.
kv_map.rewrite_rule(kv_map.isempty(kv_map.add(kv_map.m(),
                                              generic.k(),
                                              generic.v())),
                    # ->
                    boolean.false())

# add(add(m, k, v), k, w) -> add(m, k, w).
kv_map.rewrite_rule(kv_map.add(kv_map.add(kv_map.m(),
                                          generic.k(),
                                          generic.v()),
                               generic.k(), generic.w()),
                    # ->
                    kv_map.add(kv_map.m(), generic.k(), generic.w()))

# equal(k, l) == false and isempty(m) == false
# => add(add(m, k, v), l, w) -> add(add(m, l, w), k, v).
kv_map.rewrite_rule(kv_map.add(kv_map.add(kv_map.m(),
                                          generic.k(),
                                          generic.v()),
                               generic.l(), generic.w()),
                    # ->
                    kv_map.add(kv_map.add(kv_map.m(),
                                          generic.l(),
                                          generic.w()),
                               generic.k(), generic.v()),
                    # Conditions:
                    [(generic.equal(generic.k(), generic.l()), boolean.false()),
                     (kv_map.isempty(kv_map.m()), boolean.false())])

# get(add(m, k, v), k) -> v.
kv_map.rewrite_rule(kv_map.get(kv_map.add(kv_map.m(),
                                          generic.k(),
                                          generic.v()),
                                generic.k()),
                    # ->
                    generic.v())

# equal(k, l) == false and isempty(m) == false
# => get(add(m, k, v), l) -> get(m, l).
kv_map.rewrite_rule(kv_map.get(kv_map.add(kv_map.m(),
                                          generic.k(),
                                          generic.v()),
                                generic.l()),
                    # ->
                    kv_map.get(kv_map.m(), generic.l()),
                    # Conditions:
                    [(generic.equal(generic.k(), generic.l()),
                      boolean.false()),
                     (kv_map.isempty(kv_map.m()), 
                      boolean.false())])

# equal(k, l) == false and isempty(m) == true
# => get(add(m, k, v), l) -> empty.
kv_map.rewrite_rule(kv_map.get(kv_map.add(kv_map.m(),
                                          generic.k(),
                                          generic.v()),
                                generic.l()),
                    # ->
                    kv_map.empty(),
                    # Conditions:
                    [(generic.equal(generic.k(), generic.l()),
                      boolean.false()),
                     (kv_map.isempty(kv_map.m()), 
                      boolean.true())])

# delete(add(m, k, v), k) -> m.
kv_map.rewrite_rule(kv_map.delete(kv_map.add(kv_map.m(),
                                             generic.k(),
                                             generic.v()),
                                  generic.k()),
                    # ->
                    kv_map.m())

# equal(k, l) == false and isempty(m) == false
# => delete(add(m, k, v), l) -> add(delete(m, l), k, v).
kv_map.rewrite_rule(kv_map.delete(kv_map.add(kv_map.m(),
                                             generic.k(),
                                             generic.v()),
                                  generic.l()),
                    # ->
                    kv_map.add(kv_map.delete(kv_map.m(), generic.l()),
                               generic.k(), generic.v()),
                    # Conditions:
                    [(generic.equal(generic.k(), generic.l()), 
                      boolean.false()),
                     (kv_map.isempty(kv_map.m()),
                      boolean.false())])

# equal(k, l) == false and isempty(m) == true
# => delete(add(m, k, v), l) -> add(delete(m, l), k, v).
kv_map.rewrite_rule(kv_map.delete(kv_map.add(kv_map.m(),
                                             generic.k(),
                                             generic.v()),
                                  generic.l()),
                    # ->
                    kv_map.m(),
                    # Conditions:
                    [(generic.equal(generic.k(), generic.l()),
                      boolean.false()),
                     (kv_map.isempty(kv_map.m()),
                      boolean.true())])
