import unittest
from alpyne.adt import Sort, GenericSort, Operation, Variable, Term, RewriteRule


class TestSort(unittest.TestCase):

    def test_instanciation(self):
        with self.assertRaises(AssertionError):
            Sort(2)  # Name must be a string.
        sort = Sort('sort')
        self.assertEqual(type(sort), Sort)

    def test_str_representation(self):
        sort = Sort('sort')
        self.assertEqual(str(sort), 'sort')

    def test_operation_definition(self):
        sort = Sort('sort')
        with self.assertRaises(AssertionError):
            sort.operation(4, ())  # Name must be a string.
            sort.operation('op', sort)  # Signature must be a tuple.
            sort.operation('op', (3, 2))  # Elts of sign. must be sorts.
            # Sort of the operation must be a sort.
            sort.operation('op', (sort,), 3)
        sort.operation('op', (sort,), sort)
        self.assertEqual(type(sort.op), Operation)

    def test_variable_definition(self):
        sort = Sort('sort')
        with self.assertRaises(AssertionError):
            sort.variable(3)  # Name must be a string.
        sort.variable('x')
        self.assertEqual(type(sort.x), Variable)


class TestGenericSort(unittest.TestCase):

    def test_str_representation(self):
        self.assertEqual(str(GenericSort()), "anysort")

    def test_variable(self):
        generic = GenericSort()
        generic.variable('x')
        self.assertEqual(type(generic.x), Variable)
        self.assertEqual(type(generic.x()), Term)


class TestOperation(unittest.TestCase):

    def test_instanciation(self):
        sort = Sort('sort')
        with self.assertRaises(AssertionError):
            Operation(2, (), sort)  # Name must be a string.
            Operation('op', sort, sort)  # Signature must be a tuple.
            Operation('op', (3, 2), sort)  # Elts of tuple must be sorts.
            Operation('op', (sort,), 3)  # Sort must be a sort.
        op = Operation('op', (sort,), sort)
        self.assertEqual(type(op), Operation)
        self.assertEqual(op.name, 'op')
        self.assertEqual(op.signature, (sort,))
        self.assertEqual(op.sort, sort)

    def test_str_representation(self):
        sort = Sort('sort')
        op = Operation('op', (sort,), sort)
        self.assertEqual(str(op), 'sort.op(sort, ) -> sort')

    def test_call(self):
        sort = Sort('sort')
        op = Operation('op', (), sort)
        term = op()
        self.assertEqual(type(term), Term)


class TestVariable(unittest.TestCase):

    def test_instanciation(self):
        sort = Sort('sort')
        with self.assertRaises(AssertionError):
            Variable(3, sort)  # Name must be a string.
            Variable('x', 3)  # Sort must be a sort.
        var = Variable('x', sort)
        self.assertEqual(type(var), Variable)
        self.assertEqual(var.name, 'x')
        self.assertEqual(var.sort, sort)

    def test_str_representation(self):
        sort = Sort('sort')
        var = Variable('x', sort)
        self.assertEqual(str(var), 'sort.x')

    def test_call(self):
        sort = Sort('sort')
        var = Variable('x', sort)
        term = var()
        self.assertEqual(type(term), Term)


