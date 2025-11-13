# Symbolic Differentiation Calculator
# This project implements a symbolic differentiation system that can compute derivatives
# of mathematical expressions including polynomials, trigonometric functions, exponentials,
# and logarithms. It uses a recursive descent parser to parse expressions and builds an
# abstract syntax tree (AST) to represent them. The system supports all standard derivative
# rules: constant, power, sum/difference, product, quotient, chain rule, and derivatives
# of trigonometric, exponential, and logarithmic functions.
# 
# This implementation only uses Python's built-in math library for numerical evaluation
# of functions. All symbolic manipulation is done through custom node classes without
# external symbolic math libraries.
# This was a pain to make. 
# I was planning to also include more topics from calculus like definite and indefinite,
# But im too burn out on this project to go any further. mabey in the future this will chnage.

class Node:
    def diff(self, var):
        raise NotImplementedError

    def to_str(self):
        raise NotImplementedError
    
    def simplify(self):
        raise NotImplementedError


class NumberNode(Node):
    def __init__(self, value):
        self.value = value

    def diff(self, var):
        # d/dx(c) = 0
        return NumberNode(0)

    def to_str(self):
        # print integers nicely
        if isinstance(self.value, float) and self.value.is_integer():
            return str(int(self.value))
        return str(self.value)
    
    def simplify(self):
        return self


class VarNode(Node):
    def __init__(self, name):
        self.name = name

    def diff(self, var):
        # d/dx(x) = 1, d/dx(y) = 0 if y != x
        return NumberNode(1 if self.name == var else 0)

    def to_str(self):
        return self.name
    
    def simplify(self):
        return self


class UnaryOpNode(Node):
    def __init__(self, op, operand):
        self.op = op      # currently only '-'
        self.operand = operand

    def diff(self, var):
        if self.op == '-':
            # d/dx(-u) = -u'
            return UnaryOpNode('-', self.operand.diff(var))
        raise NotImplementedError

    def to_str(self):
        if self.op == '-':
            operand_str = self.operand.to_str()
            # Remove unnecessary parentheses for simple operands
            if isinstance(self.operand, (NumberNode, VarNode)):
                return f"-{operand_str}"
            return f"-({operand_str})"
    
    def simplify(self):
        simplified = UnaryOpNode(self.op, self.operand.simplify())
        # -(-x) = x
        if self.op == '-' and isinstance(simplified.operand, UnaryOpNode) and simplified.operand.op == '-':
            return simplified.operand.operand.simplify()
        # -0 = 0
        if self.op == '-' and isinstance(simplified.operand, NumberNode) and simplified.operand.value == 0:
            return NumberNode(0)
        return simplified


