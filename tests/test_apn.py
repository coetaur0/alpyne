import unittest
from alpyne.adt import Sort
from alpyne.apn import Place, Transition, Arc, AlgebraicPetriNet
from alpyne.exceptions import ConsumeException, FiringException


class TestPlace(unittest.TestCase):

    def test_instanciation(self):
        sort = Sort('sort')
        sort.operation('const', ())
        with self.assertRaises(AssertionError):
            Place(2, sort)  # Name of place must be a string.
            Place('place', 2)  # Sort of place must be a sort.
            Place('place', sort, [2])  # Marking must be a list of terms.

        place = Place('place', sort, [sort.const()])
        self.assertEqual(place.name, 'place')
        self.assertEqual(place.sort, sort)
        self.assertEqual(place.marking, [sort.const()])

    def test_str_representation(self):
        sort = Sort('sort')
        place = Place('place', sort)
        self.assertEqual(str(place), "place place")

    def test_consume(self):
        sort = Sort('sort')
        sort.operation('op', (sort,))
        sort.operation('const', ())
        place = Place('place', sort, [sort.const()])

        with self.assertRaises(AssertionError):
            place.consume([2])  # Tokens to consume must be a list of terms.

        with self.assertRaises(ConsumeException):
            # An error is raised when an attempt is made to consume tokens
            # absent from the place.
            place.consume([sort.op(sort.const())])

        self.assertEqual(place.marking, [sort.const()])
        place.consume([sort.const()])
        self.assertEqual(place.marking, [])

    def test_produce(self):
        sort = Sort('sort')
        sort.operation('const', ())
        place = Place('place', sort)

        with self.assertRaises(AssertionError):
            sort2 = Sort('sort2')
            sort2.operation('const', ())
            place.produce([2])  # Tokens produced in a place must be terms.
            # Tokens produced in a place must have the same sort as the place.
            place.produce([sort2.const()])

        self.assertEqual(place.marking, [])
        place.produce([sort.const()])
        self.assertEqual(place.marking, [sort.const()])


class TestTransition(unittest.TestCase):

    def test_instanciation(self):
        with self.assertRaises(AssertionError):
            Transition(2)  # Name of transition must be a string.
        t = Transition('t')
        self.assertEqual(t.name, 't')

    def test_str_representation(self):
        t = Transition('t')
        self.assertEqual(str(t), 'transition t')

    def test_inbound_arc(self):
        sort = Sort('sort')
        sort.operation('const', ())
        p = Place('p', sort, [sort.const()])
        t = Transition('t')

        with self.assertRaises(AssertionError):
            t.inbound_arc(2, [sort.const()])  # Source of arc must be a place.
            t.inbound_arc(p, [2])  # Label must be a list of terms.

        t.inbound_arc(p, [sort.const()])
        self.assertEqual(len(t.inbound_arcs), 1)
        self.assertEqual(type(t.inbound_arcs[0]), Arc)

    def test_outbound_arc(self):
        sort = Sort('sort')
        sort.operation('const', ())
        p = Place('p', sort, [sort.const()])
        t = Transition('t')

        with self.assertRaises(AssertionError):
            t.outbound_arc(2, [sort.const()])  # Target of arc must be a place.
            t.outbound_arc(p, [2])  # Label must be a list of terms.

        t.outbound_arc(p, [sort.const()])
        self.assertEqual(len(t.outbound_arcs), 1)
        self.assertEqual(type(t.outbound_arcs[0]), Arc)

    def test_fireable(self):
        sort = Sort('sort')
        sort.operation('op', (sort,))
        sort.operation('const', ())
        sort.variable('x')
        p = Place('p', sort, [sort.const()])
        t1 = Transition('t1')
        t2 = Transition('t2')
        t1.inbound_arc(p, [sort.x()])
        t2.inbound_arc(p, [sort.op(sort.const())])

        fireable, binding = t1.fireable()
        self.assertEqual(fireable, True)
        self.assertEqual(binding[sort.x], sort.const())

        fireable, _ = t2.fireable()
        self.assertEqual(fireable, False)

    def test_fire(self):
        sort = Sort('sort')
        sort.operation('op', (sort,))
        sort.operation('const', ())
        sort.variable('x')
        p1 = Place('p1', sort, [sort.const()])
        p2 = Place('p2', sort, [])
        t1 = Transition('t1')
        t2 = Transition('t2')
        t1.inbound_arc(p1, [sort.x()])
        t1.outbound_arc(p2, [sort.x()])
        t2.inbound_arc(p1, [sort.op(sort.const())])

        with self.assertRaises(FiringException):
            t2.fire()

        self.assertEqual(p1.marking, [sort.const()])
        self.assertEqual(p2.marking, [])
        t1.fire()
        self.assertEqual(p1.marking, [])
        self.assertEqual(p2.marking, [sort.const()])


class TestArc(unittest.TestCase):

    def test_instanciation(self):
        sort = Sort('sort')
        sort.operation('const', ())
        p = Place('p', sort, [sort.const()])
        t = Transition('t')

        with self.assertRaises(AssertionError):
            # Source of an arc must be a Place or Transition.
            Arc(2, t, [sort.const()])
            # Target of an arc must be a Place or Transition.
            Arc(p, 2, [sort.const()])
            # Label of arc must be a list of terms.
            Arc(p, t, [2])

        a1 = Arc(p, t, [sort.const()])
        self.assertEqual(a1.source, p)
        self.assertEqual(a1.target, t)
        self.assertEqual(a1.label, [sort.const()])

    def test_str_representation(self):
        sort = Sort('sort')
        sort.operation('const', ())
        p = Place('p', sort, [sort.const()])
        t = Transition('t')
        a = Arc(p, t, [sort.const()])
        self.assertEqual(str(a), 'arc from place p to transition t, with label\
 [sort.const(), ]')


