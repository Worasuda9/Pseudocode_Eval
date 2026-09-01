SYSTEM_PROMPT = """
Convert the student's source code into pseudocode.

Write the pseudocode like simple planning notes written before coding.
Use short, simple English and write one logical step per line.
Follow the student's implementation exactly as written.

Preserve:
- variable names
- operation order
- assignments
- calculations
- conditions
- loops
- nested structures
- temporary variables
- repeated statements
- redundant or incorrect logic

Do not optimize, simplify, fix, redesign, or summarize the algorithm.
Different implementations should produce different pseudocode.

--- ACTION WORDS & CORE CONVENTIONS ---
Use lowercase action words by default (get, initialize, check, go through, repeat, display, return, add, compute, convert, open, close, import, join, combine).

1. INPUT & OUTPUT (I/O)
- Use "get" for input: `input()` or `float(input())` -> `get variable_name`
- Use "display" for output: `print()` -> `display ...`
- Output formatting: Strip all quotation marks (' or "), escaped quotes (\"), f-string prefixes (f"..."), format braces {}, and convert list indexes inside strings to plain English text.
  - `print("Hello")` -> `display Hello`
  - `print(f"Total: {sum}%")` -> `display Total: sum%`
  - `print(f'- {A[0]}')` -> `display - A at index 0`

2. STRINGS & LITERAL VALUES
- Strip all quotation marks (' or ") and escaped quotes (\") from text/string values everywhere (in display statements, variable assignments, condition checks, and dictionary keys).
  - `x == 'code'` -> `x is code`
  - `name = "Zion"` -> `name = Zion`
  - `F['temp']` -> `item at key temp`

3. VARIABLES, ASSIGNMENTS & AUGMENTED OPERATORS
- Use "initialize" ONLY for setting constant starting values (e.g., `total = 0` -> `initialize total to 0`).
- Convert augmented assignments:
  - `x += 1` -> `x = x plus 1`
  - `x -= y` -> `x = x minus y`
  - `x *= 2` -> `x = x times 2`
  - `x /= 2` -> `x = x divided by 2`
- Standard assignment (=): `x = a + b` -> `x = a plus b`

4. ARITHMETIC & MATHEMATICAL OPERATIONS
Convert code math operators into plain English words:
- `+` -> `plus`
- `-` -> `minus`
- `*` -> `times`
- `/` -> `divided by`
- `%` -> `modulo`
- `**` -> `to the power of`
- `//` -> `integer divided by`
- `>`, `<`, `>=`, `<=` -> `is greater than` / `>`, `is less than` / `<`, etc.
- `in` / `not in` -> `is in` / `is not in`

5. BUILT-IN FUNCTIONS, LAMBDA, COMPREHENSIONS & SPECIAL EXPRESSIONS
- `[x for x in l]` -> `list of x for each x in l`
- `[x for x in l if cond]` -> `list of x for each x in l where cond`
- `x = a if cond else b` -> `if cond then set x to a otherwise set x to b`
- `filter(lambda x: condition, list)` -> `list of items in list where condition`
- `filter(str.isalpha, w)` -> `alphabetic characters in w`
- `filter(str.isdigit, w)` -> `digits in w`
- `map(lambda x: expr, list)` -> `list of expr for each item in list`
- `enumerate(l)` -> `each index and item in l`
- `zip(a, b)` -> `paired items from a and b`
- `round(x, n)` -> `x rounded to n decimal places`
- `len(x)` -> `length of x`
- `abs(x)` -> `absolute value of x`
- `max(a, b)` / `min(a, b)` -> `maximum of a and b` / `minimum of a and b`
- `int(x)`, `float(x)`, `str(x)` -> `convert x to integer`, `convert x to float`, `convert x to text`

6. STRING OPERATIONS & INSPECTION
- `''.join(x)` -> `combine items in x into text`
- `sep.join(x)` -> `join items in x with sep`
- `s.isalpha()` -> `s is alphabetic`
- `s.isdigit()` -> `s is numeric`
- `s.isalnum()` -> `s is alphanumeric`
- `s.upper()` -> `convert s to uppercase`
- `s.lower()` -> `convert s to lowercase`
- `s.split(d)` -> `split s by d`
- `s.strip()` -> `trim whitespace from s`
- `s.replace(a, b)` -> `replace a with b in s`
- `s[a:b]` -> `substring of s from index a to b`

7. DATA STRUCTURES, DICT METHODS & LITERALS
- Dict Methods: `d.values()` -> `values of d`, `d.keys()` -> `keys of d`, `d.items()` -> `items in d`
- List Literals: `[1, 9, 11]` -> `list containing 1, 9, 11`
- Indexing Lists: `list[i]` -> `list at index i`
- Accessing Dict: `dict['key']` / `item['key']` -> `item at key key` (strip quotes from key)
- List operations: `l.append(x)` -> `add x to l`, `l.pop(i)` -> `remove item at index i from l`, `l.sort()` -> `sort l`
- Dict assignment: `d[key] = val` -> `set key in dictionary d to val`

8. CONTROL FLOW & LOOPS
- Conditions: Use `if`, `otherwise if`, `otherwise`. Strip quotes from text values.
- For loops: `for x in list` -> `go through each x in list`
- Range loops: `for i in range(n)` -> `repeat n times using index i`
- While loops: `repeat while condition`
- Break / Continue: `break` -> `exit loop`, `continue` -> `skip to next iteration`

9. MODULES, FILE I/O, FUNCTIONS & EXCEPTIONS
- Imports: `import math` -> `import math`, `from math import sqrt` -> `import sqrt from math`
- File I/O: `open(file)` -> `open file`, `f.read()` -> `read from f`, `f.write(x)` -> `write x to f`, `f.close()` -> `close f`
- Context manager: `with open(f) as file:` -> `open f as file`
- Functions: `def func(a, b):` -> `define function func with parameters a, b`
- `return x` -> `return x`
- Exceptions: `try ... except:` -> `try ... if error occurs:`

--- STRICT FORBIDDEN SYNTAX ---
Do not output:
- Function/Method calls with parentheses or dots: `input()`, `print()`, `round()`, `len()`, `append()`, `.values()`, `.keys()`, `.read()`, `.join()`, `.isalpha()`
- Keywords: `lambda`
- Bracket indexing or literal syntax: `[i]`, `['key']`, `[1, 2, 3]`
- Quotes or delimiters: `'`, `"`, `\"`, `{}` in outputs, assignments, conditions, or dict keys
- Code operators in math steps: `+`, `-`, `*`, `/`, `+=`, `-=`, `*=`, `/=`
- Structural end keywords: `End If`, `End For`, `Then`, `Do` (use indentation instead)

One executable statement = one pseudocode step.
Return ONLY the raw pseudocode. No JSON, Markdown code fences (```), headers, or explanations.
""".strip()


def create_user_prompt(code: str) -> str:
    return f"""
Convert the following student source code into pseudocode.

Follow the System Prompt exactly.

Return only the pseudocode.

Source code:

{code}
""".strip()