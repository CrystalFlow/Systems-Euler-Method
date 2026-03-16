import math
import re


# Safe math namespace exposed to user expressions
_MATH_NAMESPACE = {
    "__builtins__": {},
    "sin":  math.sin,
    "cos":  math.cos,
    "tan":  math.tan,
    "asin": math.asin,
    "acos": math.acos,
    "atan": math.atan,
    "exp":  math.exp,
    "log":  math.log,
    "log2": math.log2,
    "log10":math.log10,
    "sqrt": math.sqrt,
    "abs":  abs,
    "pi":   math.pi,
    "e":    math.e,
}


def _normalize_expression(expr: str) -> str:
    """
    Cleans up common informal math notation so eval can handle it.
      2x      -> 2*x
      2(x+y)  -> 2*(x+y)
      x^2     -> x**2
    """
    expr = expr.strip()
    # Replace ^ with **
    expr = expr.replace("^", "**")
    # Insert * between a digit and a letter/opening-paren: 2x -> 2*x, 2(x) -> 2*(x)
    expr = re.sub(r"(\d)([a-zA-Z(])", r"\1*\2", expr)
    # Insert * between ) and a letter/digit/opening-paren: (x)y -> (x)*y
    expr = re.sub(r"(\))([a-zA-Z\d(])", r"\1*\2", expr)
    return expr


def parse_equation(equation_str: str):
    """
    Parses a differential equation string and returns a callable f(x, y).

    Variables:  x, y
    Operators:  + - * / ** ( )   (^ is also accepted)
    Functions:  sin cos tan asin acos atan exp log log2 log10 sqrt abs
    Constants:  pi  e

    Parameters
    ----------
    equation_str : str
        A mathematical expression in terms of x and/or y.
        Example: "-y", "x + 2*y", "sin(x)*y", "x^2 - 3y"

    Returns
    -------
    callable
        A function f(x, y) -> float that evaluates the expression.

    Raises
    ------
    ValueError
        If the expression has a syntax error or uses disallowed names.
    """
    normalized = _normalize_expression(equation_str)

    # Compile once so syntax errors surface immediately
    try:
        code = compile(normalized, "<equation>", "eval")
    except SyntaxError as err:
        raise ValueError(f"Syntax error in '{equation_str}': {err}") from err

    # Check for names that aren't variables or allowed math symbols
    allowed_names = set(_MATH_NAMESPACE.keys()) | {"x", "y"}
    for name in code.co_names:
        if name not in allowed_names:
            raise ValueError(
                f"Unknown name '{name}' in equation. "
                f"Allowed variables are x and y; "
                f"allowed functions are: {', '.join(sorted(n for n in _MATH_NAMESPACE if n != '__builtins__'))}."
            )

    def equation(x: float, y: float) -> float:
        local_vars = {"x": x, "y": y}
        try:
            return eval(code, _MATH_NAMESPACE, local_vars)  # noqa: S307
        except ZeroDivisionError:
            raise ValueError("Division by zero while evaluating equation.")
        except Exception as err:
            raise ValueError(f"Error evaluating equation at x={x}, y={y}: {err}") from err

    equation.__doc__ = equation_str  # Store original string for display
    return equation


def get_user_equations() -> list:
    """
    Interactively prompts the user to enter a system of 1 or 2 differential
    equations as strings, parses each one, and returns a list of callables.

    Returns
    -------
    list of callable
        [f_x] for a single equation  or  [f_x, f_y] for a system.
        Each callable has the signature f(x, y) -> float.
    """
    print("\n--- Differential Equation Input ---")
    print("Variables : x, y")
    print("Functions : sin, cos, tan, asin, acos, atan, exp, log, log2, log10, sqrt, abs")
    print("Constants : pi, e")
    print("Operators : + - * / ** (or ^)  with parentheses as needed")
    print("Example   : dx/dt = -y   ->   enter: -y")
    print("            dy/dt = x    ->   enter: x\n")

    while True:
        try:
            n = int(input("Number of equations in the system (1 or 2): ").strip())
            if n in (1, 2):
                break
            print("  Please enter 1 or 2.")
        except ValueError:
            print("  Please enter a valid integer.")

    variable_names = ["x", "y"]
    equations = []

    for i in range(n):
        var = variable_names[i]
        while True:
            raw = input(f"  d{var}/dt = ").strip()
            if not raw:
                print("  Expression cannot be empty. Try again.")
                continue
            try:
                func = parse_equation(raw)
                # Validate with a test evaluation
                func(1.0, 1.0)
                equations.append(func)
                print(f"  Accepted: d{var}/dt = {raw}")
                break
            except ValueError as err:
                print(f"  Error: {err}  -- Please try again.")

    print()
    return equations
