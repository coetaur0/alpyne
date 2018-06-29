"""
Model for Algebraic Data Types (ADTs) and terms.
"""
# Aurelien Coet, 2018.


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls)\
                                    .__call__(*args, **kwargs)
        return cls._instances[cls]


class Sort(object):
    """
    Sort in an ADT.

    A sort has operations and variables defined on it. Those can be used to
    define terms of the sort. It also has rewrite rules associated to it.
    """

    def __init__(self, name):
        assert type(name) == str, "Name of a sort must be a string"
        self.name = name
        self.rewrite_rules = []

    def __str__(self):
        return self.name

    def operation(self, name, signature, sort=None):
        """
        Create a new operation on the sort. The operation is stored in
        the sort's attributes.

        Args:
            name: The name of the operation.
            signature: The signature of the operation (the list of sorts it
                       takes as input).
            sort: The sort of the result of the operation. Defaults to self
                (the sort to which the operation is attached).
        """
        assert type(name) == str, "Name of an operation must be a string"
        assert type(signature) == tuple, "Signature must be a tuple of sorts"
        for s in signature:
            assert isinstance(s, Sort), "Signature must be a tuple of sorts"
        if sort is None:
            sort = self
        assert isinstance(sort, Sort), "Sort of the operation must be a sort"
        self.__dict__[name] = Operation(name, signature, sort)

    def variable(self, name):
        """
        Create a new variable of the sort represented by the object. The
        variable is stored in the sort's attributes.

        Args:
            name: The name of the variable.
        """
        assert type(name) == str, "Name of a variable must be a string"
        self.__dict__[name] = Variable(name, self)

    def rewrite_rule(self, lhs, rhs, conditions=[]):
        """
        Create a new rewrite rule for the sort.

        Args:
            lhs: The left hand side of the rule.
            rhs: The right hand side of the rule.
            condition: The condition of the rule.
        """
        assert isinstance(lhs, Term),\
            "Left hand side of the rule must be a term"
        assert isinstance(rhs, Term),\
            "Right hand side of the rule must be a term"
        assert type(conditions) == list,\
            "Conditions must be a list of conditions"
        for condition in conditions:
            assert len(condition) == 2, "Conditions must contain 2 terms"
            assert isinstance(condition[0], Term),\
                "Conditions must contain terms"
            assert isinstance(condition[1], Term),\
                "Conditions must contain terms"
        self.rewrite_rules.append(RewriteRule(lhs, rhs, conditions))


class GenericSort(Sort, metaclass=Singleton):
    """
    Generic sort in an ADT.

    Represents any sort. Shouldn't be used to define a specific sort with
    operations and variables. It is just a placeholder for any other sort in
    the definition of an operation's arguments and to define terms that can
    be of any sort.
    """

    def __init__(self):
        super().__init__('anysort')


class Operation(object):
    """
    Operation in an ADT.

    An operation is similar to a function that takes arguments of
    given sorts as input and returns a value of a given sort.
    """

    def __init__(self, name, signature, sort):
        assert type(name) == str, "Name of an operation must be a string"
        assert type(signature) == tuple,\
            "Signature of an operation must be a tuple of sorts"
        for s in signature:
            assert isinstance(s, Sort),\
                "Signature of an operation must be a tuple of sorts"
        assert isinstance(sort, Sort),\
            "Sort of the operation must be an instance of Sort"
        self.name = name
        self.signature = signature
        self.sort = sort

    def __eq__(self, other):
        if type(other) != Operation:
            return False

        for attr, value in self.__dict__.items():
            if value != other.__dict__[attr]:
                return False

        return True

    def __str__(self):
        txt = "{}.{}(".format(self.sort, self.name)
        for s in self.signature:
            txt += "{}, ".format(str(s))
        txt += ") -> {}".format(self.sort)
        return txt

    def __repr__(self):
        return str(self)

    def __call__(self, *args):
        return Term(self, args)


class Variable(object):
    """
    Variable of a given sort in an ADT.

    A variable is an expression that can be replaced by any value of its sort
    in a term.
    """

    def __init__(self, name, sort):
        assert type(name) == str, "Name of a variable must be a string"
        assert isinstance(sort,  Sort),\
            "Sort associated to a variable must be an instance of Sort"
        self.name = name
        self.sort = sort

    def __str__(self):
        return "{}.{}".format(str(self.sort), self.name)

    def __repr__(self):
        return str(self)

    def __call__(self):
        return Term(self)