class FuncNode(Node):
    # Represents function calls: sin(x), cos(x), exp(x), ln(x), etc.
    def __init__(self, func_name, arg):
        self.func_name = func_name  # 'sin', 'cos', 'tan', 'sec', 'cot', 'csc', 'exp', 'ln', 'log'
        self.arg = arg  # Node representing the argument
    
    def diff(self, var):
        # Chain rule: d/dx(f(g(x))) = f'(g(x)) * g'(x)
        arg_diff = self.arg.diff(var)
        
        # Trigonometric derivatives
        if self.func_name == 'sin':
            # d/dx(sin(u)) = cos(u) * u'
            return BinOpNode(FuncNode('cos', self.arg), '*', arg_diff)
        
        if self.func_name == 'cos':
            # d/dx(cos(u)) = -sin(u) * u'
            return BinOpNode(UnaryOpNode('-', FuncNode('sin', self.arg)), '*', arg_diff)
        
        if self.func_name == 'tan':
            # d/dx(tan(u)) = sec^2(u) * u'
            sec_squared = BinOpNode(FuncNode('sec', self.arg), '^', NumberNode(2))
            return BinOpNode(sec_squared, '*', arg_diff)
        
        if self.func_name == 'sec':
            # d/dx(sec(u)) = sec(u) * tan(u) * u'
            sec_tan = BinOpNode(FuncNode('sec', self.arg), '*', FuncNode('tan', self.arg))
            return BinOpNode(sec_tan, '*', arg_diff)
        
        if self.func_name == 'cot':
            # d/dx(cot(u)) = -csc^2(u) * u'
            csc_squared = BinOpNode(FuncNode('csc', self.arg), '^', NumberNode(2))
            return BinOpNode(UnaryOpNode('-', csc_squared), '*', arg_diff)
        
        if self.func_name == 'csc':
            # d/dx(csc(u)) = -csc(u) * cot(u) * u'
            csc_cot = BinOpNode(FuncNode('csc', self.arg), '*', FuncNode('cot', self.arg))
            return BinOpNode(UnaryOpNode('-', csc_cot), '*', arg_diff)
        
        # Exponential derivatives
        if self.func_name == 'exp':
            # d/dx(e^u) = e^u * u'
            return BinOpNode(FuncNode('exp', self.arg), '*', arg_diff)
        
        # Logarithmic derivatives
        if self.func_name == 'ln':
            # d/dx(ln(u)) = (1/u) * u' = u' / u
            return BinOpNode(arg_diff, '/', self.arg)
        
        if self.func_name == 'log':
            # d/dx(log_a(u)) = u' / (ln(a) * u)
            # For now, assume base e (natural log) - could extend to support base parameter
            # This is actually ln, so same as ln
            return BinOpNode(arg_diff, '/', self.arg)
        
        raise NotImplementedError(f"Derivative not implemented for function: {self.func_name}")
    
    def to_str(self):
        arg_str = self.arg.to_str()
        # Add parentheses around argument if it's a compound expression
        if isinstance(self.arg, (NumberNode, VarNode)):
            return f"{self.func_name}({arg_str})"
        else:
            return f"{self.func_name}({arg_str})"
    
    def simplify(self):
        simplified_arg = self.arg.simplify()
        return FuncNode(self.func_name, simplified_arg)