class TestTerm(unittest.TestCase):

    def test_instanciation(self):
        sort = Sort('sort')
        sort.operation('op', (sort,))
        sort.variable('x')
        with self.assertRaises(AssertionError):
            Term(3, ())  # Head must be an operation or a variable.
            Term(sort.op, sort.x)  # Args must be a tuple.
            Term(sort.op, ())  # Args must match signature of operation.
            Term(sort.op, (3,))  # Args must be a tuple of terms.
        term = Term(sort.op, (sort.x(),))
        self.assertEqual(type(term), Term)
        self.assertEqual(term.head, sort.op)
        self.assertEqual(term.args, (sort.x(),))

    def test_equality(self):
        sort = Sort('sort')
        sort.operation('op', (sort,))
        sort.variable('x')
        t1 = sort.op(sort.x())
        t2 = sort.op(sort.op(sort.x()))
        self.assertTrue(t1 == sort.op(sort.x()))
        self.assertFalse(t1 == t2)
        self.assertTrue(t1 != t2)

    def test_str_representation(self):
        sort = Sort('sort')
        sort.operation('op', (sort,))
        sort.variable('x')
        term = sort.op(sort.x())
        self.assertEqual(str(term), 'sort.op(sort.x)')

    def test_match(self):
        sort = Sort('sort')
        sort.operation('op', (sort,))
        sort.operation('op2', (sort, sort))
        sort.variable('x')
        sort.variable('y')
        t1 = sort.op(sort.x())
        t2 = sort.op(sort.op(sort.y()))
        t3 = sort.op2(sort.x(), sort.y())
        match1, binding1 = t1.match(t2)
        match2, _ = t1.match(t3)
        self.assertTrue(match1)
        self.assertEqual(binding1[sort.x], sort.op(sort.y()))
        self.assertFalse(match2)

    def test_apply_binding(self):
        sort = Sort('sort')
        sort.operation('op', (sort, sort))
        sort.operation('const', ())
        sort.variable('x')
        sort.variable('y')
        t1 = sort.op(sort.x(), sort.y())
        t2 = sort.op(sort.op(sort.const()), sort.const())
        _, binding = t1.match(t2)
        t3 = t1.apply_binding(binding)
        self.assertEqual(t3, t2)

    def test_generic_sort(self):
        sort = Sort('sort')
        sort.operation('op_generic', (GenericSort(),))
        sort2 = Sort('sort2')
        sort2.variable('x')
        t = sort.op_generic(sort2.x())
        self.assertEqual(type(t), Term)
        self.assertEqual(t.args[0].sort, sort2)

    def test_reduce(self):
        sort = Sort('sort')
        sort.operation('const', ())
        sort.operation('reduce', (sort,))
        sort.operation('merge', (sort, sort))
        sort.variable('x')
        sort.rewrite_rule(sort.reduce(sort.x()), sort.x())
        sort.rewrite_rule(sort.merge(sort.x(), sort.x()),
                          sort.reduce(sort.x()))
        t = sort.reduce(sort.merge(sort.reduce(sort.const()), sort.const()))
        t2 = t.reduce(sort.rewrite_rules)
        self.assertEqual(t2, sort.const())


class TestRewriteRule(unittest.TestCase):

    def test_instanciation(self):
        sort = Sort('sort')
        sort.operation('op', (sort, sort))
        sort.operation('op2', (sort,))
        sort.operation('eq', (sort, sort))
        sort.variable('x')
        sort.variable('y')
        rule = RewriteRule(sort.op(sort.x(), sort.y()),
                           sort.op2(sort.x()),
                           [(sort.eq(sort.x(), sort.y()),
                            sort.eq(sort.x(), sort.y()))])
        self.assertEqual(type(rule), RewriteRule)
        self.assertEqual(rule.lhs, sort.op(sort.x(), sort.y()))
        self.assertEqual(rule.rhs, sort.op2(sort.x()))
        self.assertEqual(rule.conditions, [(sort.eq(sort.x(), sort.y()),
                                            sort.eq(sort.x(), sort.y()))])

    def test_str_representation(self):
        sort = Sort('sort')
        sort.operation('op', (sort, sort))
        sort.operation('op2', (sort,))
        sort.operation('eq', (sort, sort))
        sort.variable('x')
        sort.variable('y')
        rule = RewriteRule(sort.op(sort.x(), sort.y()),
                           sort.op2(sort.x()),
                           [(sort.eq(sort.x(), sort.y()),
                            sort.eq(sort.x(), sort.y()))])
        self.assertEqual(str(rule), '(sort.eq(sort.x, sort.y) ==\
 sort.eq(sort.x, sort.y)), => sort.op(sort.x, sort.y) -> sort.op2(sort.x)')

    def test_apply(self):
        sort = Sort('sort')
        sort.operation('op', (sort, sort))
        sort.operation('op2', (sort,))
        sort.operation('eq', (sort, sort))
        sort.operation('const', ())
        sort.variable('x')
        sort.variable('y')
        rule = RewriteRule(sort.op(sort.x(), sort.y()),
                           sort.op2(sort.x()),
                           [(sort.eq(sort.x(), sort.y()),
                            sort.eq(sort.x(), sort.y()))])
        term = Term(sort.op, (sort.const(), sort.const()))
        term2 = rule.apply(term)
        self.assertEqual(term2, sort.op2(sort.const()))

    def test_generic_sort(self):
        generic = GenericSort()
        generic.variable('x')
        sort = Sort('sort')
        sort.operation('op_gen', (generic, generic))
        sort.operation('const', ())
        sort2 = Sort('sort2')
        sort2.operation('const', ())
        r = RewriteRule(sort.op_gen(generic.x(), generic.x()), generic.x())
        t1 = r.apply(sort.op_gen(sort2.const(), sort2.const()))
        self.assertEqual(t1, sort2.const())
        t2 = r.apply(sort.op_gen(sort2.const(), sort.const()))
        self.assertEqual(t2, sort.op_gen(sort2.const(), sort.const()))


if __name__ == "__main__":
    unittest.main()