class TestAlgebraicPetriNet(unittest.TestCase):

    def test_instanciation(self):
        sort = Sort('sort')
        sort.operation('const', ())
        p = Place('p', sort, [sort.const()])
        t = Transition('t')

        with self.assertRaises(AssertionError):
            AlgebraicPetriNet(2)  # Name of APN must be a string.
            # Places of APN must be instances of Place.
            AlgebraicPetriNet('apn', [2], [t])
            # Transitions of APN must be instances of Transition.
            AlgebraicPetriNet('apn', [p], [2])

        apn = AlgebraicPetriNet('apn', [p], [t])
        self.assertEqual(apn.name, 'apn')
        self.assertEqual(apn.places, [p])
        self.assertEqual(apn.transitions, [t])

    def test_str_representation(self):
        apn = AlgebraicPetriNet('apn')
        self.assertEqual(str(apn), 'Algebraic Petri Net apn')

    def test_add_place(self):
        sort = Sort('sort')
        sort.operation('const', ())
        apn = AlgebraicPetriNet('apn')

        with self.assertRaises(AssertionError):
            apn.add_place(2, sort)  # Name of place must be a string.
            apn.add_place('p', 2)  # Sort of place must be a sort.
            apn.add_place('p', sort, [2])  # Marking must be a list of terms.

        p = apn.add_place('p', sort, [sort.const()])
        self.assertEqual(len(apn.places), 1)
        self.assertEqual(type(apn.places[0]), Place)
        self.assertEqual(apn.places[0], p)

    def test_add_transition(self):
        apn = AlgebraicPetriNet('apn', [], [])

        with self.assertRaises(AssertionError):
            apn.add_transition(2)  # Name of transition must be a string.

        t = apn.add_transition('t')
        self.assertEqual(len(apn.transitions), 1)
        self.assertEqual(type(apn.transitions[0]), Transition)
        self.assertEqual(apn.transitions[0], t)

    def test_add_arc(self):
        sort = Sort('sort')
        sort.operation('const', ())
        apn = AlgebraicPetriNet('apn', [], [])
        p = apn.add_place('p', sort, [sort.const()])
        t = apn.add_transition('t')

        with self.assertRaises(AssertionError):
            # Source of an arc must be a Place or Transition.
            apn.add_arc(2, t, [])
            # Target of an arc must be a Place or Transition.
            apn.add_arc(p, 2, [])
            # Label of an arc must be a list of terms.
            apn.add_arc(p, t, [2])

        apn.add_arc(p, t, [sort.const()])
        apn.add_arc(t, p, [sort.const()])
        self.assertEqual(len(t.inbound_arcs), 1)
        self.assertEqual(len(t.outbound_arcs), 1)

    def test_marking(self):
        sort = Sort('sort')
        sort.operation('const', ())
        apn = AlgebraicPetriNet('apn', [], [])
        p = apn.add_place('p', sort, [sort.const()])

        markings = apn.marking()
        self.assertEqual(len(markings), 1)
        self.assertEqual(markings[p], [sort.const()])

    def test_fireables(self):
        sort = Sort('sort')
        sort.operation('op', (sort,))
        sort.operation('const', ())
        apn = AlgebraicPetriNet('apn', [], [])
        p = apn.add_place('p', sort, [sort.const()])
        t1 = apn.add_transition('t1')
        t2 = apn.add_transition('t2')
        apn.add_arc(p, t1, [sort.const()])
        apn.add_arc(p, t2, [sort.op(sort.const())])

        fireables = apn.fireables()
        self.assertEqual(len(fireables), 1)
        self.assertEqual(fireables[0], t1)

    def test_fire(self):
        sort = Sort('sort')
        sort.operation('op', (sort,))
        sort.operation('const', ())
        apn = AlgebraicPetriNet('apn', [], [])
        p = apn.add_place('p', sort, [sort.const()])
        t1 = apn.add_transition('t1')
        t2 = apn.add_transition('t2')
        apn.add_arc(p, t1, [sort.const()])
        apn.add_arc(p, t2, [sort.op(sort.const())])

        with self.assertRaises(FiringException):
            apn.fire(t2)

        self.assertEqual(p.marking, [sort.const()])
        apn.fire(t1)
        self.assertEqual(p.marking, [])

    def test_fire_random(self):
        sort = Sort('sort')
        sort.operation('op', (sort,))
        sort.operation('const', ())
        apn = AlgebraicPetriNet('apn', [], [])
        p = apn.add_place('p', sort, [sort.const()])
        t1 = apn.add_transition('t1')
        t2 = apn.add_transition('t2')
        apn.add_arc(p, t1, [sort.const()])
        apn.add_arc(p, t2, [sort.op(sort.const())])

        self.assertEqual(p.marking, [sort.const()])
        apn.fire_random()
        self.assertEqual(p.marking, [])


if __name__ == "__main__":
    unittest.main()
