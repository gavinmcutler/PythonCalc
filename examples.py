# Comprehensive test cases for all derivative rules
# This file demonstrates all the derivative rules implemented in the system

from derivative import func, diff

print("=" * 60)
print("DERIVATIVE RULE TESTS")
print("=" * 60)

# 1. Constant Rule: f(x) = c, f'(x) = 0
print("\n1. CONSTANT RULE: f(x) = c, f'(x) = 0")
f1 = func("5", "x")
df1 = diff(f1, "x")
print(f"  f(x) = {f1}")
print(f"  f'(x) = {df1}")
print(f"  f'(3) = {df1(3)}")

# 2. Constant Multiple Rule: g(x) = c*f(x), g'(x) = c*f'(x)
print("\n2. CONSTANT MULTIPLE RULE: g(x) = c*f(x), g'(x) = c*f'(x)")
f2 = func("3*x**2", "x")
df2 = diff(f2, "x")
print(f"  f(x) = {f2}")
print(f"  f'(x) = {df2}")
print(f"  f'(2) = {df2(2)}")

# 3. Power Rule: f(x) = x^n, f'(x) = n*x^(n-1)
print("\n3. POWER RULE: f(x) = x^n, f'(x) = n*x^(n-1)")
f3 = func("x**5", "x")
df3 = diff(f3, "x")
print(f"  f(x) = {f3}")
print(f"  f'(x) = {df3}")
print(f"  f'(2) = {df3(2)}")

# 4. Sum and Difference Rule: h(x) = f(x) ± g(x), h'(x) = f'(x) ± g'(x)
print("\n4. SUM AND DIFFERENCE RULE: h(x) = f(x) ± g(x), h'(x) = f'(x) ± g'(x)")
f4 = func("x**3 + 2*x**2 - 5*x + 1", "x")
df4 = diff(f4, "x")
print(f"  f(x) = {f4}")
print(f"  f'(x) = {df4}")
print(f"  f'(2) = {df4(2)}")

# 5. Product Rule: h(x) = f(x)*g(x), h'(x) = f'(x)*g(x) + f(x)*g'(x)
print("\n5. PRODUCT RULE: h(x) = f(x)*g(x), h'(x) = f'(x)*g(x) + f(x)*g'(x)")
f5 = func("x**2 * sin(x)", "x")
df5 = diff(f5, "x")
print(f"  f(x) = {f5}")
print(f"  f'(x) = {df5}")
print(f"  f'(1) = {df5(1)}")

# 6. Quotient Rule: h(x) = f(x)/g(x), h'(x) = (f'(x)*g(x) - f(x)*g'(x)) / g(x)^2
print("\n6. QUOTIENT RULE: h(x) = f(x)/g(x), h'(x) = (f'(x)*g(x) - f(x)*g'(x)) / g(x)^2")
f6 = func("x**2 / (x + 1)", "x")
df6 = diff(f6, "x")
print(f"  f(x) = {f6}")
print(f"  f'(x) = {df6}")
print(f"  f'(2) = {df6(2)}")

# 7. Chain Rule: h(x) = f(g(x)), h'(x) = f'(g(x))*g'(x)
print("\n7. CHAIN RULE: h(x) = f(g(x)), h'(x) = f'(g(x))*g'(x)")
f7 = func("sin(x**2)", "x")
df7 = diff(f7, "x")
print(f"  f(x) = {f7}")
print(f"  f'(x) = {df7}")
print(f"  f'(1) = {df7(1)}")

# 8. Trigonometric Derivatives
print("\n8. TRIGONOMETRIC DERIVATIVES")
print("  8a. sin(x): f'(x) = cos(x)")
f8a = func("sin(x)", "x")
df8a = diff(f8a, "x")
print(f"     f(x) = {f8a}, f'(x) = {df8a}, f'(1) = {df8a(1)}")