class BinOpNode(Node):
    def __init__(self, left, op, right):
        self.left = left   # Node
        self.op = op       # '+', '-', '*', '/', '^'
        self.right = right # Node

    def diff(self, var):
        # (u + v)' = u' + v'
        if self.op == '+':
            return BinOpNode(self.left.diff(var), '+', self.right.diff(var))

        # (u - v)' = u' - v'
        if self.op == '-':
            return BinOpNode(self.left.diff(var), '-', self.right.diff(var))

        # (u * v)' = u'v + uv'
        if self.op == '*':
            return BinOpNode(
                BinOpNode(self.left.diff(var), '*', self.right),
                '+',
                BinOpNode(self.left, '*', self.right.diff(var))
            )

        # (u / v)' = (u'v - uv') / v^2
        if self.op == '/':
            u, v = self.left, self.right
            du, dv = u.diff(var), v.diff(var)
            numerator = BinOpNode(
                BinOpNode(du, '*', v),
                '-',
                BinOpNode(u, '*', dv)
            )
            denom = BinOpNode(v, '^', NumberNode(2))
            return BinOpNode(numerator, '/', denom)

        # Power rule and exponential derivatives
        if self.op == '^':
            # Case 1: (x^n)' = n * x^(n-1), n constant (power rule)
            if isinstance(self.left, VarNode) and isinstance(self.right, NumberNode):
                n = self.right.value
                return BinOpNode(
                    NumberNode(n),
                    '*',
                    BinOpNode(self.left, '^', NumberNode(n - 1))
                )
            
            # Case 2: (e^u)' = e^u * u' (exponential with base e)
            # Note: e^x should typically use exp(x), but we support e**x syntax
            # Check if base is approximately e (Euler's number)
            if isinstance(self.left, NumberNode):
                import math
                if abs(self.left.value - math.e) < 1e-10:
                    # d/dx(e^u) = e^u * u'
                    return BinOpNode(
                        BinOpNode(self.left, '^', self.right),
                        '*',
                        self.right.diff(var)
                    )
            
            # Case 3: (a^u)' = ln(a) * a^u * u', a constant (general exponential)
            if isinstance(self.left, NumberNode) and isinstance(self.right, Node):
                a = self.left.value
                if a > 0 and a != 1:  # Valid base
                    # d/dx(a^u) = ln(a) * a^u * u'
                    ln_a = FuncNode('ln', NumberNode(a))
                    a_power_u = BinOpNode(self.left, '^', self.right)
                    return BinOpNode(
                        BinOpNode(ln_a, '*', a_power_u),
                        '*',
                        self.right.diff(var)
                    )
            
            # Case 4: (u^v)' - general case using logarithmic differentiation
            # For now, raise error for non-constant exponents that aren't handled above
            if not isinstance(self.right, NumberNode):
                raise NotImplementedError(f"Derivative of {self.left.to_str()}^{self.right.to_str()} not fully implemented")
            
            raise NotImplementedError(f"Power rule case not handled: {self.left.to_str()}^{self.right.to_str()}")

        raise NotImplementedError(f"Unknown op {self.op}")

    def to_str(self):
        # convert '^' to Python '**'
        op = '**' if self.op == '^' else self.op
        left_str = self.left.to_str()
        right_str = self.right.to_str()
        
        # Remove unnecessary parentheses for simple operands
        if isinstance(self.left, (NumberNode, VarNode, FuncNode)):
            left_paren = False
        elif isinstance(self.left, BinOpNode) and self._needs_paren(self.left, self.op, True):
            left_paren = True
        else:
            left_paren = False
        
        if isinstance(self.right, (NumberNode, VarNode, FuncNode)):
            right_paren = False
        elif isinstance(self.right, BinOpNode) and self._needs_paren(self.right, self.op, False):
            right_paren = True
        else:
            right_paren = False
        
        left_fmt = f"({left_str})" if left_paren else left_str
        right_fmt = f"({right_str})" if right_paren else right_str
        
        # Add spaces only for addition and subtraction
        if self.op in ('+', '-'):
            return f"{left_fmt} {op} {right_fmt}"
        else:
            # No spaces for multiplication, division, and exponentiation
            return f"{left_fmt}{op}{right_fmt}"
    
    def _needs_paren(self, child, parent_op, is_left):
        # Determine if child needs parentheses based on operator precedence
        if not isinstance(child, BinOpNode):
            return False
        
        # Operator precedence: +,- = 1, *,/ = 2, ^ = 3
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
        child_prec = precedence.get(child.op, 0)
        parent_prec = precedence.get(parent_op, 0)
        
        # Child needs parens if it has lower precedence
        if child_prec < parent_prec:
            return True
        # For equal precedence, check associativity
        if child_prec == parent_prec:
            # For left-associative ops, right child needs parens
            # For right-associative ops (^), left child needs parens
            if parent_op == '^':
                return is_left
            else:
                return not is_left
        return False
    
    def simplify(self):
        left = self.left.simplify()
        right = self.right.simplify()
        
        # Handle zeros
        if self.op == '*':
            # 0 * anything = 0, anything * 0 = 0
            if isinstance(left, NumberNode) and left.value == 0:
                return NumberNode(0)
            if isinstance(right, NumberNode) and right.value == 0:
                return NumberNode(0)
            # 1 * x = x, x * 1 = x
            if isinstance(left, NumberNode) and left.value == 1:
                return right
            if isinstance(right, NumberNode) and right.value == 1:
                return left
        
        if self.op == '+':
            # 0 + x = x, x + 0 = x
            if isinstance(left, NumberNode) and left.value == 0:
                return right
            if isinstance(right, NumberNode) and right.value == 0:
                return left
            # Combine constant numbers
            if isinstance(left, NumberNode) and isinstance(right, NumberNode):
                return NumberNode(left.value + right.value)
            # Collect and combine constants in addition chains
            # Only do this if left is already an addition (to avoid infinite recursion)
            if isinstance(left, BinOpNode) and left.op == '+':
                terms = self._collect_add_terms(left, right)
                constants = [t for t in terms if isinstance(t, NumberNode)]
                non_constants = [t for t in terms if not isinstance(t, NumberNode)]
                const_sum = sum(c.value for c in constants)
                if const_sum != 0:
                    non_constants.append(NumberNode(const_sum))
                if len(non_constants) == 0:
                    return NumberNode(0)
                if len(non_constants) == 1:
                    return non_constants[0]
                # Rebuild addition chain (don't simplify again to avoid recursion)
                result = non_constants[0]
                for term in non_constants[1:]:
                    result = BinOpNode(result, '+', term)
                return result
        
        if self.op == '-':
            # x - 0 = x
            if isinstance(right, NumberNode) and right.value == 0:
                return left
            # 0 - x = -x
            if isinstance(left, NumberNode) and left.value == 0:
                return UnaryOpNode('-', right).simplify()
            # Combine constant numbers
            if isinstance(left, NumberNode) and isinstance(right, NumberNode):
                return NumberNode(left.value - right.value)
        
        if self.op == '/':
            # 0 / x = 0 (x != 0)
            if isinstance(left, NumberNode) and left.value == 0:
                return NumberNode(0)
            # x / 1 = x
            if isinstance(right, NumberNode) and right.value == 1:
                return left
        
        if self.op == '^':
            # x^0 = 1
            if isinstance(right, NumberNode) and right.value == 0:
                return NumberNode(1)
            # x^1 = x
            if isinstance(right, NumberNode) and right.value == 1:
                return left
            # 1^x = 1
            if isinstance(left, NumberNode) and left.value == 1:
                return NumberNode(1)
            # 0^x = 0 (x > 0)
            if isinstance(left, NumberNode) and left.value == 0:
                return NumberNode(0)
        
        return BinOpNode(left, self.op, right)
    
    def _collect_add_terms(self, left, right):
        # Collect all terms in an addition/subtraction chain
        # Recursively extracts all operands from nested addition operations
        terms = []
        # Collect from left side - if it's an addition, recurse; otherwise add it
        if isinstance(left, BinOpNode) and left.op == '+':
            terms.extend(self._collect_add_terms(left.left, left.right))
        else:
            terms.append(left)
        # Add right side term
        terms.append(right)
        return terms


