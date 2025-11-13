# Symbolic Differentiation Calculator

A Python implementation of a symbolic differentiation system that computes derivatives of mathematical expressions. This project uses a recursive descent parser to build an abstract syntax tree (AST) and implements all standard calculus derivative rules.

## Features

- **Symbolic Differentiation**: Computes exact symbolic derivatives (not numerical approximations)
- **Comprehensive Rule Support**: Implements all standard derivative rules from calculus
- **Function Support**: Handles polynomials, trigonometric functions, exponentials, and logarithms
- **Expression Simplification**: Automatically simplifies derivative expressions by removing zeros and unnecessary parentheses
- **Clean Output**: Formatted derivative expressions with proper spacing
- **No External Dependencies**: Only uses Python's built-in `math` library

## Supported Derivative Rules

1. **Constant Rule**: `f(x) = c → f'(x) = 0`
2. **Constant Multiple Rule**: `g(x) = c·f(x) → g'(x) = c·f'(x)`
3. **Power Rule**: `f(x) = x^n → f'(x) = n·x^(n-1)`
4. **Sum and Difference Rule**: `h(x) = f(x) ± g(x) → h'(x) = f'(x) ± g'(x)`
5. **Product Rule**: `h(x) = f(x)·g(x) → h'(x) = f'(x)·g(x) + f(x)·g'(x)`
6. **Quotient Rule**: `h(x) = f(x)/g(x) → h'(x) = (f'(x)·g(x) - f(x)·g'(x)) / g(x)^2`
7. **Chain Rule**: `h(x) = f(g(x)) → h'(x) = f'(g(x))·g'(x)`
8. **Trigonometric Functions**: sin, cos, tan, sec, cot, csc
9. **Exponential Functions**: `e^x`, `e^(g(x))`, `a^x`, `a^(g(x))`
10. **Logarithmic Functions**: `ln(x)`, `ln(g(x))`

## Installation

No installation required! Just ensure you have Python 3.x installed.

```bash
# Clone the repository
git clone https://github.com/gavinmcutler/PythonCalc.git
cd PythonCalc
```

## Quick Start

Run the examples to see all derivative rules in action:

```bash
python examples.py
```

Or import and use the library in your own Python scripts:

```python
from derivative import func, diff

# Your code here
y = func("x**2 + 1", "x")
dydx = diff(y, "x")
print(dydx)
```

## Usage

### Basic Example

```python
from derivative import func, diff

# Define a function
y = func("x**2 + 2*x + 4", "x")

# Compute its derivative
dydx = diff(y, "x")

# Print results
print(f"y(x) = {y}")
print(f"y'(x) = {dydx}")
print(f"y'(5) = {dydx(5)}")
```

### Supported Functions

The parser supports the following mathematical functions:

- **Trigonometric**: `sin(x)`, `cos(x)`, `tan(x)`, `sec(x)`, `cot(x)`, `csc(x)`
- **Exponential**: `exp(x)` (for e^x), `2**x` (for 2^x), `3**(x**2)` (for 3^(x²))
- **Logarithmic**: `ln(x)`, `log(x)`

### Example Expressions

```python
# Polynomial
f1 = func("x**3 + 2*x**2 - 5*x + 1", "x")

# Trigonometric
f2 = func("sin(x**2)", "x")
f3 = func("cos(x) * tan(x)", "x")

# Exponential
f4 = func("exp(x)", "x")
f5 = func("2**x", "x")

# Logarithmic
f6 = func("ln(x**2 + 1)", "x")

# Combined
f7 = func("x**2 * exp(x) + sin(x) * cos(x)", "x")
```

## Example Output

```
============================================================
DERIVATIVE RULE TESTS
============================================================

1. CONSTANT RULE: f(x) = c, f'(x) = 0
  f(x) = 5
  f'(x) = 0
  f'(3) = 0

2. CONSTANT MULTIPLE RULE: g(x) = c*f(x), g'(x) = c*f'(x)
  f(x) = 3*x**2
  f'(x) = 3*(2*x)
  f'(2) = 12

3. POWER RULE: f(x) = x^n, f'(x) = n*x^(n-1)
  f(x) = x**5
  f'(x) = 5*x**4
  f'(2) = 80

...

8. TRIGONOMETRIC DERIVATIVES
  8a. sin(x): f'(x) = cos(x)
     f(x) = sin(x), f'(x) = cos(x), f'(1) = 0.5403023058681398
  8b. cos(x): f'(x) = -sin(x)
     f(x) = cos(x), f'(x) = -(sin(x)), f'(1) = -0.8414709848078965
  ...
```

## Project Structure

- **Node Classes**: Abstract base class and implementations for different expression types
  - `NumberNode`: Represents numeric constants
  - `VarNode`: Represents variables
  - `UnaryOpNode`: Represents unary operations (e.g., negation)
  - `BinOpNode`: Represents binary operations (+, -, *, /, ^)
  - `FuncNode`: Represents function calls (sin, cos, exp, ln, etc.)

- **Parser**: Recursive descent parser that converts string expressions to AST
- **Differentiation**: Each node type implements its own `diff()` method
- **Simplification**: Automatic simplification of derivative expressions

## How the Parser Works

The parser uses a **recursive descent parser** to convert mathematical expressions from strings into an Abstract Syntax Tree (AST). This section explains each step of the parsing process.

### Overview