print("  8b. cos(x): f'(x) = -sin(x)")
f8b = func("cos(x)", "x")
df8b = diff(f8b, "x")
print(f"     f(x) = {f8b}, f'(x) = {df8b}, f'(1) = {df8b(1)}")

print("  8c. tan(x): f'(x) = sec^2(x)")
f8c = func("tan(x)", "x")
df8c = diff(f8c, "x")
print(f"     f(x) = {f8c}, f'(x) = {df8c}, f'(1) = {df8c(1)}")

print("  8d. sec(x): f'(x) = sec(x)*tan(x)")
f8d = func("sec(x)", "x")
df8d = diff(f8d, "x")
print(f"     f(x) = {f8d}, f'(x) = {df8d}, f'(1) = {df8d(1)}")

print("  8e. cot(x): f'(x) = -csc^2(x)")
f8e = func("cot(x)", "x")
df8e = diff(f8e, "x")
print(f"     f(x) = {f8e}, f'(x) = {df8e}, f'(1) = {df8e(1)}")

print("  8f. csc(x): f'(x) = -csc(x)*cot(x)")
f8f = func("csc(x)", "x")
df8f = diff(f8f, "x")
print(f"     f(x) = {f8f}, f'(x) = {df8f}, f'(1) = {df8f(1)}")

# 9. Exponential Derivatives
print("\n9. EXPONENTIAL DERIVATIVES")
print("  9a. e^x: f'(x) = e^x")
f9a = func("exp(x)", "x")
df9a = diff(f9a, "x")
print(f"     f(x) = {f9a}, f'(x) = {df9a}, f'(1) = {df9a(1)}")

print("  9b. e^(g(x)): f'(x) = e^(g(x))*g'(x)")
f9b = func("exp(x**2)", "x")
df9b = diff(f9b, "x")
print(f"     f(x) = {f9b}, f'(x) = {df9b}, f'(1) = {df9b(1)}")

print("  9c. a^x: f'(x) = ln(a)*a^x (where a=2)")
f9c = func("2**x", "x")
df9c = diff(f9c, "x")
print(f"     f(x) = {f9c}, f'(x) = {df9c}, f'(2) = {df9c(2)}")

print("  9d. a^(g(x)): f'(x) = ln(a)*a^(g(x))*g'(x) (where a=3, g(x)=x^2)")
f9d = func("3**(x**2)", "x")
df9d = diff(f9d, "x")
print(f"     f(x) = {f9d}, f'(x) = {df9d}, f'(1) = {df9d(1)}")

# 10. Logarithmic Derivatives
print("\n10. LOGARITHMIC DERIVATIVES")
print("  10a. ln(x): f'(x) = 1/x")
f10a = func("ln(x)", "x")
df10a = diff(f10a, "x")
print(f"      f(x) = {f10a}, f'(x) = {df10a}, f'(2) = {df10a(2)}")

print("  10b. ln(g(x)): f'(x) = g'(x)/g(x)")
f10b = func("ln(x**2 + 1)", "x")
df10b = diff(f10b, "x")
print(f"      f(x) = {f10b}, f'(x) = {df10b}, f'(2) = {df10b(2)}")

# 11. Combined Examples
print("\n11. COMBINED EXAMPLES")
f11a = func("x**2 * exp(x) + sin(x) * cos(x)", "x")
df11a = diff(f11a, "x")
print(f"  f(x) = {f11a}")
print(f"  f'(x) = {df11a}")
print(f"  f'(1) = {df11a(1)}")

f11b = func("ln(x) / x**2", "x")
df11b = diff(f11b, "x")
print(f"  f(x) = {f11b}")
print(f"  f'(x) = {df11b}")
print(f"  f'(2) = {df11b(2)}")

f11c = func("sin(x**2 + 1) * exp(x)", "x")
df11c = diff(f11c, "x")
print(f"  f(x) = {f11c}")
print(f"  f'(x) = {df11c}")
print(f"  f'(1) = {df11c(1)}")

print("\n" + "=" * 60)