class Parser:
    # Recursive descent parser for mathematical expressions
    # Parses expressions following operator precedence: +,- < *,/ < ^
    
    def __init__(self, text):
        # Initialize parser with input text and position index
        self.text = text
        self.i = 0  # Current position in text
    
    def skip_ws(self):
        # Skip whitespace characters at current position
        t = self.text
        while self.i < len(t) and t[self.i].isspace():
            self.i += 1

    def peek(self):
        # Look at next character without consuming it, skipping whitespace
        # Returns None if at end of input
        self.skip_ws()
        if self.i >= len(self.text):
            return None
        return self.text[self.i]

    def consume(self, ch=None):
        # Consume and return next character, skipping whitespace
        # If ch is provided, raises error if character doesn't match
        # Returns None if at end of input
        self.skip_ws()
        if self.i >= len(self.text):
            return None
        c = self.text[self.i]
        if ch is not None and c != ch:
            raise ValueError(f"Expected '{ch}' but got '{c}'")
        self.i += 1
        return c
    
    def parse_number(self):
        # Parse a numeric literal (integer or float)
        # Handles decimal point and ensures valid number format
        self.skip_ws()
        t = self.text
        start = self.i
        dot_seen = False  # Track if we've seen a decimal point
        # Consume digits and at most one decimal point
        while self.i < len(t) and (t[self.i].isdigit() or (t[self.i] == '.' and not dot_seen)):
            if t[self.i] == '.':
                dot_seen = True
            self.i += 1
        if start == self.i:
            raise ValueError("Number Expected")
        return NumberNode(float(t[start:self.i]))

    def parse_name(self):
        # Parse a variable name (identifier)
        # Must start with letter or underscore, followed by alphanumeric or underscore
        self.skip_ws()
        t = self.text
        start = self.i
        # First character must be letter or underscore
        if self.i < len(t) and (t[self.i].isalpha() or t[self.i] == '_'):
            self.i += 1
            # Subsequent characters can be alphanumeric or underscore
            while self.i < len(t) and (t[self.i].isalnum() or t[self.i] == '_'):
                self.i += 1
        else:
            raise ValueError("Name expected")
        return VarNode(t[start:self.i])

    def parse_atom(self):
        # Parse an atomic expression: number, variable, function call, parenthesized expression, or unary minus
        # Atoms are the base case for recursive parsing
        self.skip_ws()
        c = self.peek()
        if c is None:
            raise ValueError("Unexpected end of input")

        # Parse number if starts with digit or decimal point
        if c.isdigit() or c == '.':
            return self.parse_number()

        # Parse variable name or function call if starts with letter or underscore
        if c.isalpha() or c == '_':
            # Check if it's a function call (followed by '(')
            start_pos = self.i
            name = self.parse_name()
            self.skip_ws()
            # If next character is '(', it's a function call
            if self.i < len(self.text) and self.text[self.i] == '(':
                # It's a function call, not just a variable
                # Reset position and parse as function
                self.i = start_pos
                return self.parse_function_call()
            # Otherwise it's just a variable
            return name

        # Parse parenthesized expression: (expr)
        if c == '(':
            self.consume('(')
            node = self.parse_expr()
            self.consume(')')
            return node

        # Parse unary minus: -atom
        if c == '-':
            self.consume('-')
            node = self.parse_atom()
            return UnaryOpNode('-', node)

        raise ValueError(f"Unexpected character: {c}")
    
    def parse_function_call(self):
        # Parse a function call: func_name(expr)
        # Supported functions: sin, cos, tan, sec, cot, csc, exp, ln, log
        func_name = self.parse_name().name
        self.consume('(')
        arg = self.parse_expr()
        self.consume(')')
        return FuncNode(func_name, arg)

    def parse_power(self):
        # Parse exponentiation operations (right-associative)
        # Handles Python's ** operator, converts to internal ^ representation
        node = self.parse_atom()
        while True:
            self.skip_ws()
            # Look for '**' (Python exponentiation operator)
            if self.text[self.i:self.i + 2] == '**':
                self.i += 2
                right = self.parse_atom()
                node = BinOpNode(node, '^', right)
            else:
                break
        return node

    def parse_term(self):
        # Parse multiplication and division operations (left-associative)
        # Terms are built from power expressions
        node = self.parse_power()
        while True:
            c = self.peek()
            if c in ('*', '/'):
                op = self.consume()
                right = self.parse_power()
                node = BinOpNode(node, op, right)
            else:
                break
        return node

    def parse_expr(self):
        # Parse addition and subtraction operations (left-associative)
        # Expressions are built from terms
        # This is the top-level expression parser
        node = self.parse_term()
        while True:
            c = self.peek()
            if c in ('+', '-'):
                op = self.consume()
                right = self.parse_term()
                node = BinOpNode(node, op, right)
            else:
                break
        return node

    def parse(self):
        # Main entry point: parse entire expression and verify no trailing characters
        node = self.parse_expr()
        self.skip_ws()
        if self.i != len(self.text):
            raise ValueError("Unexpected trailing characters")
        return node
    
    