The parser follows operator precedence rules:
- **Highest precedence**: Exponentiation (`^` or `**`) - right-associative
- **Medium precedence**: Multiplication (`*`) and Division (`/`) - left-associative
- **Lowest precedence**: Addition (`+`) and Subtraction (`-`) - left-associative

### Parsing Steps

The parser processes expressions in a hierarchical manner, starting from the lowest precedence operations and working down to atoms:

#### 1. **Entry Point: `parse()`**
   - Main entry point that initiates parsing
   - Calls `parse_expr()` to parse the entire expression
   - Verifies no trailing characters remain after parsing

#### 2. **Top Level: `parse_expr()`**
   - Parses addition and subtraction operations (lowest precedence)
   - Starts by parsing a term, then looks for `+` or `-` operators
   - Builds left-associative chains: `a + b - c` → `((a + b) - c)`
   - Example: `"x + 2*y - 3"` → `BinOpNode(BinOpNode(x, '+', 2*y), '-', 3)`

#### 3. **Terms: `parse_term()`**
   - Parses multiplication and division operations (medium precedence)
   - Starts by parsing a power expression, then looks for `*` or `/` operators
   - Builds left-associative chains: `a * b / c` → `((a * b) / c)`
   - Example: `"x * y / 2"` → `BinOpNode(BinOpNode(x, '*', y), '/', 2)`

#### 4. **Powers: `parse_power()`**
   - Parses exponentiation operations (highest precedence)
   - Starts by parsing an atom, then looks for `**` operators
   - Builds right-associative chains: `a ** b ** c` → `(a ** (b ** c))`
   - Converts Python's `**` to internal `^` representation
   - Example: `"x ** 2"` → `BinOpNode(x, '^', 2)`

#### 5. **Atoms: `parse_atom()`**
   - Parses the most basic expressions (base case for recursion)
   - Handles five types of atoms:
     - **Numbers**: `"42"`, `"3.14"` → `NumberNode`
     - **Variables**: `"x"`, `"y"` → `VarNode`
     - **Function calls**: `"sin(x)"` → `FuncNode` (detected by checking for `(` after name)
     - **Parenthesized expressions**: `"(x + 1)"` → recursively calls `parse_expr()`
     - **Unary minus**: `"-x"` → `UnaryOpNode('-', x)`

#### 6. **Helper Methods**

   - **`parse_number()`**: 
     - Consumes digits and at most one decimal point
     - Returns a `NumberNode` with the parsed float value
     - Example: `"3.14"` → `NumberNode(3.14)`

   - **`parse_name()`**:
     - Parses identifiers (variable names or function names)
     - Must start with letter or underscore, followed by alphanumeric/underscore
     - Example: `"x"`, `"sin"`, `"my_var"` → `VarNode` or used in `FuncNode`

   - **`parse_function_call()`**:
     - Parses function calls like `sin(x)`, `exp(x**2)`
     - Reads function name, consumes `(`, parses argument expression, consumes `)`
     - Returns `FuncNode(func_name, argument_node)`

   - **`skip_ws()`**: Skips whitespace characters at the current position
   - **`peek()`**: Looks at the next character without consuming it (returns `None` if at end of input)
   - **`consume(ch)`**: Consumes and returns the next character; if `ch` is provided, validates that the character matches it

### Example: Parsing `"x**2 + 2*x + 1"`

Here's how the parser processes this expression step by step:

1. **`parse_expr()`** is called
   - Parses first term: `"x**2"`
   - Finds `+` operator
   - Parses second term: `"2*x"`
   - Finds `+` operator
   - Parses third term: `"1"`
   - Builds: `BinOpNode(BinOpNode(x**2, '+', 2*x), '+', 1)`

2. **First term `"x**2"`** (via `parse_term()` → `parse_power()`):
   - Parses atom: `"x"` → `VarNode("x")`
   - Finds `**` operator
   - Parses right atom: `"2"` → `NumberNode(2)`
   - Returns: `BinOpNode(VarNode("x"), '^', NumberNode(2))`

3. **Second term `"2*x"`** (via `parse_term()`):
   - Parses power: `"2"` → `NumberNode(2)`
   - Finds `*` operator
   - Parses power: `"x"` → `VarNode("x")`
   - Returns: `BinOpNode(NumberNode(2), '*', VarNode("x"))`

4. **Third term `"1"`**:
   - Parses atom: `"1"` → `NumberNode(1)`

### Resulting AST Structure

```
BinOpNode(
  BinOpNode(
    BinOpNode(VarNode("x"), '^', NumberNode(2)),  // x**2
    '+',
    BinOpNode(NumberNode(2), '*', VarNode("x"))  // 2*x
  ),
  '+',
  NumberNode(1)  // 1
)
```

This AST structure allows the differentiation system to apply rules recursively, with each node type knowing how to differentiate itself.

## Implementation Details

- Uses a recursive descent parser following operator precedence
- Builds an abstract syntax tree (AST) to represent expressions
- Implements the chain rule for composite functions
- Automatically simplifies expressions by:
  - Removing terms multiplied by zero
  - Combining constant terms
  - Removing unnecessary parentheses
  - Formatting output with appropriate spacing

## Limitations

- Currently only supports single-variable differentiation
- Some complex cases of the power rule (like `u^v` where both are non-constant) are not fully implemented
- No support for integration (definite or indefinite) - may be added in the future

## Requirements

- Python 3.x
- `math` library (built-in)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author Notes

This project was built as a learning exercise in implementing symbolic mathematics. While integration features were initially planned, they are not currently implemented. Future updates may include additional calculus features such as definite and indefinite integration.

