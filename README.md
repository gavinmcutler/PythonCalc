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

Or use the library in your own code:

```bash
python derivative.py  # (if you add your own code at the bottom)
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

This project is open source and available for educational purposes.

## Author Notes

This project was built as a learning exercise in implementing symbolic mathematics. While integration features were initially planned, they are not currently implemented. Future updates may include additional calculus features.