def symbolic_diff_expr(expr: str, var: str) -> str:
    # Takes an expression string in python syntax and return a new string representing its derivatve with respect to 'var'
    tree = Parser(expr).parse()
    d = tree.diff(var)
    simplified = d.simplify()
    return simplified.to_str()


class MathFunc:
    def __init__(self, expr: str, var:str):
        self.expr = expr    # string to eval, eg: "x**3 + 2*x + 1"
        self.var = var      # variable name, eg: "x"
    
    def __call__(self, value):
        # Evaluates the expression with the variable bound to the value
        import math
        # Provide math functions for evaluation
        env = {
            self.var: value,
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'sec': lambda x: 1 / math.cos(x),
            'cot': lambda x: 1 / math.tan(x),
            'csc': lambda x: 1 / math.sin(x),
            'exp': math.exp,
            'ln': math.log,
            'log': math.log,
            'e': math.e,
            'pi': math.pi
        }
        return eval(self.expr, {"__builtins__": {}}, env)

    def __str__(self):
        return self.expr


def func(expr: str, var: str) -> MathFunc:
    # creates a symbolic function of one variable
    # ex: y = func("x + 1","x")
    return MathFunc(expr, var)


def diff(f: MathFunc, var: str) -> MathFunc:
    # Differentiate f with resprect to 'var' and return another mathmatical function
    # ex: dydx = diff(y, "x")
    d_expr = symbolic_diff_expr(f.expr, var)
    return MathFunc(d_expr, var)