class Term(object):
    """
    Term in an ADT.
    """

    def __init__(self, head, args=()):
        assert isinstance(head, Operation) or isinstance(head, Variable),\
            "Head of a term must be a variable or an operation"
        if type(head) == Operation:
            assert type(args) == tuple,\
                "Arguments of an operation in a term must be a tuple of terms"
            for i, arg in enumerate(args):
                assert isinstance(arg, Term),\
                    "Arguments of an operation must be terms"
                if type(head.signature[i]) != GenericSort:
                    assert arg.sort == head.signature[i],\
                        "Arguments sorts must match the head's signature"
        else:
            assert len(args) == 0, "A variable cannot have arguments"

        self.head = head
        self.sort = head.sort
        self.args = args

    def __eq__(self, other):
        if type(other) != Term or other.head != self.head:
            return False

        for i, operand in enumerate(self.args):
            if operand != other.args[i]:
                return False
        return True

    def __neq__(self, other):
        return not self == other

    def __str__(self):
        if type(self.head) == Operation:
            txt = "{}.{}(".format(str(self.head.sort), self.head.name)
            for i, arg in enumerate(self.args):
                txt += "{}".format(str(arg))
                if i < len(self.args)-1:
                    txt += ", "
            txt += ")"
            return txt
        return str(self.head)

    def __repr__(self):
        return str(self)

    def match(self, other):
        """
        Check if two terms match and compute the corresponding variable
        bindings if they do.

        Args:
            other: The term to match this one with.

        Returns:
            A tuple containing a boolean indicating whether the terms
            match, as well as a dict with the variables bindings if
            they do (the dict is empty if they don't).
        """
        assert isinstance(other, Term), "Other must be another term"

        if type(self.sort) != GenericSort and\
           type(other.sort) != GenericSort and\
           self.sort != other.sort:
            return (False, {})

        if type(self.sort) == GenericSort and\
           type(self.head) == Operation and\
           self.head.name not in other.head.sort.__dict__:
            return (False, {})

        if type(other.sort) == GenericSort and\
           type(other.head) == Operation and\
           other.head.name not in self.head.sort.__dict__:
            return (False, {})

        bindings = {}

        def compare(lhs, rhs):
            if type(lhs.head) == Variable and type(rhs.head) == Variable:
                if (lhs.head in bindings and bindings[lhs.head] != rhs)\
                   or (rhs.head in bindings and bindings[rhs.head] != lhs):
                    return False
                else:
                    bindings[lhs.head] = rhs
                    bindings[rhs.head] = lhs
                    return True

            elif type(lhs.head) == Variable and type(rhs.head) == Operation:
                if lhs.head in bindings and bindings[lhs.head] != rhs:
                    return False
                else:
                    bindings[lhs.head] = rhs
                    return True

            elif type(lhs.head) == Operation and type(rhs.head) == Variable:
                if rhs.head in bindings and bindings[rhs.head] != lhs:
                    return False
                else:
                    bindings[rhs.head] = lhs
                    return True

            elif type(lhs.head) == Operation and type(rhs.head) == Operation:
                if lhs.head == rhs.head:
                    equivalent = True
                    for i in range(len(lhs.args)):
                        equivalent = equivalent and compare(lhs.args[i],
                                                            rhs.args[i])
                    return equivalent
                else:
                    return False

            else:
                return False

        return (compare(self, other), bindings)

    def apply_binding(self, binding):
        """
        Apply a set of variable bindings on the variables of a term.

        Args:
            binding: The set of variable bindings to apply on the term.

        Returns:
            A new term where the variables are replaced by their bindings.
        """
        assert type(binding) == dict, "Binding must be a dict"
        for key, value in binding.items():
            assert isinstance(key, Variable),\
                "Keys in binding must be variables"
            assert isinstance(value, Term),\
                "Variable bindings must be terms"

        def rename(t):
            if type(t.head) == Variable:
                return binding[t.head] or t
            else:
                args = []
                for arg in t.args:
                    args.append(rename(arg))
                return Term(t.head, tuple(args))

        return rename(self)

    def reduce(self, rewrite_rules):
        """
        Reduce the term by applying a set of rewrite rules on it until a
        fixpoint is reached. The resulting term is in normal form
        (accordingly to the rewrite rules passed as argument).

        Args:
            rewrite_rules: A list of rewrite rules to be applied on the term
                in order to reduce it to its normal form.

        Returns:
            A new term obtained after applying the rewrite rules on the term
            until a fixpoint (normal form) was reached.
        """
        prev_term = None
        new_term = Term(self.head, self.args)
        while new_term != prev_term:
            prev_term = new_term
            for rule in rewrite_rules:
                new_term = rule.apply(new_term, rewrite_rules)

        return new_term


class RewriteRule(object):
    """
    Rewrite rule for terms in ADTs.
    """

    def __init__(self, lhs, rhs, conditions=[]):
        assert isinstance(lhs, Term), "Left hand side must be a term"
        assert isinstance(rhs, Term), "Right hand side must be a term"
        assert type(conditions) == list,\
            "Conditions must be a list of conditions"
        for condition in conditions:
            assert len(condition) == 2, "Conditions must contain 2 terms"
            assert isinstance(condition[0], Term),\
                "Conditions must contain terms"
            assert isinstance(condition[1], Term),\
                "Conditions must contain terms"
        self.lhs = lhs
        self.rhs = rhs
        self.conditions = conditions

    def __str__(self):
        txt = ""
        if self.conditions:
            for condition in self.conditions: 
                txt += "({} == {}), ".format(str(condition[0]),
                                             str(condition[1]))
            txt += "=> "
        txt += "{} -> {}".format(str(self.lhs), str(self.rhs))
        return txt

    def __repr__(self):
        return str(self)

    def apply(self, term, rewrite_rules=[]):
        """
        Apply the rewrite rule on a term if it is possible.

        Args:
            term: The term to apply the rule on.
            rewrite_rules: A list of rewrite rules to use to reduce the
                conditions of the rule.

        Returns:
            A new term with where the rewrite rule has been applied.
        """
        # Recursive application of the rule on the arguments of the term
        # -> left-right innermost strategy.
        args = []
        for arg in term.args:
            args.append(self.apply(arg))

        new_term = Term(term.head, tuple(args))

        matching, binding = new_term.match(self.lhs)
        if matching:
            if self.conditions:
                for condition in self.conditions:
                    if condition[0].apply_binding(binding)\
                                   .reduce(rewrite_rules) !=\
                       condition[1].apply_binding(binding)\
                                   .reduce(rewrite_rules):
                        return new_term
            return Term(self.rhs.head, self.rhs.args).apply_binding(binding)
        else:
            return new_term
