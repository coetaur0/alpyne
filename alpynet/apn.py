"""
Model for Algebraic Petri Nets (APNs).
"""
# Aurelien Coet, 2018.

import random
import graphviz as gv
from alpynet.adt import Sort, Term, RewriteRule
from alpynet.exceptions import ConsumeException, FiringException


class Place(object):
    """
    Place in an algebraic petri net (APN).
    """

    def __init__(self, name, sort, marking=[]):
        assert type(name) == str, "Name of a place must be a string"
        assert isinstance(sort, Sort), "Sort of a place must be a sort"
        assert type(marking) == list, "Initial marking must be a list"
        for token in marking:
            assert isinstance(token, Term), "Tokens in a place must be terms"
            assert token.sort == sort, "Tokens' sorts must match the place's"
        self.name = name
        self.sort = sort
        self.marking = marking

    def __str__(self):
        return "place {}".format(self.name)

    def consume(self, tokens):
        """
        Consume tokens from the place.

        Args:
            tokens: A list of tokens to consume from the place.
        """
        assert type(tokens) == list, "Tokens must be a list of terms"
        new_marking = self.marking.copy()
        for token in tokens:
            assert isinstance(token, Term), "Tokens must be terms"
            if token not in self.marking:
                raise ConsumeException
            new_marking.remove(token)
        self.marking = new_marking

    def produce(self, tokens):
        """
        Produce tokens in the place.

        Args:
            tokens: A list of tokens to produce in the place.
        """
        assert type(tokens) == list, "Tokens must be a list of terms"
        new_marking = self.marking.copy()
        for token in tokens:
            assert isinstance(token, Term), "Tokens must be terms"
            assert token.sort == self.sort, "Tokens must have the place's sort"
            new_marking.append(token)
        self.marking = new_marking


class Transition(object):
    """
    Transition in an algebraic petri net (APN).
    """

    def __init__(self, name):
        assert type(name) == str, "Name of a transition must be a string"
        self.name = name
        self.inbound_arcs = []
        self.outbound_arcs = []

    def __str__(self):
        return "transition {}".format(self.name)

    def inbound_arc(self, source, label):
        """
        Add an arc to the list of inbound arcs of the transition.

        Args:
            arc: The arc to add to the list.
        """
        assert isinstance(source, Place), "Source of arc must be a place"
        assert type(label) == list, "Label must be a list of terms"
        for term in label:
            assert isinstance(term, Term), "Elements in label must be terms"
        self.inbound_arcs.append(Arc(source, self, label))

    def outbound_arc(self, target, label):
        """
        Add an arc to the list of outbound arcs of the transition.

        Args:
            arc: The arc to add to the list.
        """
        assert isinstance(target, Place), "Target of arc must be a place"
        assert type(label) == list, "Label must be a list of terms"
        for term in label:
            assert isinstance(term, Term), "Elements in label must be terms"
        self.outbound_arcs.append(Arc(self, target, label))

    def fireable(self):
        """
        Check if the transition is fireable, and if so, compute the variable
        bindings that make it possible.

        Returns:
            A boolean indicating whether the transition can be fired,
            as well as the bindings for the variables in the labels
            of its inbound and outbound arcs if it can be fired.
        """
        bindings = {}
        matched_tokens = []

        for arc in self.inbound_arcs:
            has_match = False

            for term in arc.label:
                for token in arc.source.marking:
                    # If a token in a precondition is already being consumed by
                    # some other term on an inbound arc, it cannot be consumed
                    # a second time.
                    if token in matched_tokens:
                        continue

                    (matching, binding) = term.match(token)
                    if matching:
                        has_match = True
                        for key, value in binding.items():
                            # If there is some conflict in the variable
                            # bindings, the transition cannot be fired.
                            if key in bindings and bindings[key] != value:
                                has_match = False
                            else:
                                bindings[key] = value
                                matched_tokens.append(term)
                        break

                if has_match is False:
                    return (False, {})

        return (True, bindings)

    def _consume_inbound(self, bindings, rewrite_rules):
        """
        Consume tokens from the places connected to the inbound arcs of the
        transition.

        Args:
            bindings: A dict of variable bindings to be applied to the terms
                on the labels of the inbound arcs of the transition.
            rewrite_rules: A list of rewrite rules to be used to reduce the
                terms on the labels of the inbound arcs of the transition.
        """
        for arc in self.inbound_arcs:
            tokens = []
            for term in arc.label:
                tokens.append(term.apply_binding(bindings)
                                  .reduce(rewrite_rules))
            arc.source.consume(tokens)

    def _produce_outbound(self, bindings, rewrite_rules):
        """
        Produce tokens in the places connected to the outbound arcs of the
        transition.

        Args:
            bindings: A dict of variable bindings to be applied to the terms
                on the labels of the outbound arcs of the transition.
            rewrite_rules: A list of rewrite rules to be used to reduce the
                terms on the labels of the outbound arcs of the transition.
        """
        for arc in self.outbound_arcs:
            tokens = []
            for term in arc.label:
                tokens.append(term.apply_binding(bindings)
                                  .reduce(rewrite_rules))
            arc.target.produce(tokens)

    def fire(self, rewrite_rules=[]):
        """
        Fire the transition. Consumes tokens in the preconditions of the
        transition, and produces new ones in its postconditions. If there
        are statements inside the transition, those are evaluated, and
        their associated contexts are updated accordingly in the variable
        bindings for the arcs of the transition.

        Args:
            rewrite_rules: A list of rewrite rules to use to reduce the
                terms on the inbound and outbound arcs of the transition.

        Raises:
            A FiringException when the transition cannot be fired.
        """
        fireable, bindings = self.fireable()

        if fireable is False:
            raise FiringException

        self._consume_inbound(bindings, rewrite_rules)
        self._produce_outbound(bindings, rewrite_rules)


class Arc(object):
    """
    Arc between places and transitions in an algebraic petri net (APN).
    """

    def __init__(self, source, target, label):
        assert isinstance(source, Place) or isinstance(source, Transition),\
            "Source of an arc must be a place or transition"
        assert isinstance(target, Place) or isinstance(target, Transition),\
            "Target of an arc must be a place or transition"
        assert type(label) == list, "Label of an arc must be a list of terms"
        for term in label:
            assert isinstance(term, Term), "Content of the label must be terms"
        self.source = source
        self.target = target
        self.label = label

    def __str__(self):
        txt = "arc from {} to {}, with label [".format(self.source,
                                                       self.target)
        for term in self.label:
            txt += str(term) + ', '
        txt += "]"
        return txt


class AlgebraicPetriNet(object):
    """
    Algebraic Petri Net (APN).
    """

    def __init__(self, name, places=[], transitions=[], rewrite_rules=[]):
        assert type(name) == str, "Name of an APN must be a string"
        assert type(places) == list, "Places must be a list of Places"
        for place in places:
            assert isinstance(place, Place),\
                "Places must be instances of Place"
        assert type(transitions) == list,\
            "Transitions must be a list of transitions"
        for transition in transitions:
            assert isinstance(transition, Transition),\
                "Transitions must be instances of Transition"
        for rule in rewrite_rules:
            assert isinstance(rule, RewriteRule),\
                "Rewrite rules in the APN must be instances of RewriteRule"
        self.name = name
        self.places = places
        self.transitions = transitions
        self.rewrite_rules = rewrite_rules

    def __str__(self):
        return "Algebraic Petri Net {}".format(self.name)

    def add_place(self, name, sort, marking=[]):
        """
        Add a place to the APN.

        Args:
            name: The name of the place.
            sort: The sort of the place.
            marking: A list of terms representing the initial marking of the
                place.

        Returns:
            The newly created place.
        """
        place = Place(name, sort, marking)
        self.places.append(place)
        return place

    def add_transition(self, name):
        """
        Add a transition to the APN.

        Args:
            name: The name of the transition.

        Returns:
            The newly created transition.
        """
        transition = Transition(name)
        self.transitions.append(transition)
        return transition

    def add_arc(self, source, target, label=[]):
        """
        Add an arc to the APN.

        Args:
            source: The source of the arc (a Place or a Transition).
            target: The target of the arc (a Place or a Transition).
            label: The label for the arc (a list of terms).
        """
        assert isinstance(source, Place) or isinstance(source, Transition),\
            "Source of an arc must be a Place or Transition"
        assert isinstance(target, Place) or isinstance(target, Transition),\
            "Target of an arc must be a Place or transition"
        assert type(source) != type(target),\
            "Source and target of an arc cannot be both Places or Transitions"
        if isinstance(source, Place):
            assert source in self.places, "Source must exist in the APN"
            assert target in self.transitions, "Target must exist in the APN"
            target.inbound_arc(source, label)
        else:
            assert source in self.transitions, "Source must exist in the APN"
            assert target in self.places, "Target must exist in the APN"
            source.outbound_arc(target, label)

    def marking(self):
        """
        Get the markings of the places of the APN.

        Returns:
            A dict with the places of the APN as keys and their markings as
            values.
        """
        markings = {}
        for place in self.places:
            markings[place] = place.marking
        return markings

    def fireables(self):
        """
        Get the list of transitions that are fireable in the APN given its
        current marking.

        Returns:
            A list of transitions that can be fired.
        """
        fireables = []
        for transition in self.transitions:
            fireable, _ = transition.fireable()
            if fireable:
                fireables.append(transition)
        return fireables

    def fire(self, transition):
        """
        Fire a transition in the APN.

        Args:
            transition: The transition to fire in the APN.
        """
        assert transition in self.transitions, "Transition must be in the APN"
        transition.fire(self.rewrite_rules)

    def fire_random(self):
        """
        Randomly fire one of the fireable transitions of the APN.
        """
        random.choice(self.fireables()).fire(self.rewrite_rules)

    def visualise(self, filepath, format='pdf'):
        """
        Visualise the APN and its current marking graphically.

        Args:
            filepath: The path to the file where the visualisation of the APN
                must be saved.
            format: The format in which the visualisation must be saved.
        """
        graph = gv.Digraph(name=self.name, format=format,
                           graph_attr={'label': self.name})

        for place in self.places:
            label = ""
            for token in place.marking:
                label += str(token) + '\n'
            graph.node(place.name, label=label,
                       _attributes={'forcelabels': 'true',
                                    'xlabel': place.name})

        for transition in self.transitions:
            graph.node(transition.name, label=transition.name,
                       _attributes={'shape': 'box'})

            for arc in transition.inbound_arcs:
                label = ""
                for term in arc.label:
                    label += str(term) + '\n'
                graph.edge(arc.source.name, arc.target.name, label=label)

            for arc in transition.outbound_arcs:
                label = ""
                for term in arc.label:
                    label += str(term) + '\n'
                graph.edge(arc.source.name, arc.target.name, label=label)

        graph.render(filepath, view=True)
